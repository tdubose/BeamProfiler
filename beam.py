#!/usr/local/bin/python
# encoding: utf-8
import math
import numpy
import cv2

def beamParam(deltaZ, w1, w2, wavelength):
	num1 = float(deltaZ*(math.pi**2)*(w1**2)*(w2**2-w1**2) - (2*wavelength**2*deltaZ**3) + math.pi*(math.sqrt((w1-w2)**2*(w1+w2)**2*(deltaZ**2)*(math.pi*w1*w2 - wavelength*deltaZ)*(math.pi*w1*w2 + wavelength*deltaZ))))
	denom1 = float((w1**2 - w2**2)**2*math.pi**2 + 4*wavelength**2*deltaZ**2)
	z1 = float(num1/denom1)
	#print num1
	#print denom1
	#print "z1: " + str(z1)
	num2 = wavelength*(deltaZ**3)*(w1-w2)*(w1+w2)
	denom2 = (deltaZ*math.pi*(w1**4 - w2**4)) + 2*math.sqrt(((w1-w2)**2)*((w1+w2)**2)*(deltaZ**2)*((math.pi*w1*w2-(wavelength*deltaZ)))*(math.pi*w1*w2 + wavelength*deltaZ))
	z0 = 2.0*float(num2/denom2)#depth of focus
	#print num2
	#print denom1
	#print "z0: " + str(z0)
	w0 = math.sqrt((wavelength*z0)/math.pi)*2.0
	#print "w0: " + str(w0)
	return [z1, z0, w0]
	
def beamParam2(deltaZ, w1, w2, wavelength):#this is to resolve the ambiguity of the another possible solution
	num1 = float(deltaZ*(math.pi**2)*(w1**2)*(w2**2-w1**2) - (2*wavelength**2*deltaZ**3) - math.pi*(math.sqrt((w1-w2)**2*(w1+w2)**2*(deltaZ**2)*(math.pi*w1*w2 - wavelength*deltaZ)*(math.pi*w1*w2 + wavelength*deltaZ))))
	denom1 = float((w1**2 - w2**2)**2*math.pi**2 + 4*wavelength**2*deltaZ**2)
	z1 = float(num1/denom1)
	#print num1
	#print denom1
	#print "z1: " + str(z1)
	num2 = wavelength*(deltaZ**3)*(w1-w2)*(w1+w2)
	denom2 = (deltaZ*math.pi*(w1**4 - w2**4)) - 2*math.sqrt(((w1-w2)**2)*((w1+w2)**2)*(deltaZ**2)*((math.pi*w1*w2-(wavelength*deltaZ)))*(math.pi*w1*w2 + wavelength*deltaZ))
	z0 = 2.0*float(num2/denom2)#depth of focus
	#print num2
	#print denom1
	#print "z0: " + str(z0)
	w0 = math.sqrt((wavelength*z0)/math.pi)*2.0
	#print "w0: " + str(w0)
	return [z1, z0, w0]
