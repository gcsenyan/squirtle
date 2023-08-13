#!/usr/bin/python3

import RPi.GPIO as gpio
import time 
import sys
import getopt
from datetime import datetime

PUMP_GPIO = [18, 23, 24, 25]
MAX_TIME = 60
t = 10

def printUsage(argv0, err=0):
    print("Example usage: ")
    print(argv0, "-p 0,1,2,3 -t 10")
    sys.exit(err)

def sanityCheck(pumps, t):
    for p in pumps:
        if p >= len(PUMP_GPIO):
            print("Unsupported pump number:", p);
            sys.exit(4)
    if t > MAX_TIME:
        print("Time should be shorter than", MAX_TIME, "seconds.")
        sys.exit(5)

def activateOnePump(p, t):
    print("Activating pump", p, "for", t,"seconds.") 
    gpio.output(PUMP_GPIO[p], gpio.HIGH)
    time.sleep(t)
    gpio.output(PUMP_GPIO[p], gpio.LOW)

def activatePumps(pumps, t):
    for p in pumps:
        activateOnePump(p, t)

def shutoffPumps():
    for g in PUMP_GPIO:
        gpio.output(g, gpio.LOW)

def initPumpsGPIO():
    gpio.setmode(gpio.BCM)
    for g in PUMP_GPIO:
        gpio.setup(g, gpio.OUT)


initPumpsGPIO()
shutoffPumps()

if len(sys.argv) < 2:
    printUsage(sys.argv[0], 1)

try:
    opts, args = getopt.getopt(sys.argv[1:], "hp:t:", ["pump", "time"])
    for opt, arg in opts:
        if opt in ("-p", "--pump"):
            pumps_str = list(arg.split(","))
            pumps = [eval(_) for _ in pumps_str]
        elif opt in ("-t", "--time"):
            t = int(arg)
        elif opt in ("-h", "--help"):
            printUsage(sys.argv[0])
        else:
            printUsage(sys.argv[0], 2)

    print(datetime.now())
    sanityCheck(pumps, t)
    activatePumps(pumps, t)

except Exception as e:
    print(e)
    shutoffPumps()
    printUsage(sys.argv[0], 3) 
finally:
    gpio.cleanup()

