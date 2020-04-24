# -*- coding: utf-8 -*-

from datetime import date
import datetime
import os
import random
import json
import time
from timeit import default_timer as timer
from mcp3008 import *
from datetime import datetime
import RPi.GPIO as GPIO
import signal

# * Cleaning up
def keyboardInterruptHandler(signal, frame):
    GPIO.cleanup()
    print("Script exiting...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

# * Disable GPIO Debug
GPIO.setwarnings(False)

# * Debug
print("Starting script...")

# * Initialisierung
GPIO.setmode(GPIO.BCM)
mcp = MCP3008()
HF59B_CHANNEL = 0
HF59B = True
HFW59D_CHANNEL = 1
HFW59D = False
start = False

# * Constants
TIME_INTERVAL = 100
TODAY = date.today().strftime("%d-%m-%Y")
DEBUG_STEPPER = 100000
SEED = random.randint(10000000, 20000000)
PATH = "./data/" + str(TODAY)+"-"+str(SEED)+"-data.vpd"
# ? TIME_INTERVAL = 0 => Ifinitly small
# ? TIME_INTERVAL > 0 => Time between writes in ms
TIME_INTERVAL = 0

# * Initialisierung der GPIOs
GPIO.setup(22, GPIO.OUT)  # sets LED HF59B      GPIO 22 to output
GPIO.setup(23, GPIO.OUT)  # sets LED HFW59D     GPIO 23 to output
GPIO.setup(24, GPIO.IN)  # sets Key select      GPIO 24 to input
GPIO.setup(25, GPIO.IN)  # sets Key start/stop  GPIO 25 to input


# * Die LEDs werden je nach Status von HF59B und HFW59D eingeschaltet
def updateLED():
    if HF59B:
        GPIO.output(22, GPIO.HIGH)
    else:
        GPIO.output(22, GPIO.LOW)
    if HFW59D:
        GPIO.output(23, GPIO.HIGH)
    else:
        GPIO.output(23, GPIO.LOW)

# * myCallbackSelect definiert was beim Betätigen der Select Taste passiert


def myCallbackSelect(channel):
    global HF59B, HFW59D
    if not start:
        if HF59B and HFW59D:
            HFW59D = not HFW59D
        elif HF59B and not HFW59D:
            HF59B = not HF59B
            HFW59D = not HFW59D
        else:
            HF59B = not HF59B
        updateLED()
    else:
        blink()

# * myCallbackStartStop definiert was beim Betätigen der start/Stop Taste passiert


def myCallbackStartStop(channel):
    global start
    start = not start

    # * start data acquisition
    if start:
        blink()

    # * stop data acquisition
    else:
        updateLED()


# * Die LED's blinken je nach Status von HF59B und HFW59D und gehen dann aus
# * Dies zeigt den start der Data Acqusition an

def blink():
    global HF59B, HFW59D
    blinkSpeed = 0.5
    GPIO.remove_event_detect(25)
    for _ in range(5):
        if HF59B:
            GPIO.output(22, GPIO.LOW)
        if HFW59D:
            GPIO.output(23, GPIO.LOW)
        time.sleep(blinkSpeed)
        if HF59B:
            GPIO.output(22, GPIO.HIGH)
        if HFW59D:
            GPIO.output(23, GPIO.HIGH)
        time.sleep(blinkSpeed)
    # * switch LEDs off for the time of data acquisition
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.add_event_detect(
        25, GPIO.RISING, callback=myCallbackStartStop, bouncetime=300)

# * Schreibt eine neue zeile in die VoltPowerDate file


def writeToVPDFile(objectToWrite, fileToWrite, PATH):
    fileToWrite.write(str(objectToWrite["voltage"]) + "|" + str(objectToWrite["power"]) + "|" + str(
        objectToWrite["date"]) + "|" + str(objectToWrite["time"]) + "|" + str(objectToWrite["channel"]) + "\n")

# * Berechnet die Größe der File (Debug)


def getSize(filename):
    st = os.stat(filename)
    return st.st_size


# * Add rising edge detection on a channel,
# * ignoring further edges for 200ms for switch bounce handling
GPIO.add_event_detect(
    24, GPIO.RISING, callback=myCallbackSelect, bouncetime=300)
GPIO.add_event_detect(
    25, GPIO.RISING, callback=myCallbackStartStop, bouncetime=300)

# ! MAIN

updateLED()

# * Erzeugt eine neue seed-spezifische File
if not os.path.exists(PATH):
    f = open(PATH, "w")
    f.write("#"+str(SEED)+"-"+str(TODAY)+"\n")
    f.close()

with open(PATH, "a") as file:
    while True:
        # print(HF59B, HFW59D, start)
        voltage = 0
        power = 0
        kanal = 0
        date_now = 0
        time_now = 0

        while start:
            time.sleep(TIME_INTERVAL / 1000)
            dateTimeObj = datetime.now()
            date_now = dateTimeObj.strftime("%m/%d/%Y")
            time_now = dateTimeObj.strftime("%H:%M:%S.%f")

            if HF59B:
                kanal = 1
                analog_value = mcp.analog_read(HF59B_CHANNEL)
                voltage = 2.47 * analog_value / 1024
                power = voltage * 1000

                # ! Schreibt die Daten in die File
                writeToVPDFile({
                    "power": str(round(power, 5)),
                    "voltage": str(round(voltage, 5)),
                    "date": str(date_now),
                    "time": str(time_now),
                    "channel": str(kanal)
                }, file, PATH)

            if HFW59D:
                kanal = 2
                analog_value = mcp.analog_read(HFW59D_CHANNEL)
                voltage = 2.47 * analog_value / 1024
                power = voltage * 1000

                # ! Schreibt die Daten in die File
                writeToVPDFile({
                    "power": str(round(power, 5)),
                    "voltage": str(round(voltage, 5)),
                    "date": str(date_now),
                    "time": str(time_now),
                    "channel": str(kanal)
                }, file, PATH)

