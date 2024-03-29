import json


class Settings(dict):
    BINS = "Bins (Histogram)"
    BW_FACTOR = "Band-width factor (KDE plots)"
    COMMON_NORMALIZATION = "Common normalization (Histogram & KDE)"
    CONFIDENCE_INTERVAL = "Confidence interval (Regression)"
    POLYNOMIAL_DEGREE = "Polynomial degree"
    NUMERIC_HUE = "Numeric hue"

    def __init__(self):
        super().__init__()
        self.define_defaults()

    def define_defaults(self):
        self[self.BINS] = "auto"
        self[self.BW_FACTOR] = 1
        self[self.COMMON_NORMALIZATION] = False
        self[self.CONFIDENCE_INTERVAL] = 95
        self[self.POLYNOMIAL_DEGREE] = 2
        self[self.NUMERIC_HUE] = False

    def reload(self, path="settings.json"):
        try:
            with open(path) as f:
                data: dict = json.load(f)
                for key, value in data.items():
                    if key in self:
                        self[key] = value
        except FileNotFoundError:
            pass

    def save(self, path="settings.json"):
        with open(path, "w") as f:
            json.dump(self, f, indent=2)
