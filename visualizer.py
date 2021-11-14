from tkinter import Tk, NSEW
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
from tkinter.ttk import Button
from typing import Optional

import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ttkthemes import ThemedStyle

from fancybox import Fancybox
from plot_types import PlotType


class Visualizer(Tk):
    FILETYPES = [
        ("Comma-separated values", "*.csv"),
        ("Tab-separated values", "*.tsv"),
    ]

    def __init__(self, csv: str):
        super().__init__()
        self.title = "Visualizer"
        self.wm_title("Visualizer")
        self.style = ThemedStyle(theme="breeze")
        self.df: Optional[pd.DataFrame] = None
        self.open_button = Button(self, text="Open", command=self.choose_csv)
        self.x_axis = Fancybox(self)
        self.y_axis = Fancybox(self)
        self.classes = Fancybox(self)
        self.scatter_plot_button = Button(self, text="Scatter plot", command=self.plot)
        self.line_plot_button = Button(
            self, text="Line plot", command=lambda: self.plot(plot_type=PlotType.LINE)
        )
        self.histogram_button = Button(
            self,
            text="Histogram",
            command=lambda: self.plot(plot_type=PlotType.HISTOGRAM),
        )
        self.univariate_kde_button = Button(
            self,
            text="Univariate KDE",
            command=lambda: self.plot(plot_type=PlotType.KDE_UNIVARIATE),
        )
        self.bivariate_kde_button = Button(
            self,
            text="Bivariate KDE",
            command=lambda: self.plot(plot_type=PlotType.KDE_BIVARIATE),
        )
        self.linear_regression_button = Button(
            self,
            text="Linear regression plot",
            command=lambda: self.plot(plot_type=PlotType.LINEAR_REGRESSION),
        )
        self.quadratic_regression_button = Button(
            self,
            text="Quadratic regression plot",
            command=lambda: self.plot(plot_type=PlotType.QUADRATIC_REGRESSION),
        )
        self.canvas = FigureCanvasTkAgg(Figure(), self)
        self.load_csv(csv)

    def set_bindings(self):
        self.bind("<Alt-o>", lambda event: self.choose_csv())
        self.bind("<Alt-s>", lambda event: self.plot(PlotType.SCATTER))
        self.bind("<Alt-l>", lambda event: self.plot(PlotType.LINE))
        self.bind("<Alt-h>", lambda event: self.plot(PlotType.HISTOGRAM))
        self.bind("<Alt-u>", lambda event: self.plot(PlotType.KDE_UNIVARIATE))
        self.bind("<Alt-b>", lambda event: self.plot(PlotType.KDE_BIVARIATE))
        self.bind("<Alt-l>", lambda event: self.plot(PlotType.LINEAR_REGRESSION))
        self.bind("<Alt-q>", lambda event: self.plot(PlotType.QUADRATIC_REGRESSION))
        self.bind("<Alt-x>", lambda event: self.x_axis.focus_set())
        self.bind("<Alt-y>", lambda event: self.y_axis.focus_set())
        self.bind("<Alt-c>", lambda event: self.classes.focus_set())

    def run(self):
        self.set_bindings()
        self.draw()
        self.mainloop()

    def draw(self):
        self.columnconfigure(index=(1, 2, 3), weight=1)
        self.rowconfigure(index=(1,), weight=1)
        self.open_button.grid(row=0, column=0, padx=5, pady=5)
        self.x_axis.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)
        self.y_axis.grid(row=0, column=2, padx=5, pady=5, sticky=NSEW)
        self.classes.grid(row=0, column=3, padx=5, pady=5, sticky=NSEW)
        self.scatter_plot_button.grid(row=0, column=4, padx=5, pady=5)
        self.line_plot_button.grid(row=0, column=5, padx=5, pady=5)
        self.histogram_button.grid(row=0, column=6, padx=5, pady=5)
        self.univariate_kde_button.grid(row=0, column=7, padx=5, pady=5)
        self.bivariate_kde_button.grid(row=0, column=8, padx=5, pady=5)
        self.linear_regression_button.grid(row=0, column=9, padx=5, pady=5)
        self.quadratic_regression_button.grid(row=0, column=10, padx=5, pady=5)
        self.canvas.figure.add_subplot(111)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=11, sticky=NSEW)

    def plot(self, plot_type=PlotType.SCATTER):
        x_label = self.x_axis.get()
        if not x_label:
            showerror("Error", "You need to select an x-axis")
            return
        y_label = self.y_axis.get()
        if not y_label and plot_type not in [
            PlotType.HISTOGRAM,
            PlotType.KDE_UNIVARIATE,
        ]:
            showerror("Error", "You need to select an y-axis")
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
            sns.histplot(self.df, x=x_label, hue=classes, ax=plot)
        elif plot_type == PlotType.KDE_UNIVARIATE:
            sns.kdeplot(
                x=x_label, data=self.df, hue=classes, common_norm=False, ax=plot
            )
        elif plot_type == PlotType.KDE_BIVARIATE:
            sns.kdeplot(
                x=x_label,
                y=y_label,
                hue=classes,
                data=self.df,
                ax=plot,
                common_norm=False,
                fill=True,
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
        elif plot_type == PlotType.QUADRATIC_REGRESSION:
            if classes:
                for column_value in self.df[classes].unique():
                    sns.regplot(
                        x=x_label,
                        y=y_label,
                        data=self.df[self.df[classes] == column_value],
                        ax=plot,
                        label=column_value,
                        order=2,
                    )
                    plot.legend(title=classes)
            else:
                sns.regplot(x=x_label, y=y_label, data=self.df, ax=plot, order=2)

        self.canvas.draw()

    def choose_csv(self):
        csv = fd.askopenfilename(filetypes=self.FILETYPES)
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

        headers = list(self.df.columns.values)
        self.x_axis["values"] = self.y_axis["values"] = self.classes["values"] = headers
        self.x_axis.set(headers[0])
        self.y_axis.set(headers[0])
