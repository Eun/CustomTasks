# -*- coding: utf-8 -*-
################## SETTINGS ##################################################
SETTINGS = {
  "symbols": [u"[ ]", u"[+]", u"[-]"],
  "colors":  ["keyword", "entity.name.function.CustomTasks", "comment.line.number-sign.CustomTasks"],
  "title-color": "string"
} 
## Note:                                                                    ##
## You might have to restart ST 2 after changing settings                   ##
##                                                                          ##
##                                                                          ##
################## DO NOT CHANGE BELOW #######################################
##                                                                          ##
import sublime, sublime_plugin, re, os.path, codecs
__path__ = os.path.abspath(os.path.dirname(__file__))
print __path__
fo = codecs.open(__path__ + "/CustomTasks.tmLanguage", "w+", "utf-8")
fo.write('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict><key>fileTypes</key><array><string>CustomTasks</string><string>CustomTasks</string><string>todo.txt</string><string>todo</string><string>todolists</string></array><key>name</key><string>CustomTasks</string><key>patterns</key><array>')
max = len(SETTINGS['symbols'])
for i in range(max):
    fo.write('<dict><key>comment</key><string>'+str(i)+'</string><key>match</key><string>')
    fo.write('^(\s+)?'+ SETTINGS['symbols'][i] +'(.*)?$')
    fo.write('</string><key>name</key><string>'+SETTINGS['colors'][i]+'</string></dict>')
fo.write('<dict><key>comment</key><string>Titles</string><key>match</key><string>^(\s+)?(.*)?:$</string><key>name</key><string>'+SETTINGS['title-color']+'</string></dict></array><key>scopeName</key><string>text.CustomTasks</string><key>uuid</key><string>8c6182de-c8b7-428f-85ae-d75b70e48b71</string></dict></plist>');
fo.close();

regexp = ''

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