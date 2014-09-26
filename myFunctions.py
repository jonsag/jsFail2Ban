#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import ConfigParser, os, sys, getpass, imaplib

from pprint import pprint

config = ConfigParser.ConfigParser()
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__))) # read config file

mailUsername = config.get('mail','mailUsername')
mailPassword = config.get('mail','mailpassword')

imapAddress = config.get('mail','imapAddress')
imapPort = int(config.get('mail','imapPort'))

searchString1 = config.get('words','searchString1')
searchString2 = config.get('words','searchString2')

months = config.get('misc','months')

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
    
def mailUserPass(mailUsername, mailPassword, verbose): # check mail username and password
    if not mailUsername:
        mailUsername = raw_input("Enter mail username: ")
    if not mailPassword:
        mailPassword = getpass.getpass("Enter mail password: ")
    if verbose:
        print "--- Mail username: %s" % mailUsername
        print "--- Mail password: %s" % mailPassword
    return mailUsername, mailPassword

def mboxConnect(mailUsername, mailPassword, imapAddress, imapPort, verbose):
    print "--- Setting up connection"
    mbox = imaplib.IMAP4_SSL(imapAddress, imapPort)
    if verbose:
        print "--- Logging in to %s on port %s" % (imapAddress, imapPort)
    mbox.login(mailUsername, mailPassword)
    mbox.select()
    return mbox

def mboxDisconnect(mbox, verbose):
    print "--- Logging out"
    mbox.close()
    mbox.logout()

def listmBoxes(mbox, verbose):
    print "--- Listing mailboxes"
    type, data = mbox.list()
    print 'Response code:', type
    print 'Response:'
    pprint(data)
    
def searchMailForString(mbox, searchString1, searchString2, verbose):
    found = 0
    messagesFound = []
    
    print "--- Searching subject for '%s'" % searchString1   
    typ, data = mbox.search(None, '(SUBJECT "%s")' % searchString1)
    if typ == "OK":
        messages = data[0].split(' ')
        hits = len(messages)
        if verbose:
            print "--- %s messages found" % hits
        print "--- Searching messages for '%s' in subject" % searchString2
        for messageNo in messages:
            subject = ""
            typ, data = mbox.fetch(messageNo, '(RFC822)')
            newData = data[0][1].split('\n')
            for line in newData:
                if line.startswith("From: "):
                    sender = line
                elif line.startswith("X-Google-Original-From: "):
                    googleOriginalFrom = line
                elif line.startswith("Received: "):
                    received = line
                elif line.startswith("Subject: "):
                    subject = line
                elif line.startswith("Date: "):
                    date = line
                
                if searchString2 in subject:
                    found += 1
                    if verbose:
                        print "--- %s: '%s' found in message no: %s" % (found, searchString2, messageNo)
                    else:
                        progress = "%s " % found
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                    messagesFound.append({"messageNo": messageNo, "from": sender,
                        "googleOriginalFrom": googleOriginalFrom, "received": received,
                        "subject": subject, "date": date})
                    subject = ""

    if not verbose:
        print
    print "--- Messages with the words %s and %s in subject: %s" % (searchString1, searchString2, found)
    
    if verbose:
        for line in messagesFound:
            print "\nMessage no: %s" % line['messageNo']
            print "-------------------------------------------------------"
            print line['from']
            print line['googleOriginalFrom']
            print line['received']
            print line['subject']
            print line['date']
        
    return messagesFound

def formatTime(inputDateTime):
    splitDate = inputDateTime.split(' ')
    year = splitDate[2]
    countMonth = 0
    for monthName in months:
        print "%s - %s" % (monthName, splitDate[1])
        countMonth += 1
        if monthName == splitDate[1]:
            if countMonth < 10:
                month = "0%s" % countMonth
            else:
                month = countMonth
            break
    day = splitDate[0]
    splitTime = splitDate[3].split(':')
    hour = splitTime[0]
    minute = splitTime[1]
    second = splitTime[2]
    
    time = "%s-%s-%s %s:%s:%s" % (year, month, day, hour, minute, second)
    return time 

def makeLog(messagesFound, verbose):
    log = []
    print "--- Creating log"
    for line in messagesFound:
        subject = line['subject'].split(' ')
        targetSystem = subject[-1]
        targetServer = subject[2].strip(':').lower()
        IP = subject[4]
        received = line['received'].split(',')
        time = formatTime(received[-1].lstrip(' ')) 
        #time = received[-1].lstrip(' ')
        
        log.append({"targetSystem": targetSystem, "targetServer": targetServer,
            "IP": IP, "time": time})
        
    if verbose:
        print "\nLog:"
        print "--------------------------------------------------------"
        for line in log:
            print "Target system: %s" % line['targetSystem']
            print "Target server: %s" % line['targetServer']
            print "Attacking IP: %s" % line['IP']
            print "Time detected: %s" % line['time']
            print
