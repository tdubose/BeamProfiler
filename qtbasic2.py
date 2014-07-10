#!/usr/local/bin/python
# encoding: utf-8
import sys
from PyQt4 import QtGui, QtCore
from ui_profilewindow import Ui_ProfileWindow
from ui_cameraview import Ui_CameraView
from ui_setup import Ui_Setup
from camerawidget import CameraWidget
from cameradevice import CameraDevice
from opencvqimage import OpenCVQImage
from shot202 import Shot202
import time
import cv2
from cameradevice import *

class MW(QtGui.QMainWindow):
	
	def __init__(self,_cameraDevice):
		super(MW, self).__init__()
		self.ui = Ui_ProfileWindow()
		self.ui.setupUi(self)
		self.show()
		self.cameraDevice = _cameraDevice
		self.profRange = (0.0,100.0)
		self.controller = Shot202("COM3")
		
	def openCameraWindow(self):
		self.cw = CameraWidget(self.cameraDevice)
		self.cw.show()
		
	def openSetupDialog(self):
		self.sd = SD(self.profRange, self.cameraDevice.exposure, self.cameraDevice.gain)
		self.sd.show()
		self.sd.newRange.connect(self.updatePos)
		self.sd.newExposure.connect(self.updateExposure)
		self.sd.newGain.connect(self.updateGain)
		
	def updatePos(self, newRange):
		self.profRange = newRange
		print self.profRange
	
	def updateExposure(self, newExposure):
		#print self.cameraDevice.fps
		print self.cameraDevice.exposure
		self.cameraDevice.exposure = float(newExposure)#float(newExposure))
		print self.cameraDevice.exposure
	
	def updateGain(self, newGain):
		print self.cameraDevice.fps
		print self.cameraDevice.gain
		self.cameraDevice.gain = float(newGain)
		print self.cameraDevice.gain
		
	def startProfile(self):
		self.profRangeStart_Pulse = int(self.profRange[0]*100)
		self.profRangeStop_Pulse = int(self.profRange[1]*100)
		CurrentPos = int(self.controller.getpos(inpulses=True))#returns absolute location in pulses
		self.controller.go(self.profRangeStart_Pulse)
		time.sleep((abs(CurrentPos-self.profRangeStart_Pulse)/4500) + 2)
		#Live Camera View appears to be paused because the entire program is stopped with time.sleep.
		print "Image one about to be taken"
		self.imgPos1 = self.cameraDevice._cameraDevice.read()
		cv2.imwrite("testImgPos1.png", self.imgPos1[1])
		print "Image one written, stage about to move to position 2"
		CurrentPos2 = int(self.controller.getpos(inpulses=True))
		self.controller.go(self.profRangeStop_Pulse)
		time.sleep((abs(CurrentPos2-self.profRangeStop_Pulse)/4500) + 2)
		print "Image two about to be taken"
		self.imgPos2 = self.cameraDevice._cameraDevice.read()
		cv2.imwrite("testImgPos2.png", self.imgPos2[1])
		print "End of start profile"

class SD(QtGui.QDialog):
	
	newRange = QtCore.pyqtSignal(tuple)
	newExposure = QtCore.pyqtSignal(int)
	newGain = QtCore.pyqtSignal(int)
	
	def __init__(self,profRange, exposure, gain):
		super(SD, self).__init__()
		self.ui = Ui_Setup()
		self.ui.setupUi(self)
		
		# Set controls equal to extant values
		self.ui.lineEdit.setText(str(profRange[0]))
		self.ui.lineEdit_2.setText(str(profRange[1]))
		self.oldRange = profRange
		
		self.ui.horizontalSlider.setValue(exposure)
		self.oldExposure = exposure
		self.ui.horizontalSlider_2.setValue(gain)
		self.oldGain = gain
		#Range of Start to Stop must be between 0.00 and 790.00"
		
	def accept(self):   
		try:
			newrange = (float(self.ui.lineEdit.text()),float(self.ui.lineEdit_2.text()))
			newexposure = (self.ui.horizontalSlider.value())
			newgain = (self.ui.horizontalSlider_2.value())
		except Exception, e:
			raise e
			newrange = self.oldRange
			newexposure = self.oldExposure
			newgain = self.oldGain
		finally:
			self.newRange.emit(newrange)
			self.newExposure.emit(newexposure)
			self.newGain.emit(newgain)
			self.close()

def main():	
	app = QtGui.QApplication(sys.argv)
	cameraDevice = CameraDevice(mirrored = True)
	mw = MW(cameraDevice)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()