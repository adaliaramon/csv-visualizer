from tkinter.ttk import Combobox


class Fancybox(Combobox):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.bind("<Control-n>", lambda event: self.select(+1))
        self.bind("<Control-N>", lambda event: self.select(-1))

    def select(self, delta: int):
        values = self["values"]
        index = values.index(self.get())
        new_index = (index + delta) % len(values)
        self.set(values[new_index])
