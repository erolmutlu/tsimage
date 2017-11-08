# -*- coding: iso-8859-1 -*-
from enigma import eTPM, eNetworkManager
from Components.Console import Console
from Components.About import about
from Components.DreamInfoHandler import DreamInfoHandler
from Components.Language import language
from Components.Sources.List import List
from Components.Ipkg import IpkgComponent
from Tools.Directories import resolveFilename, SCOPE_METADIR
from Tools.HardwareInfo import HardwareInfo
import hashlib
from time import time
from os import urandom

rootkey = ['\x9f', '|', '\xe4', 'G', '\xc9', '\xb4', '\xf4', '#', '&', '\xce', '\xb3', '\xfe', '\xda', '\xc9', 'U', '`', '\xd8', '\x8c', 's', 'o', '\x90', '\x9b', '\\', 'b', '\xc0', '\x89', '\xd1', '\x8c', '\x9e', 'J', 'T', '\xc5', 'X', '\xa1', '\xb8', '\x13', '5', 'E', '\x02', '\xc9', '\xb2', '\xe6', 't', '\x89', '\xde', '\xcd', '\x9d', '\x11', '\xdd', '\xc7', '\xf4', '\xe4', '\xe4', '\xbc', '\xdb', '\x9c', '\xea', '}', '\xad', '\xda', 't', 'r', '\x9b', '\xdc', '\xbc', '\x18', '3', '\xe7', '\xaf', '|', '\xae', '\x0c', '\xe3', '\xb5', '\x84', '\x8d', '\r', '\x8d', '\x9d', '2', '\xd0', '\xce', '\xd5', 'q', '\t', '\x84', 'c', '\xa8', ')', '\x99', '\xdc', '<', '"', 'x', '\xe8', '\x87', '\x8f', '\x02', ';', 'S', 'm', '\xd5', '\xf0', '\xa3', '_', '\xb7', 'T', '\t', '\xde', '\xa7', '\xf1', '\xc9', '\xae', '\x8a', '\xd7', '\xd2', '\xcf', '\xb2', '.', '\x13', '\xfb', '\xac', 'j', '\xdf', '\xb1', '\x1d', ':', '?']

def bin2long(s):
	return reduce( lambda x,y:(x<<8L)+y, map(ord, s))

def long2bin(l):
	res = ""
	for byte in range(128):
		res += chr((l >> (1024 - (byte + 1) * 8)) & 0xff)
	return res

def rsa_pub1024(src, mod):
	return long2bin(pow(bin2long(src), 65537, bin2long(mod)))
	
def decrypt_block(src, mod):
	if len(src) != 128 and len(src) != 202:
		return None
	dest = rsa_pub1024(src[:128], mod)
	hash = hashlib.sha1(dest[1:107])
	if len(src) == 202:
		hash.update(src[131:192])	
	result = hash.digest()
	if result == dest[107:127]:
		return dest
	return None

def validate_cert(cert, key):
	buf = decrypt_block(cert[8:], key) 
	if buf is None:
		return None
	return buf[36:107] + cert[139:196]

def read_random():
	try:
		xor = lambda a,b: ''.join(chr(ord(c)^ord(d)) for c,d in zip(a,b*100))
		random = urandom(8)
		x = str(time())[-8:]
		result = xor(random, x)
				
		return result
	except:
		return None

