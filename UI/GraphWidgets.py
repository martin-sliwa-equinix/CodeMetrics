from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import *
import PyQt5 as QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as
        FigureCanvas)
from matplotlib.pyplot import xlabel, ylabel
import seaborn as sns
import numpy as np
import pandas as pd


# Graph Widget
class MultilineGraphWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        fig = Figure(constrained_layout=True)
        #fig.set_facecolor("blue")
        fig.patch.set_visible(False)
        self.canvas = FigureCanvas(fig)
        self.setStyleSheet("background-color:grey;")

        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0,0,0,0)
        vertical_layout.addWidget(self.canvas)
        
        
        self.axes = self.canvas.figure.add_subplot(111)
        
        #self.axes.patch.set_visible(False)
        self.setLayout(vertical_layout)
        self.layout().addWidget(self.canvas)

        rs = np.random.RandomState(365)
        values = rs.randn(365, 4).cumsum(axis=0)
        dates = pd.date_range("1 1 2016", periods=365, freq="D")
        data = pd.DataFrame(values, dates, columns=["A", "B", "C", "D"])
        data = data.rolling(7).mean()

        sns.set_context("paper")
        plot = sns.lineplot(data=data, ax=self.axes)
        plot.tick_params(colors='red', which='both')
        plot.xaxis.label.set_color('purple')
        plot.yaxis.label.set_color('silver')
        
        self.plot = plot
