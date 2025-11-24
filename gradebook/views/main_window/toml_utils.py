import tomli
import os
import tomli_w
from gradebook.views.main_window.save_state import SaveState
from dataclasses import asdict

def save_to_toml(file_path: str, save_state: SaveState) -> None:
    with open(file_path, "wb") as file:
        tomli_w.dump(asdict(save_state), file)

def load_from_toml(file_path: str) -> SaveState:
    if not os.path.exists(file_path):
        default_state = SaveState() 
        save_to_toml(file_path, default_state)
        return default_state
    
    with open(file_path, "rb") as file:
        data = tomli.load(file)

    return SaveState(**data)