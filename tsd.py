#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "J. Martin"
__license__ = """GPL v3. See LICENCE for full text.
Includes software parts by XBMC team, and feedparser, check respective files for licence details"""

import feedparser
import os
import re
import ConfigParser
import time
from subtitles import Subtitles


# Paths & files
showFile = "shows.cfg"
global logfile 
logfile = "tvshowlog.txt"
subfile = "subpen.txt"
subfolder =	"/storage/USB/Descargas/Subtitles"
downloadDir = "/var/lib/transmission-daemon/newtorrent/"
#os.chdir ("/home/pi/tvshowsdownloader/")



#-------------------------------------------------------------------
def sendNotification (text):
	os.system("echo \"" + text + "\" | /usr/bin/sendxmpp -t -u ceoserverpi -o gmail.com jose.martin.burgos")
#-------------------------------------------------------------------
def writeToLog (text, level):
	f = open ("logfile", "a")
	
	a=""
	
	for i in range(level):
		a = a + "-"
	
	print >> f, a + text
	print  a + text
	f.close()
#-------------------------------------------------------------------

if __name__=='__main__':
	
	# Initialize subtitler
	subtitler = Subtitles (subfile, subfolder)
	subtitler.loadPendingSubs()

	# Initial log traces
	writeToLog("Runned at " + time.strftime("%d/%m/%Y %H:%M:%S"),0)
	writeToLog("",0)
	writeToLog("Checking for new episodes...",0)
	
	# Read show file
	configFile = ConfigParser.ConfigParser()
	configFile.read(showFile)

	for show in configFile.sections():
	
		writeToLog(show,1)
		writeToLog( "Downloading RSS file...",2)

		showrssUrl = configFile.get(show, "rss")
	
		feed = feedparser.parse( showrssUrl )
	
		last_chapter = int(configFile.get(show, "last_chapter"))
		last_season = int(configFile.get(show, "last_season"))
		
		# Try to download the RSS correctly
		counter = 1
		while feed["bozo"] == 1:
			#writeToLog("Failed, retrying...")
			feed = None
			feed = feedparser.parse( showrssUrl )
			counter +=1
			if counter == 11:
				writeToLog("Cannot download RSS",2)
				break

		# Get chapter entries from the RSS
		items = feed["items"]

		flag = 0
		new_season = last_season
		new_chapter = last_chapter
		for item in items:
			title = str(item["title"].encode('utf8'))
			if not "720p" in title:
				continue
			"""titlStr = re.sub("(.*) \[.*\]","\g<1>", title)
	
			chp = titlStr.split()[-1:][0]
			chpp = chp.split('x')"""
			
			#print "Last: " + str(last_season) + "x" + str(last_chapter)
	
			season = int (re.sub(".*([0-9])x([0-9][0-9]) .*","\g<1>",title))
			chapter = int (re.sub(".*([0-9])x([0-9][0-9]) .*","\g<2>",title))
		
		
			if (season > last_season or (season == last_season and chapter > last_chapter)) and flag==0:
				writeToLog( "New episode: Season: " + str(season) + ". Chapter: " + str(chapter),2)
				#print "Season " + str(chpp[0]) + " chapter " + chpp[1]
				

				os.system("transmission-remote --add \"" + item["link"] + "\" --auth transmission:esteesmiservidortorrent")
			
				#notify
				chpstr= show + " S" + str(season).zfill(2) + "E" + str(chapter).zfill(2)
				sendNotification("Downloading " + chpstr)

				#subs
				subtitler.addSub([show,season,chapter])
			
				if season > new_season or ((season == new_season) and (chapter > new_chapter)):
					new_season = season
					new_chapter = chapter
			
			else:
				flag = 1
		
			configFile.set(show, "last_chapter", str(new_chapter))
			configFile.set(show, "last_season", str(new_season))
	with open(showFile, 'wb') as configWrite:
		configFile.write(configWrite)

	writeToLog("",0)
	writeToLog("Checking for subtitles...",0)
	
	subtitler.checkSubtitles()
	subtitler.writePendingSubs()


	writeToLog("Done",0)
	writeToLog("---------------------------------------",0)