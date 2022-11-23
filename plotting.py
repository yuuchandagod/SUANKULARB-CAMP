from pyqtgraph import PlotWidget


class Plotting:

    def __init__(self, graph: PlotWidget):
        self.graph = graph

    def plot(self, pkg, data):
        print('plotting')
        self.graph.clear()
        size_min = min(len(pkg), len(data))
        if size_min > 50:
            self.graph.plot(pkg[-50:], data[0][-50:],
                            {'symbol': 'o', 'symbolSize': 6, 'symbolPen': 'r', 'pen': 'r'})
            self.graph.plot(pkg[-50:], data[1][-50:],
                            {'symbol': 'o', 'symbolSize': 6, 'symbolPen': 'g', 'pen': 'g'})
            self.graph.plot(pkg[-50:], data[2][-50:],
                            {'symbol': 'o', 'symbolSize': 6, 'symbolPen': 'c', 'pen': 'c'})
        else:
            self.graph.plot(pkg[-size_min:], data[-size_min:])
