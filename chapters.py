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

from Comm import notify

class Chapters:
    '''
    Handlles the chapters part of TVshowDownloader
    '''
    def __init__(self, showFile, downloadFolder, subtitler, log):
        '''
        Stores the shows file and
        '''
        self.showFile = showFile
        self.downloadFolder = downloadFolder
        self.configFile = ConfigParser.ConfigParser()
        self.subtitler = subtitler
        self.log = log
    def loadShows (self):
        # Read show file
        self.configFile.read(self.showFile)

    def checkShows (self):
        for show in self.configFile.sections():
        
            self.log.write(show,1)
            self.log.write( "Downloading RSS file...",2)

            showrssUrl = self.configFile.get(show, "rss")
        
            feed = feedparser.parse( showrssUrl )
        
            last_chapter = int(self.configFile.get(show, "last_chapter"))
            last_season = int(self.configFile.get(show, "last_season"))
            
            # Try to download the RSS correctly
            counter = 1
            while feed["bozo"] == 1:
                #self.log.write("Failed, retrying...")
                feed = None
                feed = feedparser.parse( showrssUrl )
                counter +=1
                if counter == 11:
                    self.log.write("Cannot download RSS",2)
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
                    self.log.write( "New episode: Season: " + str(season) + ". Chapter: " + str(chapter),2)
                    #print "Season " + str(chpp[0]) + " chapter " + chpp[1]
                    
                    destDir = os.path.join(self.downloadFolder, show)
                    if not os.path.exists(destDir):
                        os.makedirs(destDir)

                    os.system("transmission-remote --add \"" + item["link"] + "\" --auth transmission:esteesmiservidortorrent --download-dir " + destDir)
                
                    #notify
                    chpstr = show + " S" + str(season).zfill(2) + "E" + str(chapter).zfill(2)
                    notify("Downloading " + chpstr)

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