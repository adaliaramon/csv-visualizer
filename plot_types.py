from enum import auto
from enum import Enum


class PlotType(Enum):
    SCATTER = auto()
    LINE = auto()
    HISTOGRAM = auto()
    KDE_UNIVARIATE = auto()
    KDE_BIVARIATE = auto()
    LINEAR_REGRESSION = auto()
    POLYNOMIAL_REGRESSION = auto()
