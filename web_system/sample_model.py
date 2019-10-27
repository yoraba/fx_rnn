# coding utf-8
import matplotlib.pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
import random

class SampleModel:
    def get_dummy_graph(self):
        fig, ax = matplotlib.pyplot.subplots()
        ax.set_title(u'IMINASHI GRAPH')
        x_ax = range(1, 284)
        y_ax = [x * random.randint(436, 875) for x in x_ax]
        ax.plot(x_ax, y_ax)

        canvas = FigureCanvasAgg(fig)
        buf = BytesIO()
        canvas.print_png(buf)
        data = buf.getvalue()
        return data