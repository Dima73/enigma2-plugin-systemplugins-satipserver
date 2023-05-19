from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext


def localeInit():
	gettext.bindtextdomain("SATIPserver", resolveFilename(SCOPE_PLUGINS, "SystemPlugins/SATIPserver/locale"))


def _(txt):
	t = gettext.dgettext("SATIPserver", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t


localeInit()
language.addCallback(localeInit)
