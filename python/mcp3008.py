import spidev

class MCP3008:
  def __init__(self, bus = 0, client = 0):
      self.spi = spidev.SpiDev()
      self.spi.open(bus, client)
      self.spi.max_speed_hz=1000000

  def analog_read(self, channel):
      if (channel < 0 or channel > 7):
       return -1
      result = self.spi.xfer2([1, (8 + channel) << 4, 0])
      return ((result[1] & 3) << 8) + result[2]

