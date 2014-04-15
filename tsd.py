#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "J. Martin"
__license__ = """GPL v3. See LICENCE for full text.
Includes software parts by XBMC team, and feedparser, check respective files for licence details"""

import os
import time
from subtitles import Subtitles
from chapters import Chapters

# Paths & files
showFile = "shows.cfg"
global logfile 
logfile = "tvshowlog.txt"
subfile = "subpen.txt"
subfolder =	"/storage/USB/Descargas/Subtitles"
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
	
	chapterer = Chapters (showFile, subtitler)
	chapterer.loadShows()

	chapterer.checkShows()

	writeToLog("",0)
	writeToLog("Checking for subtitles...",0)
	
	subtitler.checkSubtitles()
	subtitler.writePendingSubs()


	writeToLog("Done",0)
	writeToLog("---------------------------------------",0)