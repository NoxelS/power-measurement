from mcp3008 import *
import time

mcp = MCP3008()
HFW59D_CHANNEL = 7

while True:
   analog_value = mcp.analog_read(HFW59D_CHANNEL)
   voltage = 2.47 * analog_value / 1024
   temperature_c = (voltage * 1000 - 500) / 10
   temperature_f = 9.0 / 5.0 * temperature_c + 32.0
#   print "analog_Voltage: %.2fV" % (voltage)
   print ("Temperatur: %.1fC (%.1fF) (%.3fV)" % (temperature_c, temperature_f, voltage))
   time.sleep(1)

