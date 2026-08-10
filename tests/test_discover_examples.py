from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISCOVER = ROOT / "scripts" / "discover_examples.py"
ROUTING = ROOT / "scripts" / "audit_ci_routing.py"


def run(*args: str) -> dict:
    process = subprocess.run(
        [sys.executable, str(DISCOVER), "--repo", str(ROOT), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(process.stdout)


def route(*changed_paths: str) -> dict:
    with tempfile.TemporaryDirectory() as temporary:
        changed = Path(temporary) / "changed.txt"
        changed.write_text(
            "".join(f"M\t{path}\n" for path in changed_paths),
            encoding="utf-8",
        )
        process = subprocess.run(
            [
                sys.executable,
                str(ROUTING),
                str(ROOT),
                "--changed-files-from",
                str(changed),
                "--routing-config",
                str(ROOT / "config" / "ci-routing.json"),
                "--ownership-config",
                str(ROOT / "config" / "markdown-audit.json"),
                "--format",
                "json",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return json.loads(process.stdout)


class DiscoverExamplesTests(unittest.TestCase):
    def test_first_party_counts_and_library_exclusion(self) -> None:
        idf = run("--surface", "esp-idf", "--selector", "all", "--idf-versions", "v5.5.5,v6.0.2")
        arduino = run("--surface", "arduino", "--selector", "all", "--arduino-core", "3.3.11")
        self.assertEqual(12, len(idf["include"]))
        self.assertEqual(9, len(arduino["include"]))
        self.assertFalse(any("/libraries/" in item["path"] for item in arduino["include"]))

    def test_name_and_path_selectors(self) -> None:
        by_name = run("--surface", "esp-idf", "--selector", "01_AXP2101", "--idf-versions", "v5.5.5,v6.0.2")
        by_path = run("--surface", "arduino", "--selector", "examples/arduino/09_LVGL_Arduino", "--arduino-core", "3.3.11")
        self.assertEqual(2, len(by_name["include"]))
        self.assertEqual(["examples/arduino/09_LVGL_Arduino"], [item["path"] for item in by_path["include"]])

    def test_routing_output_is_consumed_by_discovery_command(self) -> None:
        data = route(
            "examples/esp-idf/01_AXP2101/main/main.c",
            "examples/arduino/09_LVGL_Arduino/09_LVGL_Arduino.ino",
        )
        idf = run("--surface", "esp-idf", "--selector", "all", "--idf-versions", "v5.5.5,v6.0.2", "--selected-paths", json.dumps(data["esp_idf"]["selected"]))
        arduino = run("--surface", "arduino", "--selector", "all", "--arduino-core", "3.3.11", "--selected-paths", json.dumps(data["arduino"]["selected"]))
        self.assertEqual(2, len(idf["include"]))
        self.assertEqual(1, len(arduino["include"]))

    def test_global_workflow_route_selects_all_arduino_sketch_roots(self) -> None:
        data = route(".github/workflows/examples.yml")
        self.assertEqual("all", data["arduino"]["mode"])
        self.assertEqual(9, len(data["arduino"]["selected"]))
        self.assertEqual(
            len(data["arduino"]["selected"]),
            len(set(data["arduino"]["selected"])),
        )
        arduino = run(
            "--surface",
            "arduino",
            "--selector",
            "all",
            "--arduino-core",
            "3.3.11",
            "--selected-paths",
            json.dumps(data["arduino"]["selected"]),
        )
        self.assertEqual(9, len(arduino["include"]))

    def test_policy_only_changes_use_the_lightweight_gate(self) -> None:
        data = route(
            ".gitignore",
            "assets/ci-routing-config.json",
            "tests/test_discover_examples.py",
            "scripts/audit_markdown.py",
            "config/ci-routing.json",
            "config/markdown-audit.json",
            "releases/download_artifacts_impl.py",
        )
        self.assertEqual("none", data["esp_idf"]["mode"])
        self.assertEqual("none", data["arduino"]["mode"])


if __name__ == "__main__":
    unittest.main()
