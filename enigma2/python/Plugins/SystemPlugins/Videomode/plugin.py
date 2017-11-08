from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.SystemInfo import SystemInfo
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigBoolean, ConfigNothing
from Components.Sources.StaticText import StaticText

import VideoHardware

config.misc.videowizardenabled = ConfigBoolean(default = True)

class VideoSetup(Screen, ConfigListScreen):

	def __init__(self, session, hw):
		Screen.__init__(self, session)
		# for the skin: first try VideoSetup, then Setup, this allows individual skinning
		self.skinName = ["VideoSetup", "Setup" ]
		self.setup_title = _("A/V Settings")
		self.hw = hw
		self.onChangedEntry = [ ]

		# handle hotplug by re-creating setup
		self.onShow.append(self.startHotplug)
		self.onHide.append(self.stopHotplug)

		self.list = [ ]
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)

		from Components.ActionMap import ActionMap
		self["actions"] = ActionMap(["SetupActions"], 
			{
				"cancel": self.keyCancel,
				"save": self.apply,
			}, -2)

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))

		self.createSetup()
		self.grabLastGoodMode()
		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(self.setup_title)

	def startHotplug(self):
		self.hw.on_hotplug.append(self.createSetup)

	def stopHotplug(self):
		self.hw.on_hotplug.remove(self.createSetup)

	def createSetup(self):
		level = config.usage.setup_level.index

		self.list = [
			getConfigListEntry(_("Video")),
			getConfigListEntry(_("Video Output"), config.av.videoport)
		]

		(port, mode, rate) = self._getPortModeRate()

		# if we have modes for this port:
		if mode and rate:
			# add mode- and rate-selection:
			self.list.append(getConfigListEntry(_("Mode"), mode))
			if mode.value == 'PC':
				self.list.append(getConfigListEntry(_("Resolution"), rate))
			else:
				self.list.append(getConfigListEntry(_("Refresh Rate"), rate))

		# some modes (720p, 1080i) are always widescreen. Don't let the user select something here, "auto" is not what he wants.
		force_wide = self.hw.isWidescreenMode(port, mode and mode.value or None)

		if not force_wide:
			self.list.append(getConfigListEntry(_("Aspect Ratio"), config.av.aspect))

		if force_wide or config.av.aspect.value in ("16_9", "16_10"):
			self.list.extend((
				getConfigListEntry(_("Display 4:3 content as"), config.av.policy_43),
				getConfigListEntry(_("Display >16:9 content as"), config.av.policy_169)
			))
		elif config.av.aspect.value == "4_3":
			self.list.append(getConfigListEntry(_("Display 16:9 content as"), config.av.policy_169))

#		if port == "DVI":
#			self.list.append(getConfigListEntry(_("Allow Unsupported Modes"), config.av.edid_override))
		if port and port.value and port.value == "Scart":
			self.list.append(getConfigListEntry(_("Color Format"), config.av.colorformat))
			if level >= 1:
				self.list.append(getConfigListEntry(_("WSS on 4:3"), config.av.wss))
				if SystemInfo["ScartSwitch"]:
					self.list.append(getConfigListEntry(_("Auto scart switching"), config.av.vcrswitch))

		if SystemInfo["CanChangeOsdAlpha"]:
			self.list.append(getConfigListEntry(_("OSD visibility"), config.av.osd_alpha))

		if not isinstance(config.av.scaler_sharpness, ConfigNothing):
			self.list.append(getConfigListEntry(_("Scaler sharpness"), config.av.scaler_sharpness))

		if level >= 1:
			self.list.append(getConfigListEntry(_("Audio")))
			self.list.append(getConfigListEntry(_("AC3 default"), config.av.defaultac3))
			if SystemInfo["CanDownmixAC3"]:
				self.list.append(getConfigListEntry(_("AC3 downmix"), config.av.downmix_ac3))
			self.list.extend((
				getConfigListEntry(_("General AC3 Delay"), config.av.generalAC3delay),
				getConfigListEntry(_("General PCM Delay"), config.av.generalPCMdelay)
			))
			if SystemInfo["SupportsAC3PlusTranscode"]:
				self.list.append(getConfigListEntry(_("Convert AC3+ to AC3"), config.av.convert_ac3plus))

		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.createSetup()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.createSetup()

	def confirm(self, confirmed):
		if not confirmed:
			config.av.videoport.value = self.last_good[0]
			config.av.videomode[self.last_good[0]].value = self.last_good[1]
			config.av.videorate[self.last_good[1]].value = self.last_good[2]
			self.hw.setMode(*self.last_good)
			self.createSetup()
		else:
			self.keySave()

	def _getPortModeRate(self):
		mode = None
		rate = None
		port = config.av.videoport
		if config.av.videomode.has_key(port.value):
			mode = config.av.videomode[port.value]
			if config.av.videorate.has_key(mode.value):
				rate = config.av.videorate[mode.value]
		return (port, mode, rate)

	def _getPortModeRateValues(self):
		mode = None
		rate = None
		port = config.av.videoport.value
		if config.av.videomode.has_key(port):
			mode = config.av.videomode[port].value
			if config.av.videorate.has_key(mode):
				rate = config.av.videorate[mode].value
		return (port, mode, rate)

	def grabLastGoodMode(self):
		self.last_good = self._getPortModeRateValues()

	def apply(self):
		(port, mode, rate) = self._getPortModeRateValues()
		if (port, mode, rate) != self.last_good:
			self.hw.setMode(port, mode, rate)
			from Screens.MessageBox import MessageBox
			self.session.openWithCallback(self.confirm, MessageBox, _("Is this videomode ok?"), MessageBox.TYPE_YESNO, timeout = 20, default = False)
		else:
			self.keySave()

	# for summary:
	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]

	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())

	def createSummary(self):
		from Screens.Setup import SetupSummary
		return SetupSummary


def createInstance(reason, session = None, **kwargs):
	if reason == 0:
		video_hw = VideoHardware.video_hw

def videoSetupMain(session, **kwargs):
	session.open(VideoSetup, VideoHardware.video_hw)

def startSetup(menuid):
	if menuid != "osd_video_audio":
		return [ ]

	return [(_("A/V Settings"), videoSetupMain, "av_setup", 20)]

def VideoWizard(*args, **kwargs):
	from VideoWizard import VideoWizard
	return VideoWizard(*args, **kwargs)

def Plugins(**kwargs):
	list = [
		PluginDescriptor(where = [PluginDescriptor.WHERE_AUTOSTART], fnc = createInstance),
		PluginDescriptor(name=_("Video Setup"), description=_("Advanced Video Setup"), where = PluginDescriptor.WHERE_MENU, needsRestart = False, fnc=startSetup) 
	]
	return list
