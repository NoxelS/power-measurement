from mcp3008 import *
from datetime import datetime
import time

mcp = MCP3008()
HF59B_CHANNEL = 0
HFW59D_CHANNEL = 1


# Schalterstellung Range max, min abfragen zur Umrechnung
#  max = 19,990 mW/m2
#  min = 1999 uW/m2
Range = max

# Schalterstellung DC output level
# DCout 1V=1, 2V=2
DCout = 1

# Geräteeinstellung Signal
# signal RMS, Peak , Peakhold
RMS = 1
Peak = 2
Peakhold =3
Signal = RMS


while True:
   analog_value = mcp.analog_read(HFW59D_CHANNEL)
   dateTimeObj = datetime.now()
   voltage = 2.47 * analog_value / 1024
   leistung = voltage * 1000
#   temperature_c = (voltage * 1000 - 500) / 10
#   temperature_f = 9.0 / 5.0 * temperature_c + 32.0
#   print "analog_Voltage: %.2fV" % (voltage)
   print ("voltage: (%.3fV) (%.3fuW)" % (voltage, leistung), dateTimeObj)
   #print(dateTimeObj)
   time.sleep(0.2)

