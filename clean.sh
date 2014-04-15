#!/bin/bash
#===============================================================================
# 
#  @author: J. Martin
#  April 2014
# 
# 
#  Cleans dir for git upload.
#===============================================================================

rm *~
rm *.pyc
rm logfile
touch logfile
rm subpen.txt
touch subpen.txt
mv shows.cfg shows.cfg.use
cp shows.cfg.default shows.cfg

