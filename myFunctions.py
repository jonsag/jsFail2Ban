#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import ConfigParser, os, sys

config = ConfigParser.ConfigParser()
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__))) # read config file

gmailUsername = config.get('gmail','gmailUsername')
gmailPassword = config.get('gmail','gmailpassword')

def onError(errorCode, extra):
    print "\nError:"
    if errorCode == 1:
        print extra
        usage(errorCode)
    elif errorCode == 2:
        print "No options given"
        usage(errorCode)
    elif errorCode == 3:
        print "No program part chosen"
        
def usage(exitCode):
    print "\nUsage:"
    print "----------------------------------------"
    print "%s -a <url> -n <name>" % sys.argv[0]
    print "    OR"
    print "%s -f <file>" % sys.argv[0]

    sys.exit(exitCode)
    
def gmailPart(): # check gmail username and password
    if not gmailUsername:
        gmailUsername = raw_input("Gmail username: ")
    if not gmailPassword:
        gmailPassword = getpass.getpass("Gmail password: ")
    
    print "\nGmail username: %s" % gmailUsername
    print "Gmail password: %s" % gmailPassword
