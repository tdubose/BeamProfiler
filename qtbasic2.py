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
import visa



class MW(QtGui.QMainWindow):
	
	def __init__(self,_cameraDevice):
		super(MW, self).__init__()
		self.ui = Ui_ProfileWindow()
		self.ui.setupUi(self)
		self.show()
		self.cameraDevice = _cameraDevice
		#self.connect(self, QtCore.SIGNAL("updatePos"),self.updatePos)
		self.profRange = (0.0,100.0)
		
	def openCameraWindow(self):
		self.cw = CameraWidget(self.cameraDevice)
		self.cw.show()
		
	def openSetupDialog(self):
		self.sd = SD(self.profRange)
		self.sd.show()
		self.sd.newRange.connect(self.updatePos)
		
	def updatePos(self, newRange):
		self.profRange = newRange
		print self.profRange
		
	def startProfile(self):
		self.rm = visa.ResourceManager()
		self.controller = self.rm.get_instrument("COM3")

		self.controller.ask("P:R")
		self.controller.ask("P:S")

				
				
class SD(QtGui.QDialog):
	
	newRange = QtCore.pyqtSignal(tuple)
	
	def __init__(self,profRange):
		super(SD, self).__init__()
		self.ui = Ui_Setup()
		self.ui.setupUi(self)
		self.ui.lineEdit.setText(str(profRange[0]))
		self.ui.lineEdit_2.setText(str(profRange[1]))
		self.oldRange = profRange
				
	def accept(self):
		try:
			newrange = (float(self.ui.lineEdit.text()),float(self.ui.lineEdit_2.text()))
		except Exception, e:
			raise e
			newrange = self.oldRange
		finally:
			self.newRange.emit(newrange)
			self.close()
		
def main():	
	app = QtGui.QApplication(sys.argv)
	cameraDevice = CameraDevice(mirrored = True)
	mw = MW(cameraDevice)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()