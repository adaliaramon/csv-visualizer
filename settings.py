import json


class Settings(dict):
    def __init__(self):
        super().__init__()
        self.define_defaults()

    def define_defaults(self):
        self["bins"] = "auto"
        self["band-width factor"] = 1
        self["confidence interval"] = 95
        self["polynomial degree"] = 2

    def reload(self, path="settings.json"):
        try:
            with open(path, "r") as f:
                data: dict = json.load(f)
                for key, value in data.items():
                    self[key] = value
        except FileNotFoundError:
            pass

    def save(self, path="settings.json"):
        with open(path, "w") as f:
            json.dump(self, f, indent=2)
