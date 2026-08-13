from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "examples.yml"


class ExamplesWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_manual_and_tag_runs_always_select_complete_matrices(self) -> None:
        self.assertNotIn("inputs.target", self.workflow)
        self.assertNotIn("inputs.", self.workflow)
        self.assertNotIn("github.event.inputs", self.workflow)
        self.assertNotRegex(self.workflow, r"(?m)^\s+inputs:")
        self.assertNotRegex(self.workflow, r"(?m)^\s+target:")
        self.assertIn('if [[ "${{ github.event_name }}" == "workflow_dispatch" ]]; then', self.workflow)
        self.assertIn('if [[ "${{ github.ref_type }}" == "tag" ]]; then', self.workflow)
        self.assertEqual(2, self.workflow.count('echo "selector=all" >> "$GITHUB_OUTPUT"'))
        self.assertIn("--idf-versions v5.5.5,v6.0.2", self.workflow)
        self.assertIn("--arduino-core 3.3.11", self.workflow)
        self.assertIn(
            "--fqbn esp32:esp32:esp32s3:FlashMode=qio,FlashSize=16M,PSRAM=opi,USBMode=hwcdc,PartitionScheme=default",
            self.workflow,
        )

    def test_scope_checks_use_complete_range_and_publish_routing_flags(self) -> None:
        self.assertIn("git diff --check $diff_range", self.workflow)
        self.assertIn(
            "python3 scripts/check_immutable_artifacts.py . --manifest config/immutable-artifacts.sha256",
            self.workflow,
        )
        for flag in ("docs_only", "firmware_touched", "release_review_required"):
            self.assertIn(f"{flag}: ${{{{ steps.select.outputs.{flag} }}}}", self.workflow)
        self.assertIn("for key in ('docs_only', 'firmware_touched', 'release_review_required'):", self.workflow)
        self.assertIn('out.write(f"{key}=', self.workflow)
        self.assertIn("GITHUB_STEP_SUMMARY", self.workflow)

    def test_cancellation_preserves_manual_and_tag_runs(self) -> None:
        self.assertIn(
            "cancel-in-progress: ${{ github.event_name != 'workflow_dispatch' "
            "&& github.ref_type != 'tag' }}",
            self.workflow,
        )

    def test_actions_use_supported_majors(self) -> None:
        self.assertNotIn("actions/checkout@v4", self.workflow)
        self.assertNotIn("actions/upload-artifact@v4", self.workflow)
        self.assertEqual(5, self.workflow.count("actions/checkout@v7"))
        self.assertEqual(2, self.workflow.count("actions/upload-artifact@v7"))
        self.assertIn("arduino/setup-arduino-cli@v2", self.workflow)


if __name__ == "__main__":
    unittest.main()
