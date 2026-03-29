from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class ChartUtils:

    @staticmethod
    def create_bar_chart(categories, values, title, xlabel, ylabel):

        figure = Figure()
        canvas = FigureCanvas(figure)

        ax = figure.add_subplot(111)

        ax.bar(categories, values)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        figure.tight_layout()

        return canvas


    @staticmethod
    def create_line_chart(x_data, y_data, title, xlabel, ylabel):

        figure = Figure()
        canvas = FigureCanvas(figure)

        ax = figure.add_subplot(111)

        ax.plot(x_data, y_data, marker="o")

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        figure.tight_layout()

        return canvas