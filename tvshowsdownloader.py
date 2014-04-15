#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "J. Martin"
__license__ = """GPL v3. See LICENCE for full text.
Includes software parts by XBMC team, and feedparser, check respective files for licence details"""

import feedparser
import re
import os
import ConfigParser
import time

logfile = "tvshowlog.txt"

subfile = "subpen.txt"


#os.chdir ("/home/pi/tvshowsdownloader/")


subfileo = open(subfile)
subpending = []
while True:
	line = subfileo.readline()
	if not line:
		break
		
	parts = line.split(',')
	subpending.append([parts[0], int(parts[1]), int(parts[2])])
subfileo.close()


def sendNotification (text):
	os.system("echo \"" + text + "\" | /usr/bin/sendxmpp -t -u ceoserverpi -o gmail.com jose.martin.burgos")
def writeToLog (text, level):
	f = open ("logfile", "a")
	
	a=""
	
	for i in range(level):
		a = a + "-"
	
	print >> f, a + text
	print  a + text

#-------------------------------------------------------------------

if __name__=='__main__':
	
	
	writeToLog("Runned at " + time.strftime("%d/%m/%Y %H:%M:%S"),0)
	writeToLog("",0)
	writeToLog("Checking for new episodes...",0)
	
	showFile = "shows.cfg"
	downloadDir = "/var/lib/transmission-daemon/newtorrent/"
	configFile = ConfigParser.ConfigParser()
	configFile.read(showFile)
	for show in configFile.sections():
	
		writeToLog(show,1)
		writeToLog( "Downloading RSS file...",2)
		python_wiki_rss_url = configFile.get(show, "rss")
	
		feed = feedparser.parse( python_wiki_rss_url )
	
		last_chapter = int(configFile.get(show, "last_chapter"))
		last_season = int(configFile.get(show, "last_season"))
	
		counter = 1
		while feed["bozo"] == 1:
			#writeToLog("Failed, retrying...")
			feed = None
			feed = feedparser.parse( python_wiki_rss_url )
			counter +=1
			if counter == 11:
				writeToLog("Cannot download RSS",2)
				break

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
				#print "Torrent: " + str(item["link"])
				#os.system("wget -q " + str(item["link"]) + " -P " + downloadDir)
				os.system("transmission-remote --add \"" + item["link"] + "\" --auth transmission:esteesmiservidortorrent")
			
				#notify
				chpstr= show + " S" + str(season).zfill(2) + "E" + str(chapter).zfill(2)
				
				sendNotification("Downloading " + chpstr)
				#subs
				subpending.append([show,season,chapter])
			
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

#print subpending
for entry in subpending:
	import subService
	writeToLog( "Looking for sub to " + entry[0] + " " + str(entry[1]).zfill(2) + "x" + str(entry[2]).zfill(2),1)
	a=subService.search_subtitles("", "", entry[0],"",str(entry[1]),str(entry[2]),"","","Spanish","","","")
	if len(a[0]) > 0:
		flag = 0
		for i in range(len(a[0])):
			tipo = re.compile( "\((.*)\)" ).search( str(a[0][i]["filename"]) ).group( 1 )
			#print "Tipo: " + tipo
			if tipo == "ESPAÑA":
				subService.download_subtitles(a[0],i,None,"/storage/USB/Descargas/Subtitles",None,None)
				flag = 1
		if flag == 1:
			writeToLog( "Found, removing...",2)
			sendNotification("Subtitles for " + entry[0] + " S" + str(entry[1]).zfill(2) + "E" + str(entry[2]).zfill(2) + " downloaded")
			subpending.remove(entry)



subfileo = open(subfile,"w")
for entry in subpending:
	print >> subfileo, entry[0] + "," + str(entry[1]) + "," + str(entry[2])
subfileo.close()
writeToLog("Done",0)
writeToLog("---------------------------------------",0)

