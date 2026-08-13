#!/usr/bin/env python3
"""Verify the repository's checked-in immutable delivery artifacts."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath


LINE = re.compile(r"^([0-9a-f]{64})  ([^\r\n]+)$")
DELIVERY_SUFFIXES = (".bin", ".zip", ".7z", ".tar", ".tgz", ".tar.gz", ".xz", ".bz2")


class ManifestError(ValueError):
    """A manifest or artifact does not meet the immutable-artifact policy."""


def repository_path(value: str) -> str:
    if not value or "\\" in value or "\x00" in value:
        raise ManifestError("manifest path must be a non-empty POSIX relative path")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise ManifestError(f"unsafe manifest path: {value!r}")
    return pure.as_posix()


def parse_manifest(path: Path) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ManifestError(f"cannot read manifest: {exc}") from exc
    if not lines:
        raise ManifestError("manifest is empty")
    entries: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        match = LINE.fullmatch(line)
        if not match:
            raise ManifestError(f"malformed manifest line {number}")
        digest, raw_path = match.groups()
        relative = repository_path(raw_path)
        if relative in entries:
            raise ManifestError(f"duplicate manifest path: {relative}")
        entries[relative] = digest
    return entries


def checked_in_paths(repo: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "-z", "--", "firmware"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ManifestError("cannot enumerate tracked firmware artifacts") from exc
    return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def delivery_artifacts(repo: Path) -> set[str]:
    return {
        path for path in checked_in_paths(repo)
        if path.lower().endswith(DELIVERY_SUFFIXES)
    }


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify(repo: Path, manifest: Path) -> None:
    repo = repo.resolve()
    entries = parse_manifest(manifest)
    for relative, expected in entries.items():
        candidate = repo / relative
        try:
            candidate.resolve().relative_to(repo)
            mode = candidate.lstat().st_mode
        except (OSError, ValueError) as exc:
            raise ManifestError(f"missing immutable artifact: {relative}") from exc
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise ManifestError(f"immutable artifact is not a regular file: {relative}")
        if digest(candidate) != expected:
            raise ManifestError(f"digest mismatch: {relative}")
    missing = sorted(delivery_artifacts(repo) - set(entries))
    if missing:
        raise ManifestError("unlisted tracked delivery artifact: " + ", ".join(missing))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--manifest", default="config/immutable-artifacts.sha256")
    args = parser.parse_args()
    repo = Path(args.repo)
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = repo / manifest
    try:
        verify(repo, manifest)
    except ManifestError as exc:
        print(f"immutable artifact check failed: {exc}", file=sys.stderr)
        return 1
    print("immutable artifact check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