class SoftwareTools(DreamInfoHandler):
	lastDownloadDate = None
	NetworkConnectionAvailable = None
	list_updating = False
	available_updates = 0
	available_updatelist  = []
	available_packetlist  = []
	installed_packetlist = {}
	upgradable_packages = {}
	upgradeAvailable = False

	def __init__(self):
		aboutInfo = about.getImageVersionString()
		if aboutInfo.startswith("dev-"):
			self.ImageVersion = 'Experimental'
		else:
			self.ImageVersion = 'Stable'
		self.language = language.getLanguage()[:2] # getLanguage returns e.g. "fi_FI" for "language_country"
		DreamInfoHandler.__init__(self, self.statusCallback, blocking = False, neededTag = 'ALL_TAGS', neededFlag = self.ImageVersion)
		self.directory = resolveFilename(SCOPE_METADIR)
		self.hardware_info = HardwareInfo()
		self.list = List([])
		self.NotifierCallback = None
		self.Console = Console()
		self.UpdateConsole = Console()
		self.UpgradeConsole = Console()
		self.cmdList = []
		self.unwanted_extensions = ('-dbg', '-dev', '-doc', '-staticdev')
		self.reboot_required_packages = ('dreambox-dvb-modules', 'kernel-')
		self.ipkg = IpkgComponent()
		self.ipkg.addCallback(self.ipkgCallback)		

	def statusCallback(self, status, progress):
		pass

	def startSoftwareTools(self, callback = None):
		if callback is not None:
			self.NotifierCallback = callback

		if eNetworkManager.getInstance().online():
			self.NetworkConnectionAvailable = True
			self.getUpdates()
		else:
			self.NetworkConnectionAvailable = False
			self.getUpdates()

	def getUpdates(self, callback = None):
		if self.lastDownloadDate is None:
			etpm = eTPM()
			l2cert = etpm.getData(eTPM.DT_LEVEL2_CERT)
			if l2cert is None:
				return
			l2key = validate_cert(l2cert, rootkey)
			if l2key is None:
				return
			l3cert = etpm.getData(eTPM.DT_LEVEL3_CERT)
			if l3cert is None:
				return
			l3key = validate_cert(l3cert, l2key)
			if l3key is None:
				return
			rnd = read_random()
			if rnd is None:
				return
			val = etpm.computeSignature(rnd)
			result = decrypt_block(val, l3key)
			if result[80:88] == rnd:
				if self.NetworkConnectionAvailable == True:
					self.lastDownloadDate = time()
					if self.list_updating is False and callback is None:
						self.list_updating = True
						self.ipkg.startCmd(IpkgComponent.CMD_UPDATE)
					elif self.list_updating is False and callback is not None:
						self.list_updating = True
						self.NotifierCallback = callback
						self.ipkg.startCmd(IpkgComponent.CMD_UPDATE)
					elif self.list_updating is True and callback is not None:
						self.NotifierCallback = callback
				else:
					self.list_updating = False
					if callback is not None:
						callback(False)
					elif self.NotifierCallback is not None:
						self.NotifierCallback(False)
			else:
				self.NetworkConnectionAvailable = False
				self.list_updating = False
				if callback is not None:
					callback(False)
				elif self.NotifierCallback is not None:
					self.NotifierCallback(False)		
		else:
			if self.NetworkConnectionAvailable == True:
				self.lastDownloadDate = time()
				if self.list_updating is False and callback is None:
					self.list_updating = True
					self.ipkg.startCmd(IpkgComponent.CMD_UPDATE)
				elif self.list_updating is False and callback is not None:
					self.list_updating = True
					self.NotifierCallback = callback
					self.ipkg.startCmd(IpkgComponent.CMD_UPDATE)
				elif self.list_updating is True and callback is not None:
					self.NotifierCallback = callback
			else:
				if self.list_updating and callback is not None:
					etpm = eTPM()
					l2cert = etpm.getData(eTPM.DT_LEVEL2_CERT)
					if l2cert is None:
						return
					l2key = validate_cert(l2cert, rootkey)
					if l2key is None:
						return
					l3cert = etpm.getData(eTPM.DT_LEVEL3_CERT)
					if l3cert is None:
						return
					l3key = validate_cert(l3cert, l2key)
					if l3key is None:
						return
					rnd = read_random()
					if rnd is None:
						return
					val = etpm.computeSignature(rnd)
					result = decrypt_block(val, l3key)
					if result[80:88] == rnd:
						self.NotifierCallback = callback
						self.startIpkgListAvailable()
				else:	
					self.list_updating = False
					if callback is not None:
						callback(False)
					elif self.NotifierCallback is not None:
						self.NotifierCallback(False)

	def ipkgCallback(self, event, param):
		if event == IpkgComponent.EVENT_ERROR:
			self.list_updating = False
			if self.NotifierCallback is not None:
				self.NotifierCallback(False)
		elif event == IpkgComponent.EVENT_DONE:
			if self.list_updating:
				self.startIpkgListAvailable()
		#print event, "-", param		
		pass

	def startIpkgListAvailable(self, callback = None):
		if callback is not None:
			self.list_updating = True
		if self.list_updating:
			if not self.UpdateConsole:
				self.UpdateConsole = Console()
			cmd = "opkg list | grep -e '^[a-z][a-z0-9+.-]'"
			self.UpdateConsole.ePopen(cmd, self.IpkgListAvailableCB, callback)

	def IpkgListAvailableCB(self, result, retval, extra_args = None):
		(callback) = extra_args
		if result:
			if self.list_updating:
				self.available_packetlist = []
				for x in result.splitlines():
					tokens = x.split(' - ')
					name = tokens[0].strip()
					if not any(name.endswith(x) for x in self.unwanted_extensions):
						l = len(tokens)
						version = l > 1 and tokens[1].strip() or ""
						descr = l > 2 and tokens[2].strip() or ""
						self.available_packetlist.append([name, version, descr])
				if callback is None:
					self.startInstallMetaPackage()
				else:
					if self.UpdateConsole:
						if len(self.UpdateConsole.appContainers) == 0:
								callback(True)
		else:
			self.list_updating = False
			if self.UpdateConsole:
				if len(self.UpdateConsole.appContainers) == 0:
					if callback is not None:
						callback(False)

	def startInstallMetaPackage(self, callback = None):
		if callback is not None:
			self.list_updating = True
		if self.list_updating:
			if self.NetworkConnectionAvailable == True:
				if not self.UpdateConsole:
					self.UpdateConsole = Console()
				cmd = "opkg install enigma2-meta enigma2-plugins-meta enigma2-skins-meta"
				self.UpdateConsole.ePopen(cmd, self.InstallMetaPackageCB, callback)
			else:
				self.InstallMetaPackageCB(True)

	def InstallMetaPackageCB(self, result, retval = None, extra_args = None):
		(callback) = extra_args
		if result:
			self.fillPackagesIndexList()
			if callback is None:
				self.startIpkgListInstalled()
			else:
				if self.UpdateConsole:
					if len(self.UpdateConsole.appContainers) == 0:
							callback(True)
		else:
			self.list_updating = False
			if self.UpdateConsole:
				if len(self.UpdateConsole.appContainers) == 0:
					if callback is not None:
						callback(False)

	def startIpkgListInstalled(self, callback = None):
		if callback is not None:
			self.list_updating = True
		if self.list_updating:
			if not self.UpdateConsole:
				self.UpdateConsole = Console()
			cmd = "opkg list-installed"
			self.UpdateConsole.ePopen(cmd, self.IpkgListInstalledCB, callback)

	def IpkgListInstalledCB(self, result, retval, extra_args = None):
		(callback) = extra_args
		if result:
			self.installed_packetlist = {}
			for x in result.splitlines():
				tokens = x.split(' - ')
				name = tokens[0].strip()
				if not any(name.endswith(x) for x in self.unwanted_extensions):
					l = len(tokens)
					version = l > 1 and tokens[1].strip() or ""
					self.installed_packetlist[name] = version
			for package in self.packagesIndexlist[:]:
				if not self.verifyPrerequisites(package[0]["prerequisites"]):
					self.packagesIndexlist.remove(package)
			for package in self.packagesIndexlist[:]:
				attributes = package[0]["attributes"]
				if attributes.has_key("packagetype"):
					if attributes["packagetype"] == "internal":
						self.packagesIndexlist.remove(package)
			if callback is None:
				self.listUpgradable()
			else:
				if self.UpdateConsole:
					if len(self.UpdateConsole.appContainers) == 0:
							callback(True)
		else:
			self.list_updating = False
			if self.UpdateConsole:
				if len(self.UpdateConsole.appContainers) == 0:
					if callback is not None:
						callback(False)

	def listUpgradable(self, callback = None):
		self.list_updating = True
		if not self.UpgradeConsole:
			self.UpgradeConsole = Console()
		cmd = "opkg list-upgradable"
		self.UpgradeConsole.ePopen(cmd, self.listUpgradableCB, callback)

	def listUpgradableCB(self, result, retval, extra_args = None):
		(callback) = extra_args
		self.upgradable_packages = {}
		self.available_updates = 0
		self.available_updatelist  = []
		if result:
			for x in result.splitlines():
				tokens = x.split(' - ')
				name = tokens[0].strip()
				if not any(name.endswith(x) for x in self.unwanted_extensions):
					l = len(tokens)
					version = l > 2 and tokens[2].strip() or ""
					self.upgradable_packages[name] = version
		for package in self.packagesIndexlist[:]:
			attributes = package[0]["attributes"]
			packagename = attributes["packagename"]
			for x in self.available_packetlist:
				if x[0] == packagename:
					if self.installed_packetlist.has_key(packagename):
						if self.installed_packetlist[packagename] != x[1]:
							self.available_updates +=1
							self.available_updatelist.append([packagename])
		self.list_updating = False
		if self.upgradable_packages:
			self.upgradeAvailable = True
		if self.UpgradeConsole:
			if len(self.UpgradeConsole.appContainers) == 0:
				if callback is not None:
					callback(True)
					callback = None
				elif self.NotifierCallback is not None:
					self.NotifierCallback(True)
					self.NotifierCallback = None

	def cleanupSoftwareTools(self):
		self.list_updating = False
		if self.NotifierCallback is not None:
			self.NotifierCallback = None
		self.ipkg.stop()
		if self.Console is not None:
			if len(self.Console.appContainers):
				for name in self.Console.appContainers.keys():
					self.Console.kill(name)
		if self.UpdateConsole is not None:
			if len(self.UpdateConsole.appContainers):
				for name in self.UpdateConsole.appContainers.keys():
					self.UpdateConsole.kill(name)
		if self.UpgradeConsole is not None:
			if len(self.UpgradeConsole.appContainers):
				for name in self.UpgradeConsole.appContainers.keys():
					self.UpgradeConsole.kill(name)

	def verifyPrerequisites(self, prerequisites):
		if prerequisites.has_key("hardware"):
			hardware_found = False
			for hardware in prerequisites["hardware"]:
				if hardware == self.hardware_info.device_name:
					hardware_found = True
			if not hardware_found:
				return False
		return True


iSoftwareTools = SoftwareTools()
