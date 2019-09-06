from myqml import QtCore, QtCharts

import random
import math


class DataSource(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.m_index = -1
        self.m_data = []

        self.generateData(0, 5, 1024)

    @QtCore.Slot(QtCharts.QXYSeries)
    def update(self, series):
        if series:
            # Column index
            self.m_index += 1
            if self.m_index > len(self.m_data) - 1:
                self.m_index = 0

            points = self.m_data[self.m_index]
            series.replace(points)

    def _gen_dat(self, type_, row, col):
        if type_ == 0 or type_ == 'sin':
            y = math.sin(math.pi / 50 * col) + 0.5 + random.random()
            x = col
        else:
            y = row / 10
            x = col
        return QtCore.QPointF(x, y)

    @QtCore.Slot(int, int, int)
    @QtCore.Slot(str, int, int)
    def generateData(self, type_, rowCount, colCount):
        # rowCount is really the channel count and colCount is really the number of samples
        self.m_data = [[self._gen_dat(type_, row, col) for col in range(colCount)] for row in range(rowCount)]
