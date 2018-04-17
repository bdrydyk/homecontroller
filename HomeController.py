"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal

from pyhap.accessories.WebPowerOutlet import WebPowerOutlet
from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver

from pyhap.accessories.BMP180 import BMP180

logging.basicConfig(level=logging.INFO)


def get_bridge():
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(display_name="HomeController")
    outlet1 = WebPowerOutlet("Christmas Lights", 1)

    bridge.add_accessory(outlet1)

    outlet5 = WebPowerOutlet("Living Room Lights", 5)

    bridge.add_accessory(outlet5)


    temp = BMP180("Temperature Sensor")
    bridge.add_accessory(temp)

    # Uncomment if you have RPi module and want a LED LightBulb service on pin 16.
    # from pyhap.accessories.LightBulb import LightBulb
    # bulb = LightBulb("Desk LED", pin=16)
    # bridge.add_accessory(bulb)
    return bridge


def get_accessory():
    """Call this method to get a standalone Accessory."""
    acc = WebPowerOutlet("Living Room Light")
    return acc


acc = get_bridge()  # Change to get_bridge() if you want to run a Bridge.

# Start the accessory on port 51826
driver = AccessoryDriver(acc, port=51826)
# We want KeyboardInterrupts and SIGTERM (kill) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGINT, driver.signal_handler)
signal.signal(signal.SIGTERM, driver.signal_handler)
# Start it!
driver.start()
