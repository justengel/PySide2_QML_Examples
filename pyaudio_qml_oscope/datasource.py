from myqml import QtCore, QtCharts

import time
import random
import math
import threading
import pyaudio
import numpy as np
import np_rw_buffer


class DataSource(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.m_index = -1
        self.m_data = []

        self.generateData(0, 5, 1024)

    @QtCore.Slot(QtCharts.QXYSeries)
    def update(self, series):
        if not series or len(self.m_data) == 0:
            return

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
        # self.m_data = [[self._gen_dat(type_, row, col) for row in range(rowCount)] for col in range(colCount)]
        self.m_data = [[self._gen_dat(type_, row, col) for col in range(colCount)] for row in range(rowCount)]


# NEED to Fix this in np_rw_buffer
# (move_start should be True unless you are calling read() and want to keep track of how far behind you are)
class AudioBuffer(np_rw_buffer.AudioFramingBuffer):
    def _write(self, data, length, error, move_start=True):
        super()._write(data, length, error, move_start=move_start)


class AudioSource(DataSource):

    FLOAT32 = pyaudio.paFloat32
    INT32 = pyaudio.paInt32
    INT16 = pyaudio.paInt16

    ABORT = pyaudio.paAbort
    CONTINUE = pyaudio.paContinue

    secondsChanged = QtCore.Signal()
    sampleRateChanged = QtCore.Signal()
    channelsChanged = QtCore.Signal()

    def __init__(self, sample_rate, channels, seconds=1, chunk=None, fmt=FLOAT32, parent=None):
        self.stream = None
        self.pa = None
        self.lock = None
        super().__init__(parent)

        self.lock = threading.RLock()
        self._sample_rate = sample_rate
        self._channels = channels
        self._seconds = seconds
        self._chunk = chunk
        self.fmt = fmt

        # self.buffer = np.zeros(shape=(int(self.get_seconds() * self.get_sample_rate()), self.get_channels()),
        #                        dtype=self.get_dtype())
        self.buffer = AudioBuffer(sample_rate=self.get_sample_rate(), seconds=self.get_seconds(),
                                  channels=self.get_channels())
        self.buffer_changed = False
        self.m_data = []  # Clear data

    # ========== Data Source API ==========
    @QtCore.Slot(QtCharts.QXYSeries, QtCharts.QXYSeries, QtCharts.QXYSeries, QtCharts.QXYSeries, QtCharts.QXYSeries)
    @QtCore.Slot(QtCharts.QXYSeries, QtCharts.QXYSeries, QtCharts.QXYSeries, QtCharts.QXYSeries)
    @QtCore.Slot(QtCharts.QXYSeries, QtCharts.QXYSeries, QtCharts.QXYSeries)
    @QtCore.Slot(QtCharts.QXYSeries, QtCharts.QXYSeries)
    @QtCore.Slot(QtCharts.QXYSeries)
    @QtCore.Slot()
    def update(self, *series):
        if not series or len(self.buffer) <= 1:
            return

        if self.buffer_changed:
            # Lock for thread safe
            with self.lock:
                # data = self.buffer.copy()
                data = self.buffer.get_data()
                self.buffer_changed = False

            # Create the points
            sample_rate = self.get_sample_rate()
            channels = self.get_channels()
            points = [[QtCore.QPointF(row / sample_rate, data[row, col]) for row in range(len(data))]
                      for col in range(channels)]
            self.m_data = points

            # ===== Plot the data =====
            pts = self.m_data
            for i, ser in enumerate(series):
                ser.replace(pts[i])

    def stream_audio(self, in_data, frame_count, time_info, status):
        """Callback function for pyaudio to run without blocking."""
        channels = self.get_channels()
        seconds = self.get_seconds()
        sample_rate = self.get_sample_rate()
        samples = int(seconds * sample_rate)

        # Format the bytes to a numpy array
        data = self.format_data(in_data, channels, self.fmt)

        # Lock for thread safe
        with self.lock:
            # Rolling buffer (Yes very inefficient)
            # self.buffer = np.append(self.buffer, data, axis=0)
            # if len(self.buffer) > samples:
            #     self.buffer = self.buffer[-samples:]
            self.buffer.write(data, error=False)
            self.buffer_changed = True

        return in_data, self.CONTINUE

    # ========== Qt Audio API ==========
    @QtCore.Slot(result=float)
    def get_seconds(self):
        return self._seconds

    @QtCore.Slot(float)
    @QtCore.Slot(int)
    @QtCore.Slot(str)
    def set_seconds(self, seconds):
        if isinstance(seconds, str):
            try:
                seconds = int(seconds)
            except:
                seconds = float(seconds)
        self._seconds = abs(seconds)
        # self.buffer = np.zeros(shape=(int(self.get_seconds() * self.get_sample_rate()), self.get_channels()),
        #                        dtype=self.get_dtype())
        self.buffer.seconds = self.get_seconds()
        if self.is_running():
            self.stop()
            self.start()

    seconds = QtCore.Property(float, get_seconds, set_seconds, notify=secondsChanged)

    @QtCore.Slot(result=float)
    def get_sample_rate(self):
        return self._sample_rate

    @QtCore.Slot(float)
    @QtCore.Slot(int)
    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate
        # self.buffer = np.zeros(shape=(int(self.get_seconds() * self.get_sample_rate()), self.get_channels()),
        #                        dtype=self.get_dtype())
        self.buffer.sample_rate = self.get_sample_rate()
        if self.is_running():
            self.stop()
            self.start()

    sample_rate = QtCore.Property(float, get_sample_rate, set_sample_rate, notify=sampleRateChanged)

    @QtCore.Slot(result=int)
    def get_channels(self):
        return self._channels

    @QtCore.Slot(int)
    def set_channels(self, channels):
        self._channels = channels
        # self.buffer = np.zeros(shape=(int(self.get_seconds() * self.get_sample_rate()), self.get_channels()),
        #                        dtype=self.get_dtype())
        self.buffer.channels = self.get_channels()
        if self.is_running():
            self.stop()
            self.start()

    channels = QtCore.Property(int, get_channels, set_channels, notify=channelsChanged)

    @QtCore.Slot(result=bool)
    def is_running(self):
        """Return if the audio stream is running."""
        return self.stream is not None

    @QtCore.Slot()
    @QtCore.Slot(bool)
    def start(self, blocking=False):
        """Start the audio stream. If blocking is False run with the callback "stream_audio"."""
        if self.pa is None:
            self.pa = pyaudio.PyAudio()

        callback = None
        if not blocking:
            callback = self.stream_audio

        self.stream = self.pa.open(format=self.fmt, channels=int(self.get_channels()), rate=int(self.get_sample_rate()),
                                   input=True, frames_per_buffer=self.chunk, stream_callback=callback)

    @QtCore.Slot()
    def stop(self):
        """Stop the audio stream."""
        stream, self.stream = self.stream, None
        try:
            stream.stop_stream()
            stream.close()
        except:
            pass

    @QtCore.Slot()
    def close(self):
        """Stop the audio stream and close pyaudio."""
        self.stop()
        try:
            self.pa.terminate()
        except:
            pass
        self.pa = None

    # ========== Audio Properties ==========
    @property
    def chunk(self):
        if self._chunk is None:
            return AudioSource.calculate_samples_per_buffer(self.sample_rate)  # 1024
        return self._chunk

    @chunk.setter
    def chunk(self, value):
        self._chunk = value

    def read(self, amount=None):
        """Read the amount of samples and return a numpy array."""
        if amount is None:
            amount = self.chunk
            print(amount)
        return self.format_data(self.stream.read(amount), self.channels, self.fmt)

    @staticmethod
    def dtype_from_fmt(fmt):
        if fmt == pyaudio.paFloat32:
            dtype = np.dtype('|f4')
        elif fmt == pyaudio.paInt32:
            dtype = np.dtype('|i4')
        elif fmt == pyaudio.paInt16:
            dtype = np.dtype('|i2')
        elif fmt == pyaudio.paInt8:
            dtype = np.dtype('|i1')
        else:
            dtype = np.dtype('|f4')
        return dtype

    def get_dtype(self):
        return self.dtype_from_fmt(self.fmt)

    @staticmethod
    def format_data(data, channels, fmt):
        dtype = AudioSource.dtype_from_fmt(fmt)
        return np.frombuffer(data, dtype=dtype).reshape((-1, channels))

    @staticmethod
    def calculate_samples_per_buffer(sample_rate, update_rate=60):
        """Calculate and return the optimal samples per buffer (60 Hz of the sample rate).
        Args:
            sample_rate (float/int): Sample rate of the data
            update_rate (int): How fast to update in Hz. (60 is 60 times per second).
        Returns:
            samples_per_buffer (int): Power of 2 for the number of samples closest to the update rate.
        """
        size = sample_rate // update_rate
        if size < 32:
            return 32
        return size
        # # Force nearest power of two
        # size = max(sample_rate // update_rate, 32)
        # size = pow(2, int(np.log2(size)))  # round(np.log2(size)))
        # return int(size)
