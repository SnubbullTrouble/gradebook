import tomli
import os
import tomli_w
from gradebook.views.main_window.save_state import SaveState
from dataclasses import asdict


def save_to_toml(file_path: str, save_state: SaveState) -> None:
    """Writes the SaveState object to the toml file, skipping None values"""
    # Remove any None values so tomli_w won't crash
    data = {k: v for k, v in asdict(save_state).items() if v is not None}

    with open(file_path, "wb") as file:
        tomli_w.dump(data, file)


def load_from_toml(file_path: str) -> SaveState:
    """Reads a SaveState object from the toml file"""
    if not os.path.exists(file_path):
        default_state = SaveState()
        save_to_toml(file_path, default_state)
        return default_state

    with open(file_path, "rb") as file:
        data = tomli.load(file)

    # Missing keys automatically become dataclass defaults (often None)
    return SaveState(**data)
