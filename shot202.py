import pyvisa
import visa
import re
 
class Shot202():
	
	_TEST_ = 4
	 
	def __init__(self, port):
		self.pos = 0
		self.rm = visa.ResourceManager()
		self.controller = self.rm.get_instrument(port)
	
	def b():
		print "bar"
	
	def go(self, pos):
		self.controller.ask("A:1+P" + str(pos))
		self.controller.ask("G:")
	
	def go_mm(self, pos): # goes to pos in mm
		self.go(pos*1000) 
		
	def getpos(self, inpulses=False): # gets position, returns in pulses if inpulses is True (otherwise mm)
		unicodeStr = (self.controller.ask("Q:"))#Q command returns in unicode the location in pulses of the first and second axis followed by 3 lettered strings.
		Str = unicodeStr.encode("ascii", "ignore")
		posList = re.findall("\s+([0-9]+)",Str)
		pos = int(posList[0])
		if inpulses:
			return "pos" + " pulses"
		else:
			return str(pos/1000) + " mm"
