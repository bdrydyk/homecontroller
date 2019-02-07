"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal

from pyhap.util import generate_mac
from pyhap.accessories.WebPowerOutlet import WebPowerOutlet
from pyhap.accessory import Bridge, Accessory, Category
import pyhap.loader as loader
from pyhap.accessory_driver import AccessoryDriver
#from pyhap.accessories.BMP180 import BMP180

import board
import digitalio
import busio

import adafruit_si7021

from pyhap.accessory import Accessory, Category
import pyhap.loader as loader


logging.basicConfig(level=logging.INFO)


#print('Humidity: {}%'.format(sensor.relative_humidity))

class TemperatureSensor(Accessory):
    """Implementation of a mock temperature sensor accessory."""

    category = Category.SENSOR  # This is for the icon in the iOS Home app.

    def __init__(self, *args, **kwargs):
        """Here, we just store a reference to the current temperature characteristic and
        add a method that will be executed every time its value changes.
        """
        # If overriding this method, be sure to call the super's implementation first.
        super().__init__(*args, **kwargs)

        # Add the services that this Accessory will support with add_preload_service here
        temp_service = self.add_preload_service('TemperatureSensor')
        self.temp_char = temp_service.get_characteristic('CurrentTemperature')

        # Having a callback is optional, but you can use it to add functionality.
        self.temp_char.setter_callback = self.temperature_changed


        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.si7021 = adafruit_si7021.SI7021(self.i2c)


    def ctoF(self,c_temp):
        return 9.0/5.0 * c_temp + 32

    def ftoC(self,f_temp):
        return  (f_temp - 32) * 5.0/9.0

    def temperature_changed(self, value):
        """This will be called every time the value of the CurrentTemperature
        is changed. Use setter_callbacks to react to user actions, e.g. setting the
        lights On could fire some GPIO code to turn on a LED (see pyhap/accessories/LightBulb.py).
        """
        print('Temperature changed to: ', value)

    @Accessory.run_at_interval(3)  # Run this method every 3 seconds
    # The `run` method can be `async` as well
    def run(self):
        """We override this method to implement what the accessory will do when it is
        started.

        We set the current temperature to a random number. The decorator runs this method
        every 3 seconds.
        """
        while not i2c.try_lock():
            pass

        self.temp_char.set_value(self.si7021.temperature)
        i2c.unlock()
    # The `stop` method can be `async` as well
    def stop(self):
        """We override this method to clean up any resources or perform final actions, as
        this is called by the AccessoryDriver when the Accessory is being stopped.
        """
        print('Stopping accessory.')


def get_bridge():
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(display_name="HomeController", mac=generate_mac(), pincode=b"203-23-999")

    outlet1 = WebPowerOutlet("Christmas Lights", 1)
    outlet5 = WebPowerOutlet("Christmas Tree", 7)

    temp = TemperatureSensor("Temperature Sensor")
    #temp = BMP180("Temperature Sensor")

    bridge.add_accessory(outlet1)
    bridge.add_accessory(outlet5)
    #bridge.add_accessory(temp)

    return bridge

def main():
    bridge = get_bridge()
    driver = AccessoryDriver(bridge, port=51826,persist_file="/home/drydyk/accessory.state")
    # signal.signal(signal.SIGINT, driver.signal_handler) optional
    # signal.signal(signal.SIGTERM, driver.signal_handler) optional
    driver.start()

if __name__ == '__main__':
	main()