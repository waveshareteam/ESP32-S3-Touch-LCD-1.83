from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "releases" / "package_firmware.py"
SPEC = importlib.util.spec_from_file_location("package_firmware", SCRIPT)
assert SPEC and SPEC.loader
package_firmware = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = package_firmware
SPEC.loader.exec_module(package_firmware)


class EspIdfFlashSourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.build_dir = self.root / "build"
        self.build_dir.mkdir()
        self.firmware_dir = self.root / "firmware"
        self.firmware_dir.mkdir()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_flasher_args(self, source: str) -> None:
        (self.build_dir / "flasher_args.json").write_text(
            json.dumps({"flash_files": {"0x1000": source}}), encoding="utf-8"
        )

    def test_nested_relative_file_is_packaged(self) -> None:
        source = self.build_dir / "nested" / "bootloader.bin"
        source.parent.mkdir()
        source.write_bytes(b"firmware")
        self.write_flasher_args("nested/bootloader.bin")

        _, entries, _ = package_firmware.esp_idf_flash_entries(
            self.build_dir, self.firmware_dir
        )

        self.assertEqual("nested/bootloader.bin", entries[0]["source"])
        self.assertEqual(b"firmware", (self.firmware_dir / "0x1000_bootloader.bin").read_bytes())

    def test_absolute_path_outside_build_directory_is_rejected(self) -> None:
        outside = self.root / "outside.bin"
        outside.write_bytes(b"outside")
        self.write_flasher_args(str(outside.resolve()))

        with self.assertRaisesRegex(ValueError, "escapes build directory"):
            package_firmware.esp_idf_flash_entries(self.build_dir, self.firmware_dir)

    def test_traversal_outside_build_directory_is_rejected(self) -> None:
        outside = self.root / "outside.bin"
        outside.write_bytes(b"outside")
        self.write_flasher_args("../outside.bin")

        with self.assertRaisesRegex(ValueError, "escapes build directory"):
            package_firmware.esp_idf_flash_entries(self.build_dir, self.firmware_dir)

    def test_symbolic_link_component_is_rejected(self) -> None:
        real_dir = self.build_dir / "real"
        real_dir.mkdir()
        (real_dir / "bootloader.bin").write_bytes(b"firmware")
        linked_dir = self.build_dir / "linked"
        try:
            linked_dir.symlink_to(real_dir, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symbolic links are unavailable: {exc}")
        self.write_flasher_args("linked/bootloader.bin")

        with self.assertRaisesRegex(ValueError, "symbolic link component"):
            package_firmware.esp_idf_flash_entries(self.build_dir, self.firmware_dir)

    def test_arduino_flash_entries_still_package_a_normal_binary(self) -> None:
        source = self.build_dir / "sketch.bin"
        source.write_bytes(b"arduino")

        command_pairs, entries = package_firmware.arduino_flash_entries(
            self.build_dir, self.firmware_dir
        )

        self.assertEqual(["0x10000", "bin/0x10000_sketch.bin"], command_pairs)
        self.assertEqual("sketch.bin", entries[0]["source"])
        self.assertEqual(b"arduino", (self.firmware_dir / "0x10000_sketch.bin").read_bytes())


if __name__ == "__main__":
    unittest.main()
