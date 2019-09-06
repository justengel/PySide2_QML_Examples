import sys
from .qt import QtCore, QtQml


class Debugger(QtQml.QQmlDebuggingEnabler):
    """Help debug qml messages.

    Example:
        .. code-block:: python

            >>> Debugger.enable()

    """
    DEBUG_ENABLER = None

    def __init__(self):
        super().__init__()
        self.__class__.DEBUG_ENABLER = self
        QtCore.qInstallMessageHandler(self.message_handler)

    @staticmethod
    def message_handler(mode, context, message):
        if mode == QtCore.QtInfoMsg:
            mode = 'Info'
        elif mode == QtCore.QtWarningMsg:
            mode = 'Warning'
        elif mode == QtCore.QtCriticalMsg:
            mode = 'critical'
        elif mode == QtCore.QtFatalMsg:
            mode = 'fatal'
        else:
            mode = 'Debug'
        print("%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file),
              file=sys.stderr)

    @classmethod
    def enable(cls):
        """Create the debug enabler and setup the message handler.

        Returns:
            DEBUG_ENABLER (QtQml.QQmlDebuggingEnabler): The debug enabler.
        """
        cls.DEBUG_ENABLER = cls()
        QtCore.qInstallMessageHandler(cls.DEBUG_ENABLER.message_handler)
        return cls.DEBUG_ENABLER
