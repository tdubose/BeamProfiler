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
from GaussianFit import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from scipy.misc.pilutil import imresize#this import was added
from beam import *
import math

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
		self.sd = SD(self.profRange, self.cameraDevice.exposure, int(self.cameraDevice.gain*100.))
		self.sd.show()
		self.sd.newRange.connect(self.updatePos)
		self.sd.newExposure.connect(self.updateExposure)
		self.sd.newGain.connect(self.updateGain)
		
	def updatePos(self, newRange):
		self.profRange = newRange
		print self.profRange
	
	def updateExposure(self, newExposure):
		#print self.cameraDevice.exposure
		self.cameraDevice.exposure = float(newExposure)#float(newExposure))
		print self.cameraDevice.exposure
	
	def updateGain(self, newGain):
		#print self.cameraDevice.gain
		self.cameraDevice.gain = float(newGain)/100.
		print self.cameraDevice.gain
		
	def startProfile(self):
		self.profRangeStart_Pulse = int(self.profRange[0]*100)
		self.profRangeStop_Pulse = int(self.profRange[1]*100)
		CurrentPos = int(self.controller.getpos(inpulses=True))#returns absolute location in pulses
		self.controller.go(self.profRangeStart_Pulse)
		time.sleep((abs(CurrentPos-self.profRangeStart_Pulse)/4500) + 2)
		#Live Camera View appears to be paused because the entire program is stopped with time.sleep.
		print "Image one about to be taken"
		self.imgPos1 = self.cameraDevice._cameraDevice.read()[1]
		cv2.imwrite("testImgPos1.png", self.imgPos1)
		print "Image one written, stage about to move to position 2"
		CurrentPos2 = int(self.controller.getpos(inpulses=True))
		self.controller.go(self.profRangeStop_Pulse)
		time.sleep((abs(CurrentPos2-self.profRangeStop_Pulse)/4500) + 2)
		print "Image two about to be taken"
		self.imgPos2 = self.cameraDevice._cameraDevice.read()[1]
		cv2.imwrite("testImgPos2.png", self.imgPos2)
		
		#X and Y values may be switched, but the final roi image is correct
		#Using the moments function to get the roi
		widthFactor = 13.0
		gaussParams1 = moments(self.imgPos1.astype(float), circle = 0., rotate = 0., vheight = 0.)
		print str(gaussParams1) + "\n"
		xCenter1 = float(gaussParams1[1])
		yCenter1 = float(gaussParams1[2])
		xWidthReal1 = float(gaussParams1[3])
		yWidthReal1 = float(gaussParams1[4])
		xWidth1 = xWidthReal1*widthFactor
		yWidth1 = yWidthReal1*widthFactor
		
		#Using the gaussfit function to get the beam paramaters
		self.imgroi1 = self.imgPos1.astype(float)[yCenter1-yWidth1:yCenter1+yWidth1, xCenter1-xWidth1:xCenter1+xWidth1]
		cv2.imwrite("TESTimgroi1.png", self.imgroi1)#These images are stored in the python file in C, or in the git file
		self.NEWimgroi1 = imresize(self.imgroi1.astype(float), (170, 170))
		cv2.imwrite("DO_NOT_DELETE_NEWimgroi1.png", self.NEWimgroi1)#MUST WRITE BEFORE setScene
		scene1 = QGraphicsScene()
		scene1.addPixmap(QPixmap("DO_NOT_DELETE_NEWimgroi1.png"))
		self.ui.graphicsView.setScene(scene1)
		self.fit1 = gaussfit(self.imgroi1.astype(float))
		
		#Displaying the calculated parameters to the interface
		x1Diamfwhm = float((self.fit1[4]))#in mm NOTE, it is not fwhm, The name hasn't been changed yet
		y1Diamfwhm = float((self.fit1[5]))#mm
		x1 = self.fit1[2]
		y1 = self.fit1[3]
		self.ui.label_26.setText("%.5f" % (float(x1Diamfwhm*5.5*2)))
		self.ui.label_27.setText("%.5f" % (float(y1Diamfwhm*5.5*2)))#converts to micrometers
		self.ui.label_30.setText(str(self.profRangeStart_Pulse/100.))
		print self.fit1.astype(float)
		
		#Repeat for position 2
		gaussParams2 = moments(self.imgPos2.astype(float), circle = 0., rotate = 0., vheight = 0.)
		print str(gaussParams2) + "\n"
		xCenter2 = float(gaussParams2[1])
		yCenter2 = float(gaussParams2[2])
		xWidthReal2 = float(gaussParams2[3])
		yWidthReal2 = float(gaussParams2[4])
		xWidth2 = xWidthReal2*widthFactor
		yWidth2 = yWidthReal2*widthFactor
		
		self.imgroi2 = self.imgPos2.astype(float)[yCenter2-yWidth2:yCenter2+yWidth2, xCenter2-xWidth2:xCenter2+xWidth2]
		cv2.imwrite("TESTimgroi2.png", self.imgroi2)#These images are stored in the python file in C or in the git file
		self.NEWimgroi2 = imresize(self.imgroi2.astype(float), (170, 170))
		cv2.imwrite("DO_NOT_DELETE_NEWimgroi2.png", self.NEWimgroi2)
		scene2 = QGraphicsScene()
		scene2.addPixmap(QPixmap("DO_NOT_DELETE_NEWimgroi2.png"))
		self.ui.graphicsView_2.setScene(scene2)
		self.fit2 = gaussfit(self.imgroi2.astype(float))#gaussfit returns height, amplitude, x, y, width_x, width_y, rota
		
		x2Diamfwhm = float((self.fit2[4]))#pixels
		y2Diamfwhm = float((self.fit2[5]))#pixels
		x2 = self.fit2[2]
		y2 = self.fit2[3]
		self.ui.label_33.setText("%.4f" % (float(x2Diamfwhm*5.5*2)))#converts to micrometers
		self.ui.label_35.setText("%.4f" % (float(y2Diamfwhm*5.5*2)))
		self.ui.label_32.setText(str(self.profRangeStop_Pulse/100.))
		print self.fit2.astype(float)
		###########################################################################
		#Getting the data
		deltaZ = float(self.profRange[1] - self.profRange[0]) * 1000. #micrometers
		#print deltaZ
		w1 = float(x1Diamfwhm*5.5*2)
		#print w1
		w2 = float(x2Diamfwhm*5.5*2)
		#print w2
		wavelength = .663#in  micrometers
		y1 = float(y1Diamfwhm*5.5*2)
		#print y1
		y2 = float(y2Diamfwhm*5.5*2)
		#print y2
		
		####################################### solution to 3rd position ambiguity(using only the major axis)
		secondSolution = beamParam2(deltaZ, w1, w2, wavelength)
		Testz1 = int(secondSolution[0]/1000.)
		print "Test z1 in mm: " + str(Testz1)
		CurrentPos3 = int(self.controller.getpos(inpulses=True))
		waistPos = ((self.profRangeStart_Pulse)/100-Testz1)# in mm
		self.controller.go(waistPos*100)#in pulses
		time.sleep((abs(CurrentPos3-waistPos*100)/4500) + 2)
		print "3rd image about to be taken"
		self.imgPos3 = self.cameraDevice._cameraDevice.read()[1]
		gaussParams3 = moments(self.imgPos3.astype(float), circle = 0., rotate = 0., vheight = 0.)
		xCenter3 = gaussParams3[1]
		yCenter3 = gaussParams3[2]
		xWidthReal3 = gaussParams3[3]
		yWidthReal3 = gaussParams3[4]
		xWidth3 = xWidthReal3*widthFactor
		yWidth3 = yWidthReal3*widthFactor
		self.imgroi3 = self.imgPos3.astype(float)[yCenter3-yWidth3:yCenter3+yWidth3, xCenter3-xWidth3:xCenter3+xWidth3]
		cv2.imwrite("TESTimgroi3.png", self.imgroi3)#These images are stored in the python file in C, OR in the git file
		self.fit3 = gaussfit(self.imgroi3.astype(float))
		x3Diamfwhm = float((self.fit3[4]))#pixels, not fwhm
		y3Diamfwhm = float((self.fit3[5]))#pixels, not fwhm
		print "x3Diamfwhm: " + str(x3Diamfwhm)
		print "x2Diamfwhm: " + str(x2Diamfwhm)
		print "x1Diamfwhm: " + str(x1Diamfwhm)#compare 3rd image width to 1st image width, see if it's larger or not
		######################################
		if x3Diamfwhm > x1Diamfwhm:
			majorAxisParamaters = beamParam(deltaZ, w1, w2, wavelength)
			minorAxisParamaters = beamParam(deltaZ, y1, y2, wavelength)
			print "finished with the if statement"

		else:
			majorAxisParamaters = beamParam2(deltaZ, w1, w2, wavelength)
			minorAxisParamaters = beamParam2(deltaZ, y1, y2, wavelength)
			print "finished with the else statement"
		majorAxisParamaters = beamParam(deltaZ, w1, w2, wavelength)
		minorAxisParamaters = beamParam(deltaZ, y1, y2, wavelength)
		
		majorAngle = wavelength/((math.pi)*0.5*float(majorAxisParamaters[2]))
		minorAngle = wavelength/((math.pi)*0.5*float(minorAxisParamaters[2]))
		
		print majorAxisParamaters#a list of z1, z0, w0
		print minorAxisParamaters
		
		self.ui.label_5.setText("%.5f" % float(majorAxisParamaters[2]))
		self.ui.label_7.setText("%.5f" % float((majorAxisParamaters[1])/1000.))#mm
		self.ui.label_6.setText("%.5f" % float(minorAxisParamaters[2]))
		self.ui.label_8.setText("%.5f" % float((minorAxisParamaters[1])/1000.))#mm
		self.ui.label_9.setText("%.5f" % (((majorAxisParamaters[0]/1000) + (self.profRangeStart_Pulse/100.))*-1))
		self.ui.label_10.setText("%.5f" % (((minorAxisParamaters[0]/1000) + (self.profRangeStart_Pulse/100.))*-1))
		self.ui.label_14.setText("%.7f" % float(majorAngle))
		self.ui.label_16.setText("%.7f" % float(minorAngle))
		print "End of start profile"

class SD(QtGui.QDialog):
	
	newRange = QtCore.pyqtSignal(tuple)
	newExposure = QtCore.pyqtSignal(int)
	newGain = QtCore.pyqtSignal(int)
	
	def __init__(self,profRange, exposure, gain):
		print (profRange, exposure, gain)
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