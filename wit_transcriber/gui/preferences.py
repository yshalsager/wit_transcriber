import json
from pathlib import Path
from typing import Dict


class PreferencesManager:
    def __init__(self, path: Path) -> None:
        self.filename: Path = path / "config.json"
        self.settings_object: Dict[str, str] = {}
        if not self.filename.exists():
            self.create_preferences_file()
        else:
            self.load_preferences_file()

    def load_preferences_file(self) -> None:
        self.settings_object = json.loads(self.filename.read_text())

    def create_preferences_file(self) -> None:
        self.settings_object = {
            "ar": "",
        }
        self.update_preferences_file()

    def update_preferences_file(self) -> None:
        self.filename.write_text(json.dumps(self.settings_object, indent=4))

    def put(self, key: str, value: str) -> None:
        self.settings_object[key] = value
        self.update_preferences_file()

    def get(self, key: str) -> str:
        self.load_preferences_file()
        return self.settings_object[key]

    def get_json(self) -> Dict[str, str]:
        return self.settings_object

    def check_if_ar_key_exists(self) -> str:
        return self.get("ar")

    def get_config_file(self) -> Path:
        return Path(self.filename)
