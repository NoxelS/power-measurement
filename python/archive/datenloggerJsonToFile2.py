# Datenlogger MMI

from mcp3008 import *
from datetime import datetime
import RPi.GPIO as GPIO
import json
import time
GPIO.setmode(GPIO.BCM)

# Initialisierung

mcp = MCP3008()
HF59B_CHANNEL = 0
HFW59D_CHANNEL = 1
HF59B = True
HFW59D = False

Start = False
Stop = True

# Initialisierung der GPIOs

GPIO.setup(22, GPIO.OUT)  # sets LED HF59B      GPIO 22 to output
GPIO.setup(23, GPIO.OUT)  # sets LED HFW59D     GPIO 23 to output
GPIO.setup(24, GPIO.IN)  # sets Key select      GPIO 24 to input
GPIO.setup(25, GPIO.IN)  # sets Key start/stop  GPIO 25 to input

# *************************************************************************
# die LEDs werden je nach Status von HF59B und HFW59D eingeschaltet
# *************************************************************************


def updateLED():

    if HF59B == True:
        GPIO.output(22, GPIO.HIGH)
    else:
        GPIO.output(22, GPIO.LOW)

    if HFW59D == True:
        GPIO.output(23, GPIO.HIGH)
    else:
        GPIO.output(23, GPIO.LOW)

# **************************************************************************
# my_callback_select definiert was beim Betätigen der Select Taste passiert
# **************************************************************************


def my_callback_select(channel):
    global HF59B, HFW59D
#    print('This is a edge event callback function!')
#    print('Edge detected on channel %s'%channel)
#    print('This is run in a different thread to your main program')
    if Start == False:
        if HF59B == True and HFW59D == True:
            HFW59D = not HFW59D
        elif HF59B == True and HFW59D == False:
            HF59B = not HF59B
            HFW59D = not HFW59D
        else:
            HF59B = not HF59B
        updateLED()
    else:
        blink()

# ************************************************************************
# my_callback_start_stop definiert was beim Betätigen der Start/Stop
# Taste passiert
# ************************************************************************


def my_callback_start_stop(channel):
    global Start
#    print('This is a edge event callback function!')
#    print('Edge detected on channel %s'%channel)
#    print('This is run in a different thread to your main program')

    Start = not Start

    if Start == True:
        blink()
        # start data acquisition
    else:
        # stop data acquisition
        updateLED()

# *************************************************************************
# die LED's blinken je nach Status von HF59B und HFW59D und gehen dann aus
# dies zeigt den Start der Data Acqusition an
# *************************************************************************


def blink():

    global HF59B, HFW59D
    bCount = 0

    if HF59B == True and HFW59D == True:
        while bCount < 5:
            GPIO.output(22, GPIO.LOW)
            GPIO.output(23, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(23, GPIO.HIGH)
            time.sleep(0.5)
            bCount += 1
    elif HF59B == True and HFW59D == False:
        while bCount < 5:
            GPIO.output(22, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(22, GPIO.HIGH)
            time.sleep(0.5)
            bCount += 1
    elif HF59B == False and HFW59D == True:
        B2_count = 0
        while bCount < 5:
            GPIO.output(23, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(23, GPIO.HIGH)
            time.sleep(0.5)
            bCount += 1

    # switch LEDs off for the time of data acquisition
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)


# ************************************************************************************************
# add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
GPIO.add_event_detect(
    24, GPIO.RISING, callback=my_callback_select, bouncetime=300)
GPIO.add_event_detect(
    25, GPIO.RISING, callback=my_callback_start_stop, bouncetime=300)

# main ******************************************************************************************

# def wríteToFile():
#    with open('data.json', 'w') as outfile:
#        json.dump(data, outfile)

updateLED()

while True:

    print(HF59B, HFW59D, Start)

    voltage = 0
    power = 0
    kanal = 0
    date_now = 0
    time_now = 0
    with open('data.json') as json_file:
        print(json_file)        
        data = json.load(json_file)
        print(json_file)
        with open('data.json', 'w') as outfile:

            while Start == True:

                if HF59B == True:
                    kanal = 1
                    analog_value = mcp.analog_read(HF59B_CHANNEL)
                    dateTimeObj = datetime.now()
                    date_now = dateTimeObj.strftime("%m/%d/%Y")
                    time_now = dateTimeObj.strftime("%H:%M:%S.%f")
                    voltage = 2.47 * analog_value / 1024
                    power = voltage * 1000
                    print("voltage: (%.3fV) (%.3fuW)" %
                          (voltage, power), dateTimeObj, "HF59B")

                    # data = {}
                    # data['messdaten'] = []
                    data['messdaten'].append({
                        'date': date_now,
                        'time': time_now,
                        'voltage': voltage,
                        'power': power,
                        'channel': kanal
                    })
                    json.dump(data, outfile)

                if HFW59D == True:
                    kanal = 2
                    analog_value = mcp.analog_read(HFW59D_CHANNEL)
                    dateTimeObj = datetime.now()
                    date_now = dateTimeObj.strftime("%m/%d/%Y")
                    time_now = dateTimeObj.strftime("%H:%M:%S.%f")
                    voltage = 2.47 * analog_value / 1024
                    power = voltage * 1000
                    print("voltage: (%.3fV) (%.3fuW)" %
                          (voltage, power), dateTimeObj, "HFW59D")

                    # data = {}
                    # data['messdaten'] = []
                    data['messdaten'].append({
                        'date': date_now,
                        'time': time_now,
                        'voltage': voltage,
                        'power': power,
                        'channel': kanal
                    })

                    json.dump(data, outfile)

                time.sleep(1)
    time.sleep(1)
