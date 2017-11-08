# mod.zombi
from Components.Converter.Converter import Converter
from Components.Element import cached
from ServiceReference import ServiceReference
from enigma import eServiceCenter, eServiceReference, iServiceInformation, iPlayableService, eDVBFrontendParametersSatellite, eDVBFrontendParametersCable
from string import upper
from Tools.Directories import fileExists, resolveFilename
from os import environ, listdir, remove, rename, system
from Components.config import config
import gettext

class extExtraInfo(Converter, object):
    ECMINFO = 0
    EMU = 1
    CRD = 2
    NET = 3

    def __init__(self, type):
        Converter.__init__(self, type)
        self.list = []
        self.rescan = False
        self.interesting_events = {'EcmInfo': (self.ECMINFO, self.rescan),
         'Emu': (self.EMU, self.rescan),
         'Crd': (self.CRD, self.rescan),
         'Net': (self.NET, self.rescan)}
        if type == 'EcmInfo':
            self.type = self.ECMINFO
        elif type == 'Emu':
            self.type = self.EMU
        elif type == 'Crd':
            self.type = self.CRD
        elif type == 'Net':
            self.type = self.NET

    @cached
    def getText(self):
        service = self.source.service
        if service:
            info = service.info()
            if not info:
                return ''
            if info.getInfo(iServiceInformation.sIsCrypted):
                self.DynTimer.start(3000)
            text = ''
        elif self.type == self.ECMINFO:
            ecmcam = self.getEcmCamInfo()
            text = ecmcam
        return text

    text = property(getText)

    @cached
    def getBoolean(self):
        service = self.source.service
        if service:
            info = service.info()
            if not info:
                return False
            if self.type == self.EMU:
                caemm = self.getEmu()
                return caemm
            if self.type == self.CRD:
                caemm = self.getCrd()
                return caemm
            caemm = self.type == self.NET and self.getNet()
            return caemm
        return False

    boolean = property(getBoolean)

    def changed(self, what):
        self.what = what
        if what[0] in self.interesting_events:
            Converter.changed(self, what)
        Converter.changed(self, what)

    def getEmu(self):
        try:
            f = open('/tmp/ecm.info', 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        contentInfo = content.split('\n')
        for line in contentInfo:
            if line.startswith('using:') or line.startswith('source:'):
                using = self.parseEcmInfoLine(line)
                if using == 'emu':
                    return True

        return False

    def getCrd(self):
        try:
            f = open('/tmp/ecm.info', 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        contentInfo = content.split('\n')
        for line in contentInfo:
            if line.startswith('using:') or line.startswith('from:'):
                using = self.parseEcmInfoLine(line)
                if using == 'sci' or using == 'local':
                    return True

        return False

    def getNet(self):
        try:
            f = open('/tmp/ecm.info', 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        contentInfo = content.split('\n')
        for line in contentInfo:
            if line.startswith('using:') or line.startswith('from:'):
                using = self.parseEcmInfoLine(line)
                if using != 'fta' and using != 'emu' and using != 'sci' and using != 'local':
                    return True
            elif line.startswith('source:'):
                using = self.parseEcmInfoLine(line)
                using = using[:3]
                if using == 'net':
                    return True

        return False

    def parseEcmInfoLine(self, line):
        if line.__contains__(':'):
            idx = line.index(':')
            line = line[idx + 1:]
            line = line.replace('\n', '')
            while line.startswith(' '):
                line = line[1:]

            while line.endswith(' '):
                line = line[:-1]

            return line
        else:
            return ''
