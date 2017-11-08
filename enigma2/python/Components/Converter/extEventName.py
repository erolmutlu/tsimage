# mod.zombi
from Components.Converter.Converter import Converter
from Components.Element import cached

class extEventName(Converter, object):
	EXTENDED_DESCRIPTION = 0
	WideInfo = 1
	HDInfo = 2
	DolbyInfo = 3
	DolbyA = 4


	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "ExtendedDescription":
			self.type = self.EXTENDED_DESCRIPTION
		elif type == "WideInfo":
			self.type = self.WideInfo
		elif type == "HDInfo":
			self.type = self.HDInfo
		elif type == "DolbyInfo":
			self.type = self.DolbyInfo		
		else:
			self.type = self.DolbyA

	@cached
	def getBoolean(self):
		event = self.source.event
                #service = self.source.service
		if event is None:
			return False

		elif self.type == self.WideInfo:
			data = event.getComponentData()
                        print "[extEventName] WideInfo data = %s" %data
			if "16:9" in data or "11" in data:
				return True
			return False
		elif self.type == self.HDInfo:
			data = event.getComponentData()
                        print "[extEventName] HDInfo data = %s" %data
			if "11" in data or "HDTV" in data:
				return True
			return False
		elif self.type == self.DolbyInfo:
			data = event.getComponentData()
			#data = str(event.getNumComponent())
			#audio = service.audioTracks()
                        #data = audio.getTrackInfo(0)
                        print "[extEventName] DolbyInfo data = %s" %data
			if "dolby" in data or "AC3" in data:
				return True
			if "Dolby" in data or "AC3" in data:
				return True	
			if "DOLBY" in data or "AC3" in data:
				return True	
			return False		
		elif self.type == self.DolbyA:
			data = event.getComponentData()
                        print "[extEventName] DolbyA data = %s" %data
			if "Dolby 5.1" in data or "AC3 5.1" in data:
				return True
			if "Dolby Digital 5.1" in data or "AC3 5.1" in data:
				return True	
			return False

	boolean = property(getBoolean)

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ""

		if self.type == self.EXTENDED_DESCRIPTION:
			desc = event.getShortDescription()
			if desc and desc[-1] != '\n' and desc[-1] != ' ':
				desc += ':::  '
			return desc + event.getExtendedDescription()

	text = property(getText)
