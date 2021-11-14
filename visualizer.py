from json import JSONDecodeError
from numbers import Number
from tkinter import Tk, NSEW, Menu
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo
from tkinter.ttk import Button
from typing import Optional

import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ttkthemes import ThemedStyle

from fancybox import Fancybox
from plot_types import PlotType
from settings import Settings
from settings_panel import SettingsPanel


class Visualizer(Tk):
    TITLE = "Visualizer"
    CSV_FILETYPES = [
        ("Comma-separated values", "*.csv"),
        ("Tab-separated values", "*.tsv"),
    ]
    IMAGE_FILETYPES = ["png", "pdf", "jpg", "jpeg", "svg", "eps"]

    def __init__(self, csv: str):
        super().__init__()
        self.csv = csv
        self.settings = None
        self.settings_panel = None
        self.load_settings()
        self.wm_title(self.TITLE)
        self.style = ThemedStyle(theme="breeze")
        self.df: Optional[pd.DataFrame] = None
        self.x_axis = Fancybox(self)
        self.y_axis = Fancybox(self)
        self.classes = Fancybox(self)
        self.scatter_plot_button = Button(self, text="Scatter plot (Alt+S)", command=self.try_to_plot)
        self.line_plot_button = Button(
            self, text="Line plot", command=lambda: self.try_to_plot(plot_type=PlotType.LINE)
        )
        self.histogram_button = Button(
            self,
            text="Histogram (Alt+H)",
            command=lambda: self.try_to_plot(plot_type=PlotType.HISTOGRAM),
        )
        self.univariate_kde_button = Button(
            self,
            text="Univariate KDE (Alt+U)",
            command=lambda: self.try_to_plot(plot_type=PlotType.KDE_UNIVARIATE),
        )
        self.bivariate_kde_button = Button(
            self,
            text="Bivariate KDE (Alt+B)",
            command=lambda: self.try_to_plot(plot_type=PlotType.KDE_BIVARIATE),
        )
        self.linear_regression_button = Button(
            self,
            text="Linear regression plot (Alt+L)",
            command=lambda: self.try_to_plot(plot_type=PlotType.LINEAR_REGRESSION),
        )
        self.quadratic_regression_button = Button(
            self,
            text="Polynomial regression plot (Alt+P)",
            command=lambda: self.try_to_plot(plot_type=PlotType.POLYNOMIAL_REGRESSION),
        )
        self.canvas = FigureCanvasTkAgg(Figure(), self)
        self.load_csv(csv)

    def load_settings(self, path="settings.json", show_confirmation=False):
        if not path:
            path = fd.askopenfilename()
        if not path:
            return
        if not self.settings:
            self.settings = Settings()
        if not self.settings_panel:
            self.settings_panel = SettingsPanel(self, self.settings)
        try:
            self.settings.reload(path)
            self.settings_panel.add_fields()
        except JSONDecodeError:
            showerror("Error", "Invalid settings file: " + path)
            return
        if show_confirmation:
            showinfo("Visualizer", "Settings loaded")

    def set_bindings(self):
        self.bind("<Control-o>", lambda event: self.choose_csv())
        self.bind("<Control-s>", lambda event: self.save())
        self.bind("<Control-S>", lambda event: self.edit_settings())
        self.bind("<Alt-s>", lambda event: self.try_to_plot(PlotType.SCATTER))
        self.bind("<Alt-l>", lambda event: self.try_to_plot(PlotType.LINE))
        self.bind("<Alt-h>", lambda event: self.try_to_plot(PlotType.HISTOGRAM))
        self.bind("<Alt-u>", lambda event: self.try_to_plot(PlotType.KDE_UNIVARIATE))
        self.bind("<Alt-b>", lambda event: self.try_to_plot(PlotType.KDE_BIVARIATE))
        self.bind("<Alt-l>", lambda event: self.try_to_plot(PlotType.LINEAR_REGRESSION))
        self.bind("<Alt-p>", lambda event: self.try_to_plot(PlotType.POLYNOMIAL_REGRESSION))
        self.bind("<Alt-x>", lambda event: self.x_axis.focus_set())
        self.bind("<Alt-y>", lambda event: self.y_axis.focus_set())
        self.bind("<Alt-c>", lambda event: self.classes.focus_set())

    def run(self):
        self.set_bindings()
        self.draw()
        self.mainloop()

    def create_menu_bar(self):
        menu = Menu(self)
        file_menu = Menu(menu, tearoff=0)
        settings_menu = Menu(menu, tearoff=0)

        file_menu.add_command(label="Open", command=self.choose_csv)
        file_menu.add_command(label="Save as...", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        settings_menu.add_command(label="Save", command=self.save_settings)
        settings_menu.add_command(
            label="Load", command=lambda: self.load_settings(None, True)
        )
        settings_menu.add_command(
            label="Reset defaults", command=self.reset_settings
        )

        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="Settings", menu=settings_menu)

        self.config(menu=menu)

    def reset_settings(self):
        self.settings.define_defaults()
        self.settings_panel.add_fields()

    def save_settings(self):
        path = fd.asksaveasfilename(initialfile="settings.json")
        for key in self.settings:
            self.settings[key] = self.settings_panel.get(key)
        self.settings.save(path)
        showinfo(self.TITLE, "Settings saved")

    def draw(self):
        self.create_menu_bar()
        self.columnconfigure(index=(0, 1, 2), weight=1)
        self.rowconfigure(index=(1,), weight=1)
        self.x_axis.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        self.y_axis.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)
        self.classes.grid(row=0, column=2, padx=5, pady=5, sticky=NSEW)
        self.scatter_plot_button.grid(row=0, column=3, padx=5, pady=5)
        self.line_plot_button.grid(row=0, column=4, padx=5, pady=5)
        self.histogram_button.grid(row=0, column=5, padx=5, pady=5)
        self.univariate_kde_button.grid(row=0, column=6, padx=5, pady=5)
        self.bivariate_kde_button.grid(row=0, column=7, padx=5, pady=5)
        self.linear_regression_button.grid(row=0, column=8, padx=5, pady=5)
        self.quadratic_regression_button.grid(row=0, column=9, padx=5, pady=5)
        self.canvas.figure.add_subplot(111)
        self.canvas.draw()
        self.settings_panel.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
        self.canvas.get_tk_widget().grid(
            row=1, column=1, columnspan=9, padx=5, pady=5, sticky=NSEW
        )

    def try_to_plot(self, plot_type=PlotType.SCATTER):
        try:
            self.plot(plot_type)
        except Exception as e:
            showerror("Error", str(e))
            raise

    def plot(self, plot_type=PlotType.SCATTER):
        x_label = self.x_axis.get()
        if not x_label:
            showerror("Error", "You need to select an x-axis")
            return
        if x_label not in self.df.columns:
            showerror("Error", "Invalid x column")
            return
        y_label = self.y_axis.get()
        if plot_type not in [PlotType.HISTOGRAM, PlotType.KDE_UNIVARIATE]:
            if not y_label:
                showerror("Error", "You need to select an y-axis")
                return
            if y_label not in self.df.columns:
                showerror("Error", "Invalid y column")
                return
        if x_label == y_label and plot_type == PlotType.KDE_BIVARIATE:
            showerror("Error", "Bivariate KDE cannot be run with x=y")
            return
        classes = self.classes.get()
        classes = classes if classes else None

        plot = self.canvas.figure.get_axes()[0]
        plot.cla()  # Clear axis

        if plot_type == PlotType.LINE:
            sns.lineplot(x=x_label, y=y_label, data=self.df, hue=classes, ax=plot)
        elif plot_type == PlotType.SCATTER:
            sns.scatterplot(x=x_label, y=y_label, data=self.df, hue=classes, ax=plot)
        elif plot_type == PlotType.HISTOGRAM:
            sns.histplot(
                self.df,
                x=x_label,
                hue=classes,
                ax=plot,
                bins=self.settings_panel.get(Settings.BINS),
            )
        elif plot_type == PlotType.KDE_UNIVARIATE:
            bw_adjust = self.settings_panel.get(Settings.BW_FACTOR)
            if not isinstance(bw_adjust, Number):
                raise ValueError(Settings.BW_FACTOR + " must be a number")
            sns.kdeplot(
                x=x_label,
                data=self.df,
                hue=classes,
                common_norm=self.settings_panel.get(Settings.COMMON_NORMALIZATION),
                ax=plot,
                bw_adjust=bw_adjust,
            )
        elif plot_type == PlotType.KDE_BIVARIATE:
            sns.kdeplot(
                x=x_label,
                y=y_label,
                hue=classes,
                data=self.df,
                ax=plot,
                common_norm=self.settings_panel.get(Settings.COMMON_NORMALIZATION),
                fill=True,
                bw_adjust=self.settings_panel.get(Settings.BW_FACTOR),
            )
        elif plot_type == PlotType.LINEAR_REGRESSION:
            if classes:
                for column_value in self.df[classes].unique():
                    sns.regplot(
                        x=x_label,
                        y=y_label,
                        data=self.df[self.df[classes] == column_value],
                        ax=plot,
                        label=column_value,
                    )
                    plot.legend(title=classes)
            else:
                sns.regplot(x=x_label, y=y_label, data=self.df, ax=plot)
        elif plot_type == PlotType.POLYNOMIAL_REGRESSION:
            if classes:
                for column_value in self.df[classes].unique():
                    sns.regplot(
                        x=x_label,
                        y=y_label,
                        data=self.df[self.df[classes] == column_value],
                        ax=plot,
                        label=column_value,
                        order=self.settings_panel.get(Settings.POLYNOMIAL_DEGREE),
                        ci=self.settings_panel.get(Settings.CONFIDENCE_INTERVAL),
                    )
                    plot.legend(title=classes)
            else:
                sns.regplot(
                    x=x_label,
                    y=y_label,
                    data=self.df,
                    ax=plot,
                    order=self.settings_panel.get(Settings.POLYNOMIAL_DEGREE),
                    ci=self.settings_panel.get(Settings.CONFIDENCE_INTERVAL),
                )

        plot.set_title(self.csv)
        self.canvas.draw()

    def save(self):
        image: str = fd.asksaveasfilename()
        if not image:
            return
        for extension in self.IMAGE_FILETYPES:
            if image.endswith(extension):
                break
        else:
            showerror(
                "Error",
                f"Output file does not have a valid extension. "
                f"Possible options are: {', '.join(self.IMAGE_FILETYPES)}.",
            )
        self.canvas.figure.savefig(image)

    def choose_csv(self):
        csv = fd.askopenfilename(filetypes=self.CSV_FILETYPES)
        self.load_csv(csv)

    def load_csv(self, csv: str):
        if not csv:
            return
        if csv.endswith(".csv"):
            self.df = pd.read_csv(csv)
        elif csv.endswith(".tsv"):
            self.df = pd.read_csv(csv, sep="\t")
        else:
            showerror("Error", "Invalid file extension")
            return
        self.csv = csv

        headers = list(self.df.columns.values)
        self.x_axis["values"] = self.y_axis["values"] = self.classes["values"] = headers
        self.x_axis.set(headers[0])
        self.y_axis.set(headers[0])
