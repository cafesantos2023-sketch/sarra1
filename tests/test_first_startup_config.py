import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import ui


class FirstStartupConfigTests(unittest.TestCase):
    def test_first_startup_avatar_is_85_percent_and_stays_centered(self):
        geometry = ui.QRect(100, 200, 520, 620)

        scaled = ui._first_startup_avatar_geometry(geometry)

        self.assertEqual((scaled.width(), scaled.height()), (442, 527))
        self.assertEqual(scaled.center(), geometry.center())

    def test_setup_saves_requested_defaults(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "config"
            config_file = config_dir / "api_keys.json"
            window = SimpleNamespace(
                _overlay=None,
                _apply_state=lambda _state: None,
                _assistant_name="",
                _log=SimpleNamespace(append_log=lambda _message: None),
                _setup_return_to_avatar_only=False,
            )

            with (
                patch.object(ui, "CONFIG_DIR", config_dir),
                patch.object(ui, "API_FILE", config_file),
                patch.object(ui, "_read_full_config", return_value={"assistant_name": "Sarra"}),
            ):
                ui.MainWindow._on_setup_done(window, "test-key", "windows")

            config = json.loads(config_file.read_text(encoding="utf-8"))

        self.assertEqual(config["voice_name"], "Aoede")
        self.assertEqual(config["assistant_name"], "Sarra")
        self.assertEqual(config["user_name"], "")
        self.assertEqual(config["ui_color"], "#00d4ff")
        self.assertEqual(window._assistant_name, "Sarra")


if __name__ == "__main__":
    unittest.main()
