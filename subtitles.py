# -*- coding: utf-8 -*-
#===============================================================================
# 
#  @author J. Martin 
#  April 2014
# 
#  Manages the TVshowDownloader subtitles
#
#===============================================================================

import re
import os

# Subtitles service 
import subService

from Comm import notify

class Subtitles:
    '''
    Handlles the subtitles part of TVshowDownloader
    '''
    def __init__(self, filename, downloadFolder, log):
        '''
        Stores the pending subtitles filename
        '''
        self.filename = filename
        self.downloadFolder = downloadFolder
        self.subpending = []
        self.log = log
        
    def loadPendingSubs (self):
        '''
        Loads the subs from the supplied file
        The file shoud contain a chapter by line with the format show,season,chapter

        '''
        if os.path.isfile(self.filename):
            subfile = open(self.filename)
            while True:
    			line = subfile.readline()
    			if not line:
    				break
    				
    			parts = line.split(',')
    			self.subpending.append([parts[0], int(parts[1]), int(parts[2])])
            subfile.close()
    def writePendingSubs (self):
    	'''
    	Writes the pending sub to the supplied filename.
    	See loadPendingSubs() for file syntax
    	'''
    	subfileo = open(self.filename,"w")
        for entry in self.subpending:
			print >> subfileo, entry[0] + "," + str(entry[1]) + "," + str(entry[2])
        subfileo.close()
    def addSub(self, entry):
        '''
        Adds a entry to the pending subtitles
        '''
        self.subpending.append (entry)

    def checkSubtitles (self):
    	'''

    	'''

    	for entry in self.subpending:
			self.log.write( "Looking for sub to " + entry[0] + " S" + str(entry[1]).zfill(2) + "E" + str(entry[2]).zfill(2),1)
			
			subSearch = subService.search_subtitles("", "", entry[0],"",str(entry[1]),str(entry[2]),"","","Spanish","","","")
			
			if len(subSearch[0]) > 0:
				flag = 0
				for i in range(len(subSearch[0])):
					tipo = re.compile( "\((.*)\)" ).search( str(subSearch[0][i]["filename"]) ).group( 1 )
					#print "Tipo: " + tipo
					if tipo == "ESPAÑA":
						subService.download_subtitles(subSearch[0],i,None,self.downloadFolder,None,None)
						flag = 1

				if flag == 1:
					self.log.write( "Found, removing...",2)
					notify("Subtitles for " + entry[0] + " S" + str(entry[1]).zfill(2) + "E" + str(entry[2]).zfill(2) + " downloaded")
					self.subpending.remove(entry)
		