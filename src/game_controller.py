import json
import pyautogui

class GameController:
    def __init__(self, config_path="config/key_bindings.json"):
        with open(config_path) as f:
            self.key_bindings = json.load(f)
        self.current_keys = set()

    def press_key(self, key):
        if key not in self.current_keys:
            pyautogui.keyDown(key)
            self.current_keys.add(key)

    def release_key(self, key):
        if key in self.current_keys:
            pyautogui.keyUp(key)
            self.current_keys.remove(key)

    def release_all_keys(self):
        for key in list(self.current_keys):
            self.release_key(key)

    def mouse_action(self, action="up"):
        if action == "down":
            pyautogui.mouseDown(button=self.key_bindings["shoot"])
        else:
            pyautogui.mouseUp(button=self.key_bindings["shoot"])
