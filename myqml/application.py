"""
How to run Qt Qml

Examples:
    .. code-block:: python

        if __name__ == "__main__":
            import sys

            # Create an instance of the application
            app = QGuiApplication(sys.argv)

            # Viewer
            viewer = QQuickView()
            engine = viewer.engine()
            engine.addImportPath(current_path)

            # Create an object
            dataSource = DataSource(viewer)

            # And register it in the context of QML
            viewer.rootContext().setContextProperty("dataSource", dataSource)

            # Load the qml file into the engine
            qml_file = os.path.join(current_path, 'main.qml')
            viewer.setSource(QtCore.QUrl.fromLocalFile(qml_file))
            viewer.setResizeMode(QQuickView.SizeRootObjectToView)
            viewer.setColor(QColor("#404040"))
            viewer.show()

            engine.quit.connect(app.quit)
            sys.exit(app.exec_())

    Another alternative

    .. code-block:: python

        if __name__ == "__main__":
            import sys

            # Create an instance of the application
            app = QGuiApplication(sys.argv)

            # Create QML engine
            engine = QQmlApplicationEngine()

            # Create a calculator object
            dataSource = DataSource()

            # And register it in the context of QML
            engine.rootContext().setContextProperty("dataSource", dataSource)

            # Load the qml file into the engine
            engine.load("main.qml")

            engine.quit.connect(app.quit)
            sys.exit(app.exec_())
"""
import sys

from myqml.qt import QtGui, QtQml, QtQuick, QtWidgets
from myqml.debug import Debugger


class Interface(object):
    """Run a qml application

    Example:
        .. code-block:: python

            with Application(debug=True) as app:
                app.load('main.qml')
    """
    DEBUGGER_CLASS = Debugger

    def __init__(self, args=None, debug=False):
        if args is None:
            args = sys.argv

        self.args = args
        self.engine = None
        self.debugger = None

        if debug:
            self.debugger = self.DEBUGGER_CLASS()

        super().__init__(self.args)

        self.create_engine()

    def create_engine(self):
        """Create and set the application engine."""
        raise NotImplementedError

    def __enter__(self, *args, **kwargs):
        """Enter the `with` statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """If no errors occurred in the with statement run the application.exec_()."""
        # Check if an error occurred
        if exc_type is not None:
            return False

        self.engine.quit.connect(self.quit)
        self.exec_()  # Run the event loop just before exiting the with statement
        return True

    # ===== Engine methods =====
    def addImportPath(self, dir):
        """Add a QML import path."""
        self.engine.addImportPath(dir)

    def rootContext(self):
        """Get the root engine context."""
        try:
            return self.engine.rootContext()
        except AttributeError:
            return None

    def load(self, filePath):
        """Load the source qml file by calling "engine.load"."""
        self.engine.load(filePath)


class QmlApplication(Interface, QtGui.QGuiApplication):
    """Run a qml application.

    Warning:
        This type of application may not work with QtCharts. QtCharts may only work with the widget viewer application.

    Example:
        .. code-block:: python

            with Application(debug=True) as app:
                app.load('main.qml')
    """
    def create_engine(self):
        """Create and set the application engine."""
        self.engine = QtQml.QQmlApplicationEngine()


class ViewerApplication(Interface, QtWidgets.QApplication):
    def __init__(self, args=None, debug=False):
        self.viewer = None
        Interface.__init__(self, args=args, debug=debug)

    def create_engine(self):
        """Create and set the application engine."""
        self.viewer = QtQuick.QQuickView()
        self.viewer.setResizeMode(self.viewer.SizeRootObjectToView)
        self.engine = self.viewer.engine()

    def rootContext(self):
        """Get the root engine context."""
        try:
            return self.viewer.rootContext()
        except AttributeError:
            return None

    def load(self, filePath):
        """Load the source qml file by setting the viewer source.."""
        self.viewer.setSource(filePath)
        self.viewer.show()
