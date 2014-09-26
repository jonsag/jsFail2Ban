#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import getopt

from myFunctions import *

##### handle arguments #####
try:
    myopts, args = getopt.getopt(sys.argv[1:],'mv' , ['mail=', 'verbose'])

except getopt.GetoptError as e:
    onError(1, str(e))

if len(sys.argv) == 1: # no options passed
    onError(2, 2)

mailCheck = False
verbose = False

for option, argument in myopts:
    if option in ('-m', '--mail'):
        mailCheck = True
    elif option in ('-v', '--verbose'):
        verbose = True
        

if mailCheck:
    mailUsername, mailPassword = mailUserPass(mailUsername, mailPassword, verbose)
    
    #mbox = mboxConnect(mailUsername, mailPassword, imapAddress, imapPort, verbose)
    #listmBoxes(mbox, verbose)
    #mboxDisconnect(mbox, verbose)
    
    mbox = mboxConnect(mailUsername, mailPassword, imapAddress, imapPort, verbose)
    messagesFound = searchMailForString(mbox, searchString1, searchString2, verbose)
    mboxDisconnect(mbox, verbose)
    
    makeLog(messagesFound, verbose)
    