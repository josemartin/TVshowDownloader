# -*- coding: utf-8 -*-
#===============================================================================
# 
#  @author J. Martin 
#  April 2014
# 
#  Manages the TVshowDownloader log and notifications
#
#===============================================================================


import os

def notify (text):
    os.system("echo \"" + text + "\" | /usr/bin/sendxmpp -t -u ceoserverpi -o gmail.com jose.martin.burgos")
#-------------------------------------------------------------------

class Log:
    '''
    Handlles the chapters part of TVshowDownloader
    '''
    def __init__(self, logfile):
        '''
        Stores the logfile
        '''
        self.logfile = logfile

    def write (self, text, level):
    	f = open (self.logfile, "a")
    	
    	a=""
    	
    	for i in range(level):
    	    a = a + "-"
    	
    	print >> f, a + text
    	print  a + text
    	f.close()