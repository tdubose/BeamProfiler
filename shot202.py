import pyvisa
import visa
import re
 
class Shot202():
	

	 
	def __init__(self, port):
		self.pos = 0
		self.rm = visa.ResourceManager()
		self.controller = self.rm.get_instrument(port)
	
	def go(self, pos):#absolute movement in pulses
		self.controller.ask("A:1+P" + str(pos))
		self.controller.ask("G:")
	
	def go_mm(self, pos): # goes to pos in mm
		self.go(pos*100) 
		
	def getpos(self, inpulses=False): # gets position, returns in pulses if inpulses is True (otherwise mm)
		unicodeStr = (self.controller.ask("Q:"))#Q command returns in unicode the location in pulses of the first and second axis followed by 3 lettered strings.
		self.controller.ask("w:010")
		Str = unicodeStr.encode("ascii", "ignore")
		posList = re.findall("\s+([0-9]+)",Str)
		pos = int(posList[0])
		if inpulses:
			return str(pos)
		else:
			return str(pos/100)
			
	def move(self, move):#relative movement in pulses
		if (str(move))[0] == "-":
			self.controller.ask("M:1-P" + (str(move))[1:])
			self.controller.ask("G:")
		else:
			self.controller.ask("M:1+P" + str(move))
			self.controller.ask("G:")
	
	def move_mm(self, move):#relative movement in milimeters
		self.move(move*100)
