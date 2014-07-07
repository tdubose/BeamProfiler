import cv2
import numpy
 
from PyQt4 import QtCore
 
class CameraDevice(QtCore.QObject):
 
    _DEFAULT_FPS = 30
 
    newFrame = QtCore.pyqtSignal(numpy.ndarray)
 
    def __init__(self, cameraId=0, mirrored=False, parent=None):
        super(CameraDevice, self).__init__(parent)
 
        self.mirrored = mirrored
 
        self._cameraDevice = cv2.VideoCapture(cameraId)
 
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(1000/self.fps)
 
        self.paused = False

 
    @QtCore.pyqtSlot()
    def _queryFrame(self):
        frame = self._cameraDevice.read()[1]
        if self.mirrored:
            frame = cv2.flip(frame,1)
        self.newFrame.emit(frame)
 
    @property
    def paused(self): # >> cameraDevice.paused -> True/False
        return not self._timer.isActive()
 
    @paused.setter # >> cameraDevice.paused = True/False
    def paused(self, p):
        if p:
            self._timer.stop()
        else:
            self._timer.start()
 
    @property
    def frameSize(self):
        w = self._cameraDevice.get(3) # 3 = width (DC 1394 properties, check https://github.com/Itseez/opencv/blob/0b4534d4c95556ba99878505130f12b32d588666/modules/highgui/include/opencv2/highgui.hpp)
        h = self._cameraDevice.get(4) # 4 = height
        return int(w), int(h)

 
    @property
    def fps(self):
        fps = int(self._cameraDevice.get(5)) # 5 = FPS
        if not fps > 0:
            fps = self._DEFAULT_FPS
        return fps
		
	@property
	def exposure(self):
		self._cameraDevice.set(15, 4.5)# 15 = exposure
	
	@property
	def gain(self):
		self._cameraDevice.set(14, 0.0)# 14 = gain