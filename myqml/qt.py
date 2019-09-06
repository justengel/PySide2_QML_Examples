from PySide2 import QtCore, QtGui, QtHelp, QtMultimedia, QtNetwork, QtOpenGL, QtPrintSupport, QtSql, QtSvg, \
    QtTest, QtWidgets, QtXmlPatterns

try:
    from PySide2.QtCharts import QtCharts
except:
    QtCharts = None

try:
    from qtpy import QtLocation, QtMultimediaWidgets, QtQml, QtQuick, QtQuickWidgets, QtWebChannel, QtWebSockets
except (ImportError, Exception):
    QtLocation = None
    QtMultimediaWidgets = None
    QtQml = None
    QtQuick = None
    QtQuickWidgets = None
    QtWebChannel = None
    QtWebSockets = None


__all__ = ['API', 'API_NAME',
           'QtCore', 'QtGui', 'QtHelp', 'QtMultimedia', 'QtNetwork', 'QtOpenGL', 'QtPrintSupport',
           'QtSql', 'QtSvg', 'QtTest', 'QtWidgets', 'QtXmlPatterns', 'QtCharts',
           'QtLocation', 'QtMultimediaWidgets', 'QtQml', 'QtQuick', 'QtQuickWidgets', 'QtWebChannel', 'QtWebSockets']


API = 'pyside2'
API_NAME = 'PySide2'
