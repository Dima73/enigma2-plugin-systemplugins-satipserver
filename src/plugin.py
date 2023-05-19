from . import _
from enigma import getDesktop
from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
import os

class SATIPserver(Screen):
	if getDesktop(0).size().width() >= 1920:
		skin = """
		<screen position="center,center" size="1020,420" title="SAT>IP server" >
			<widget name="menu" position="10,10" size="1000,420" font="Regular;30" itemHeight="36" scrollbarMode="showOnDemand" />
		</screen>"""
	else:
		skin = """
		<screen position="center,center" size="720,260" title="SAT>IP server" >
			<widget name="menu" position="10,10" size="700,240" scrollbarMode="showOnDemand" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("SAT>IP server"))
		self["menu"] = MenuList([])
		self.initList()
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.run, "cancel": self.close}, -1)

	def initList(self):
		dx = 4 * " "
		list = []
		self.satpi = os.path.exists("/usr/bin/satpi")
		if self.satpi:
			list.append((_("SatPI server - WEB 'http://<box ip>:8875'"), "satpi --version && satpi --help"))
		else:
			list.append((_("Install SatPI"), "opkg update && opkg install satpi"))
		if self.satpi:
			self.status_satpi = "satpi" in os.popen("top -n 1").read()
			if self.status_satpi:
				list.append((dx + _("Stop SatPI"), "/etc/init.d/satpi stop"))
			else:
				list.append((dx + _("Start SatPI"), "/etc/init.d/satpi start"))
			self.autostart_satpi = os.path.exists("/etc/rc3.d/S80satpi")
			if self.autostart_satpi:
				list.append((dx + _("Disable autostart SatPI"), "update-rc.d -f satpi remove"))
			else:
				list.append((dx + _("Enable autostart SatPI"), "update-rc.d satpi defaults 80"))
			list.append((dx + _("Unistall SatPI"), "/etc/init.d/satpi stop && opkg remove satpi"))
		list.append(("-------------------------------------------------", ""))
		list.append((_("Attention - only one server can be used at the same time!"), ""))
		list.append(("-------------------------------------------------", ""))
		self.minisatip = os.path.exists("/usr/bin/minisatip")
		if self.minisatip:
			list.append((_("Minisatip server - WEB 'http://<box ip>:8080'"), "minisatip --help"))
		else:
			list.append((_("Install Minisatip"), "opkg update && opkg install minisatip"))
		if self.minisatip:
			self.status_minisatip = "minisatip" in os.popen("top -n 1").read()
			if self.status_minisatip:
				list.append((dx + _("Stop Minisatip"), "/etc/init.d/minisatip stop"))
			else:
				list.append((dx + _("Start Minisatip"), "/etc/init.d/minisatip start"))
			self.autostart_minisatip = os.path.exists("/etc/rc3.d/S80minisatip")
			if self.autostart_minisatip:
				list.append((dx + _("Disable autostart Minisatip"), "update-rc.d -f minisatip remove"))
			else:
				list.append((dx + _("Enable autostart Minisatip"), "update-rc.d minisatip defaults 80"))
			list.append((dx + _("Unistall Minisatip"), "/etc/init.d/minisatip stop && opkg remove minisatip"))
		self["menu"].setList(list)

	def run(self):
		self.runEntry = None
		entry = self["menu"].l.getCurrentSelection()
		returnValue = entry and len(entry) > 1 and entry[1] or ""
		if returnValue:
			if "opkg" in returnValue:
				self.runEntry = entry
				self.session.openWithCallback(self.runInstall, MessageBox, self.runEntry[0] + "\n" + _("Really execute now?"), MessageBox.TYPE_YESNO)
			else:
				self.session.openWithCallback(self.initList, Console, entry[0], [returnValue])

	def runInstall(self, answer=None):
		if answer and self.runEntry:
			self.session.openWithCallback(self.initList, Console, self.runEntry[0], [self.runEntry[1]])

def main(session, **kwargs):
	session.open(SATIPserver)

def menu(menuid, **kwargs):
	if menuid == "scan":
		return [(_("SAT>IP server"), main, "sat_ip_server", 54)]
	return []

def Plugins(**kwargs):
	pList = []
	pList.append(PluginDescriptor(name=_("SAT>IP server"), description=_("SAT>IP servers for enigma2"), where=PluginDescriptor.WHERE_MENU, needsRestart=False, fnc=menu))
	return pList
