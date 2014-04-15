# -*- coding: utf-8 -*-
#===============================================================================
# 
#  @author J. Martin 
#  April 2014
# 
#  Manages the TVshowDownloader chapters
#
#===============================================================================

import re
import os

import feedparser

import ConfigParser

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

class Chapters:
    '''
    Handlles the chapters part of TVshowDownloader
    '''
    def __init__(self, showFile, subtitler):
        '''
        Stores the shows file and
        '''
        self.showFile = showFile
        self.configFile = ConfigParser.ConfigParser()
        self.subtitler = subtitler
    def loadShows (self):
    	# Read show file
    	self.configFile.read(self.showFile)

    def checkShows (self):
    	for show in self.configFile.sections():
    	
    		writeToLog(show,1)
    		writeToLog( "Downloading RSS file...",2)

    		showrssUrl = self.configFile.get(show, "rss")
    	
    		feed = feedparser.parse( showrssUrl )
    	
    		last_chapter = int(self.configFile.get(show, "last_chapter"))
    		last_season = int(self.configFile.get(show, "last_season"))
    		
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
    				chpstr = show + " S" + str(season).zfill(2) + "E" + str(chapter).zfill(2)
    				sendNotification("Downloading " + chpstr)

    				#subs
    				self.subtitler.addSub([show,season,chapter])
    			
    				if season > new_season or ((season == new_season) and (chapter > new_chapter)):
    					new_season = season
    					new_chapter = chapter
    			
    			else:
    				flag = 1
    		
    			self.configFile.set(show, "last_chapter", str(new_chapter))
    			self.configFile.set(show, "last_season", str(new_season))
    	with open(self.showFile, 'wb') as configWrite:
    		self.configFile.write(configWrite)