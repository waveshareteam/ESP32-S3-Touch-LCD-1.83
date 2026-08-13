from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CMAKE = ROOT / "examples/esp-idf/03_esp-brookesia/components/apps/CMakeLists.txt"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "waveshare_audit_ci_routing_brookesia", SCRIPTS / "audit_ci_routing.py"
)
assert SPEC and SPEC.loader
audit_ci_routing = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit_ci_routing
SPEC.loader.exec_module(audit_ci_routing)


class BrookesiaCmakeContractTests(unittest.TestCase):
    def test_mixed_language_warning_suppressions_are_c_scoped(self) -> None:
        cmake = CMAKE.read_text(encoding="utf-8")

        self.assertIn("file(GLOB_RECURSE APPS_C_SRCS", cmake)
        self.assertIn("file(GLOB_RECURSE APPS_CPP_SRCS", cmake)
        self.assertIn(
            "$<$<COMPILE_LANGUAGE:C>:-Wno-incompatible-pointer-types>", cmake
        )
        self.assertIn("$<$<COMPILE_LANGUAGE:C>:-Wno-int-conversion>", cmake)
        self.assertIn("        -Wno-format", cmake)
        self.assertNotRegex(
            cmake, r"(?m)^\s+-Wno-incompatible-pointer-types\s*$"
        )
        self.assertNotRegex(cmake, r"(?m)^\s+-Wno-int-conversion\s*$")

    def test_component_change_routes_only_its_idf_project(self) -> None:
        report = audit_ci_routing.route_changes(
            ROOT,
            [
                audit_ci_routing.Change(
                    "M", CMAKE.relative_to(ROOT).as_posix()
                )
            ],
            audit_ci_routing.load_routing_config(ROOT / "config/ci-routing.json"),
            audit_ci_routing.load_ownership_config(ROOT / "config/markdown-audit.json"),
            max_files=5000,
            max_text_files=1000,
        )

        self.assertEqual("selected", report["esp_idf"]["mode"])
        self.assertEqual(
            ["examples/esp-idf/03_esp-brookesia"], report["esp_idf"]["selected"]
        )
        self.assertEqual("none", report["arduino"]["mode"])


if __name__ == "__main__":
    unittest.main()
