# mod.zombi
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr
from Components.Element import cached

class extMovieInfo(Converter, object):
    NAME = 0
    PICON = 1

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == "Picon":
            self.type = self.PICON
        else:
            self.type = self.NAME

    def getServiceInfoValue(self, info, what, ref=None):
        v = ref and info.getInfo(ref, what) or info.getInfo(what)
        if v != iServiceInformation.resIsString:
            return "N/A"
        return ref and info.getInfoString(ref, what) or info.getInfoString(what)

    @cached
    def getText(self):
        service = self.source.service
        if isinstance(service, iPlayableServicePtr):
            info = service and service.info()
            ref = None
        else: # reference
            info = service and self.source.info
            ref = service
        if info is None:
            return ""
        if self.type == self.NAME:
            name = ref and info.getName(ref)
            if name is None:
                name = info.getName()
                if name.endswith(".ts"):
                    name = name[:-3]
                elif name.endswith(".mp4") or name.endswith(".avi") or name.endswith(".mkv") or name.endswith(".mov") or name.endswith(".flv") or name.endswith(".m4v") or name.endswith(".mpg") or name.endswith(".iso"):
                    name = name[:-4]
                elif name.endswith(".divx") or name.endswith(".m2ts") or name.endswith(".mpeg"):
                    name = name[:-5]
                else:
                    name = name
            return name.replace('\xc2\x86', '').replace('\xc2\x87', '')
        elif self.type == self.PICON:
            return info.getInfoString(service, iServiceInformation.sServiceref)
        
    text = property(getText)

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] in (iPlayableService.evStart,):
            Converter.changed(self, what)
