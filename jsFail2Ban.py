#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import getopt, getpass

from myFunctions import *

##### handle arguments #####
try:
    myopts, args = getopt.getopt(sys.argv[1:],'g' , ['gmail='])

except getopt.GetoptError as e:
    onError(1, str(e))

if len(sys.argv) == 1: # no options passed
    onError(2, 2)

gmailCheck = False

for option, argument in myopts:
    if option in ('-g', '--gmail'):
        gmailCheck = True
        

if gmailCheck:
    gmailPart()
