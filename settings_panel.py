from tkinter import LEFT, Text, END, W, E
from tkinter.ttk import Label, Frame
from typing import Optional, Dict

from settings import Settings


class SettingsPanel(Frame):
    def __init__(self, master=None, settings: Optional[Settings] = None, **kw):
        super().__init__(master, **kw)
        self.settings = settings
        self._values: Dict[str, Text] = {}
        self.add_fields()

    def add_fields(self):
        row = 0
        for key, value in self.settings.items():
            self.columnconfigure(index=(1,), weight=1)
            label = Label(self, text=key, justify=LEFT)
            label.grid(row=row, column=0, padx=5, pady=5, sticky=W)
            value_field = Text(self, height=1, width=20)
            value_field.insert(END, value)
            value_field.grid(row=row, column=1, padx=5, pady=5, sticky=E)

            self._values[key] = value_field
            row += 1

    def get(self, key: str):
        value: str = self._values[key].get("1.0", "end-1c")
        if not value or value == "None":
            return None
        value = value.strip()
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass
        return value
