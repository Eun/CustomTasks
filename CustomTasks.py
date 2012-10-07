# -*- coding: utf-8 -*-
import sublime, sublime_plugin, re, os.path, codecs

__path__ = os.path.abspath(os.path.dirname(__file__))


try:
	fo = open(__path__+'/settings.py')
	fo.close();
except IOError as e:
	fo = codecs.open(__path__+'/settings.py', "w+", "utf-8")
   	fo.write('# -*- coding: utf-8 -*-\nimport __builtin__\n################## SETTINGS ##################################################\n__builtin__.SETTINGS = {\n  "symbols": [u"[ ]", u"[+]", u"[-]"],\n  "colors":  ["#F92672FF", "#A6E22EFF", "#75715EFF"],\n  "title-color": "#E6DB74FF"\n} \n## Note:                                                                    ##\n## You might have to restart ST 2 after changing settings                   ##\n## Color Format: rrggbbaa                                                   ##\n##                                                                          ##\n################## DO NOT CHANGE BELOW #######################################\n##                                                                          ##\nimport os\n__path__ = os.path.abspath(os.path.dirname(__file__))\nfo = open(__path__+"/CustomTasks.py","a")\nfo.write("#");\nfo.close();');
   	fo.close();
   	

import settings
fo = codecs.open(__path__ + "/CustomTasks.tmLanguage", "w+", "utf-8")
fo.write('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict><key>fileTypes</key><array><string>CustomTasks</string><string>CustomTasks</string><string>todo.txt</string><string>todo</string><string>todolists</string></array><key>name</key><string>CustomTasks</string><key>patterns</key><array>')
max = len(SETTINGS['symbols'])
for i in range(max):
    fo.write('<dict><key>comment</key><string>'+str(i)+'</string><key>match</key><string>')
    fo.write('^(\s+)?'+ re.escape(SETTINGS['symbols'][i]) +'(.*)?$')
    fo.write('</string><key>name</key><string>CustomTasksColor'+str(i)+'</string></dict>')
fo.write('<dict><key>comment</key><string>Titles</string><key>match</key><string>^(\s+)?(.*)?:$</string><key>name</key><string>CustomTasksColor-1</string></dict></array><key>scopeName</key><string>text.CustomTasks</string><key>uuid</key><string>8c6182de-c8b7-428f-85ae-d75b70e48b71</string></dict></plist>');
fo.close();

regexp = ''

if sublime.version() <= 2174:
	pref = 'Preferences.sublime-settings'
else:
	pref = 'Global.sublime-settings'
settings = sublime.load_settings(pref)

color_scheme = settings.get('color_scheme')

if (color_scheme != None):
	color_scheme_file = os.path.dirname(sublime.packages_path()) + "/" + color_scheme

	import xml.etree.ElementTree as ET
	tree = ET.parse(color_scheme_file)
	root = tree.getroot().find('dict').find('array');
	done = [];
	for d in root:
		if (d.get('pl') == 'CustomTasks'):
			id = int(d.get('id'))
			if (id >= -1 and id < len(SETTINGS['colors'])):
				done.append(id);
				if (id == -1):
					color = SETTINGS['title-color']
				else:
					color = SETTINGS['colors'][id]
				if (color[0] != '#'):
					color = "#" + color;
				d.find('dict').find('string').text = color
			else:
				root.remove(d)

	if (-1 not in done):
		el = ET.SubElement(root, 'dict', pl="CustomTasks", id="-1")
		key = ET.SubElement(el, 'key');
		key.text = 'scope'
		key = ET.SubElement(el, 'string')
		key.text = 'CustomTasksColor-1'
		key = ET.SubElement(el, 'key')
		key.text = 'settings'
		key = ET.SubElement(el, 'dict')
		skey = ET.SubElement(key, 'key')
		skey.text = 'foreground'
		skey = ET.SubElement(key, 'string')
		color = SETTINGS['title-color']
		if (color[0] != '#'):
			color = "#" + color;
		skey.text = color

	for d in range(len(SETTINGS['colors'])):
		if (d not in done):
			el = ET.SubElement(root, 'dict', pl="CustomTasks", id=str(d))
			key = ET.SubElement(el, 'key');
			key.text = 'scope'
			key = ET.SubElement(el, 'string')
			key.text = 'CustomTasksColor' + str(d)
			key = ET.SubElement(el, 'key')
			key.text = 'settings'
			key = ET.SubElement(el, 'dict')
			skey = ET.SubElement(key, 'key')
			skey.text = 'foreground'
			skey = ET.SubElement(key, 'string')
			color = SETTINGS['colors'][d]
			if (color[0] != '#'):
				color = "#" + color;
			skey.text = color



	with open(color_scheme_file, 'w') as f:
	    f.write('<?xml version="1.0" encoding="UTF-8" ?>\n<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
	    tree.write(f, 'utf-8')
	    f.close();

class CustomtasksCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global regexp, status_code
		if (regexp == ''):
			for var in SETTINGS['symbols']:
				regexp += "|" + re.escape(var)

		selection = self.view.sel()
		oldsel = []
		for region in selection:
			oldsel.append(region);
			lines = self.view.split_by_newlines(sublime.Region(region.a, region.b))
			for line in reversed(lines):
				self.rep(edit, self.view.line(line))
		selection.clear()
		for sel in oldsel:
			selection.add(sel)


	def rep(self, edit, region):
		line = self.view.substr(region)
		match = re.search(ur'^([\s]+)?('+regexp[1:]+')?([\s]+)?(.*)$', line, re.UNICODE)
		if match:
			groups = match.groups();
			pre = groups[0]
			spacer = groups[2]
			after = groups[3]
			symb = None
			
			max = len(SETTINGS['symbols'])
			for i in range(max):
				if groups[1] == SETTINGS['symbols'][i]:
					if (i+1 >= max):
						i = -1
					symb = SETTINGS['symbols'][i+1]
					break
			
			if symb == None:
				symb = SETTINGS['symbols'][0]
				spacer = " "
			
			if pre == None:
				pre = ""
			if spacer == None:
				spacer = ""
			if after == None:
				after = ""
			line = pre + symb + spacer + after
			self.view.replace(edit, region, line)
		
	def current_encoding(self):
		if self.view.encoding() == 'Undefined':
			return self.view.settings().get('default_encoding', 'UTF-8')
		else:
			return self.view.encoding()

