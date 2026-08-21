from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_immutable_artifacts.py"


class ImmutableArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)
        self.artifact = self.repo / "firmware" / "factory.bin"
        self.artifact.parent.mkdir()
        self.artifact.write_bytes(b"immutable fixture\n")
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "add", "firmware/factory.bin"], check=True)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_manifest(self, content: str | None = None) -> Path:
        path = self.repo / "manifest.sha256"
        if content is None:
            content = f"{hashlib.sha256(self.artifact.read_bytes()).hexdigest()}  firmware/factory.bin\n"
        path.write_text(content, encoding="utf-8")
        return path

    def run_checker(self, manifest: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(self.repo), "--manifest", str(manifest)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_passes_for_matching_tracked_artifact(self) -> None:
        result = self.run_checker(self.write_manifest())
        self.assertEqual(0, result.returncode, result.stderr)

    def test_rejects_digest_mismatch(self) -> None:
        result = self.run_checker(self.write_manifest("0" * 64 + "  firmware/factory.bin\n"))
        self.assertEqual(1, result.returncode)
        self.assertIn("digest mismatch", result.stderr)

    def test_rejects_missing_or_unlisted_delivery_artifact(self) -> None:
        missing = self.run_checker(self.write_manifest("0" * 64 + "  firmware/missing.bin\n"))
        self.assertEqual(1, missing.returncode)
        self.assertIn("missing immutable artifact", missing.stderr)

        policy = self.repo / "config" / "policy.txt"
        policy.parent.mkdir()
        policy.write_text("policy\n", encoding="utf-8")
        unlisted = self.run_checker(
            self.write_manifest(
                f"{hashlib.sha256(policy.read_bytes()).hexdigest()}  config/policy.txt\n"
            )
        )
        self.assertEqual(1, unlisted.returncode)
        self.assertIn("unlisted tracked delivery artifact", unlisted.stderr)

    def test_rejects_malformed_or_escaping_manifest_path(self) -> None:
        malformed = self.run_checker(self.write_manifest("not-a-manifest\n"))
        self.assertEqual(1, malformed.returncode)
        self.assertIn("malformed manifest", malformed.stderr)

        escaping = self.run_checker(self.write_manifest("0" * 64 + "  ../outside.bin\n"))
        self.assertEqual(1, escaping.returncode)
        self.assertIn("unsafe manifest path", escaping.stderr)


if __name__ == "__main__":
    unittest.main()
