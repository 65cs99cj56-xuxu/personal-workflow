from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "detect_delivery_package.py"
SPEC = importlib.util.spec_from_file_location("detect_delivery_package", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DetectDeliveryPackageTest(unittest.TestCase):
    def scan(self, files: dict[str, str]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative_path, content in files.items():
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return MODULE.scan(root)

    def test_screenshot_only_does_not_trigger(self) -> None:
        result = self.scan({"screen.png": "image"})
        self.assertFalse(result["source_eligible"])

    def test_html_only_does_not_trigger(self) -> None:
        result = self.scan({"index.html": "<main></main>"})
        self.assertFalse(result["source_eligible"])

    def test_inline_css_and_javascript_do_not_trigger(self) -> None:
        result = self.scan(
            {"index.html": "<style>body{}</style><script>void 0</script>"}
        )
        self.assertFalse(result["source_eligible"])

    def test_html_and_css_trigger(self) -> None:
        result = self.scan({"index.html": "", "styles/page.css": "body{}"})
        self.assertTrue(result["source_eligible"])
        self.assertEqual(result["files"]["javascript"], [])

    def test_html_and_javascript_trigger(self) -> None:
        result = self.scan({"index.htm": "", "scripts/page.ts": "export {}"})
        self.assertTrue(result["source_eligible"])
        self.assertEqual(result["files"]["css"], [])

    def test_html_css_and_javascript_trigger(self) -> None:
        result = self.scan(
            {"index.html": "", "page.scss": ".page{}", "page.js": "void 0"}
        )
        self.assertTrue(result["source_eligible"])

    def test_node_modules_sources_are_ignored(self) -> None:
        result = self.scan(
            {
                "index.html": "",
                "node_modules/package/index.js": "void 0",
                "node_modules/package/index.css": "body{}",
            }
        )
        self.assertFalse(result["source_eligible"])

    def test_fingerprint_changes_with_content(self) -> None:
        first = self.scan({"index.html": "v1", "page.css": "body{}"})
        second = self.scan({"index.html": "v2", "page.css": "body{}"})
        self.assertNotEqual(first["package_fingerprint"], second["package_fingerprint"])

    def test_cli_exit_codes_match_routing_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("", encoding="utf-8")
            (root / "page.css").write_text("body{}", encoding="utf-8")
            eligible = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(eligible.returncode, 0)
            self.assertIn('"source_eligible": true', eligible.stdout)
            self.assertNotIn('"triggered"', eligible.stdout)

            (root / "page.css").unlink()
            ineligible = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(ineligible.returncode, 3)
            self.assertIn('"source_eligible": false', ineligible.stdout)
            self.assertNotIn('"triggered"', ineligible.stdout)

            invalid = subprocess.run(
                [sys.executable, str(SCRIPT), str(root / "missing")],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(invalid.returncode, 2)
            self.assertIn('"error"', invalid.stdout)

    def test_directory_scan_error_is_not_treated_as_ineligible(self) -> None:
        def failing_walk(root, followlinks=False, onerror=None):
            assert onerror is not None
            onerror(PermissionError(13, "Permission denied", str(root)))
            return iter(())

        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(MODULE.os, "walk", side_effect=failing_walk):
                with self.assertRaisesRegex(OSError, "Permission denied"):
                    MODULE.scan(Path(directory))

    def test_file_read_error_is_not_treated_as_ineligible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("", encoding="utf-8")
            original_open = MODULE.Path.open

            def failing_open(path, *args, **kwargs):
                if path.name == "index.html":
                    raise PermissionError(13, "Permission denied", str(path))
                return original_open(path, *args, **kwargs)

            with mock.patch.object(MODULE.Path, "open", new=failing_open):
                with self.assertRaisesRegex(OSError, "index.html.*Permission denied"):
                    MODULE.scan(root)

    def test_file_stat_error_is_not_treated_as_ineligible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("", encoding="utf-8")
            original_stat = MODULE.Path.stat

            def failing_stat(path, *args, **kwargs):
                if path.name == "index.html":
                    raise PermissionError(13, "Permission denied", str(path))
                return original_stat(path, *args, **kwargs)

            with mock.patch.object(MODULE.Path, "stat", new=failing_stat):
                with self.assertRaisesRegex(OSError, "index.html.*Permission denied"):
                    MODULE.scan(root)

    def test_main_returns_exit_two_when_scan_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = io.StringIO()
            with (
                mock.patch.object(MODULE.sys, "argv", [str(SCRIPT), directory]),
                mock.patch.object(
                    MODULE,
                    "scan",
                    side_effect=PermissionError(13, "Permission denied", directory),
                ),
                mock.patch.object(MODULE.sys, "stdout", output),
            ):
                self.assertEqual(MODULE.main(), 2)

            self.assertIn('"error": "delivery package scan failed"', output.getvalue())


if __name__ == "__main__":
    unittest.main()
