#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "J. Martin"
__license__ = """GPL v3. See LICENCE for full text.
Includes software parts by XBMC team, and feedparser, check respective files for licence details"""

import time
from subtitles import Subtitles
from chapters import Chapters
from Comm import Log

# Paths & files
showFile = "shows.cfg"
global logfile 
logfile = "tvshowlog.txt"
subfile = "subpen.txt"
subfolder =	"/storage/USB/Descargas/Subtitles"


if __name__=='__main__':
	# Initialize log
	log = Log (logfile)

	# Initialize subtitler
	subtitler = Subtitles (subfile, subfolder, log)
	subtitler.loadPendingSubs()

	# Initial log traces
	log.write("Runned at " + time.strftime("%d/%m/%Y %H:%M:%S"),0)
	log.write("",0)
	log.write("Checking for new episodes...",0)
	
	# Initialize chapterer
	chapterer = Chapters (showFile, subtitler, log)
	chapterer.loadShows()

	# Check for new shows
	chapterer.checkShows()

	log.write("",0)
	log.write("Checking for subtitles...",0)
	
	# Check for new subtitles
	subtitler.checkSubtitles()
	subtitler.writePendingSubs()


	log.write("Done",0)
	log.write("---------------------------------------",0)