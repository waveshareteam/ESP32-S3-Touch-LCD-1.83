#!/usr/bin/env python3
"""Discover first-party examples for CI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ARDUINO_FQBN = (
    "esp32:esp32:esp32s3:FlashMode=qio,FlashSize=16M,PSRAM=opi,"
    "USBMode=hwcdc,PartitionScheme=default"
)


def normalize(value: str) -> str:
    return value.replace("\\", "/").strip("/")


def selector_matches(entry: dict[str, str], selector: str) -> bool:
    if not selector or selector == "all":
        return True
    selector = normalize(selector)
    path = normalize(entry["path"])
    name = entry["name"]
    return (
        selector == name
        or selector == path
        or path.startswith(selector + "/")
        or selector in path.split("/")
    )


def discover_esp_idf(repo: Path) -> list[dict[str, str]]:
    root = repo / "examples" / "esp-idf"
    if not root.exists():
        return []
    entries: list[dict[str, str]] = []
    for project in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        if project.is_dir() and (project / "CMakeLists.txt").exists():
            entries.append({"name": project.name, "path": project.relative_to(repo).as_posix()})
    return entries


def discover_arduino(repo: Path) -> list[dict[str, str]]:
    root = repo / "examples" / "arduino"
    if not root.exists():
        return []
    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for ino in sorted(root.rglob("*.ino"), key=lambda item: item.as_posix().lower()):
        rel = ino.relative_to(repo).as_posix()
        if rel.startswith("examples/arduino/libraries/"):
            continue
        sketch_dir = ino.parent.relative_to(repo).as_posix()
        if sketch_dir in seen:
            continue
        seen.add(sketch_dir)
        entries.append({"name": ino.parent.name, "path": sketch_dir})
    return entries


def build_matrix(args: argparse.Namespace) -> dict[str, list[dict[str, str]]]:
    repo = Path(args.repo).resolve()
    selector = normalize(args.selector)
    routed_paths: set[str] | None = None
    if args.selected_paths is not None:
        selected = json.loads(args.selected_paths)
        if not isinstance(selected, list) or not all(isinstance(path, str) for path in selected):
            raise ValueError("--selected-paths must be a JSON list of repo-relative paths")
        routed_paths = {normalize(path) for path in selected}
    if args.routing_report:
        report = json.loads(Path(args.routing_report).read_text(encoding="utf-8"))
        key = "esp_idf" if args.surface == "esp-idf" else "arduino"
        route = report[key]
        if route["mode"] == "none":
            routed_paths = set()
        elif route["mode"] == "selected":
            routed_paths = {normalize(path) for path in route["selected"]}
        elif route["mode"] != "all":
            raise ValueError(f"unsupported routing mode for {key}: {route['mode']}")
    if args.surface == "esp-idf":
        projects = [entry for entry in discover_esp_idf(repo) if selector_matches(entry, selector)]
        if routed_paths is not None:
            projects = [entry for entry in projects if normalize(entry["path"]) in routed_paths]
        versions = [item.strip() for item in args.idf_versions.split(",") if item.strip()]
        include = [entry | {"idf": version} for entry in projects for version in versions]
    else:
        sketches = [entry for entry in discover_arduino(repo) if selector_matches(entry, selector)]
        if routed_paths is not None:
            sketches = [entry for entry in sketches if normalize(entry["path"]) in routed_paths]
        include = [entry | {"core": args.arduino_core, "fqbn": args.fqbn} for entry in sketches]
    return {"include": include}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--surface", choices=("esp-idf", "arduino"), required=True)
    parser.add_argument("--selector", default="all")
    parser.add_argument("--idf-versions", default="v5.5.5,v6.0.2")
    parser.add_argument("--arduino-core", default="3.3.11")
    parser.add_argument("--fqbn", default=ARDUINO_FQBN)
    parser.add_argument("--routing-report", help="JSON report emitted by audit_ci_routing.py")
    parser.add_argument("--selected-paths", help="JSON list of paths selected by CI routing")
    parser.add_argument("--github-output")
    args = parser.parse_args()

    matrix = build_matrix(args)
    output = json.dumps(matrix, separators=(",", ":"))
    count = len(matrix["include"])
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as fh:
            fh.write(f"matrix={output}\n")
            fh.write(f"count={count}\n")
    else:
        print(output)


if __name__ == "__main__":
    main()
