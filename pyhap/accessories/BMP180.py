# An Accessory for the BMP180 sensor.
# This assumes the bmp180 module is in a package called sensors.
# Assume you have a bmp module with BMP180 class with read() method.
#from Sensors import BMP085

from pyhap.accessories.Sensors import BMP085

from pyhap.accessory import Accessory, Category
import pyhap.loader as loader

import smbus
import RPi.GPIO as GPIO


class BMP180(Accessory):

    category = Category.SENSOR

    def __init__(self, *args, **kwargs):
        super(BMP180, self).__init__(*args, **kwargs)

        self.temp_char = self.get_service("TemperatureSensor")\
                             .get_characteristic("CurrentTemperature")

        self.sensor = BMP085(0x77, 1)

    def _set_services(self):
        super(BMP180, self)._set_services()
        self.add_service(
            loader.get_serv_loader().get("TemperatureSensor"))

    def __getstate__(self):
        state = super(BMP180, self).__getstate__()
        state["sensor"] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.sensor = BMP085(0x77, 1)

    def run(self):
        while not self.run_sentinel.wait(30):
            temp  = self.sensor.readTemperature()
            self.temp_char.set_value(temp)
