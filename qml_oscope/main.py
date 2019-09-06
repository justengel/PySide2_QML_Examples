import os
import sys
import myqml
from myqml import QtCore, QtGui, QtCharts

from qml_oscope.datasource import DataSource


if __name__ == "__main__":
    with myqml.ViewerApplication(debug=True) as app:
        # Register the dataSource in the context of QML
        data_source = DataSource()
        app.rootContext().setContextProperty("dataSource", data_source)

        app.viewer.setColor(QtGui.QColor("#404040"))
        app.load('main.qml')

    print('Application Closed!')


# def qt_message_handler(mode, context, message):
#     if mode == QtCore.QtInfoMsg:
#         mode = 'Info'
#     elif mode == QtCore.QtWarningMsg:
#         mode = 'Warning'
#     elif mode == QtCore.QtCriticalMsg:
#         mode = 'critical'
#     elif mode == QtCore.QtFatalMsg:
#         mode = 'fatal'
#     else:
#         mode = 'Debug'
#     print("%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file),
#           file=sys.stderr)
#
#
# if __name__ == "__main__":
#     import sys
#
#     # Print QML Debug messages to stderr
#     QtCore.qInstallMessageHandler(qt_message_handler)
#     debug = QQmlDebuggingEnabler()
#
#     # Create an instance of the application
#     app = QGuiApplication(sys.argv)
#
#     # Viewer
#     viewer = QQuickView()
#     engine = viewer.engine()
#     engine.addImportPath(current_path)
#
#     # Create an object
#     dataSource = DataSource(viewer)
#
#     # And register it in the context of QML
#     viewer.rootContext().setContextProperty("dataSource", dataSource)
#
#     # Load the qml file into the engine
#     qml_file = os.path.join(current_path, 'main.qml')
#     viewer.setSource(QtCore.QUrl.fromLocalFile(qml_file))
#     viewer.setResizeMode(QQuickView.SizeRootObjectToView)
#     viewer.setColor(QColor("#404040"))
#     viewer.show()
#
#     engine.quit.connect(app.quit)
#     sys.exit(app.exec_())
