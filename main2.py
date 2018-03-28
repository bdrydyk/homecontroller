"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal

from pyhap.accessories.TemperatureSensor import TemperatureSensor
from pyhap.accessories.WebPowerOutlet import WebPowerOutlet
from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver

from webpower import WebPowerSwitch

logging.basicConfig(level=logging.INFO)

### WEB Power Stuff ##
def set_web_power(hexstr):
    w = WebPowerSwitch()
    w.set_outlet_states(hexstr)
    res = w.get_hex_states()
    return(str(res))

def set_outlet(outlet=None,state=None):
    w = WebPowerSwitch()
    states = w.get_outlet_states()

    if outlet ==None and state==None:
        return(jsonify(states))

    if outlet != None:
        if outlet == "set":
            res = w.set_outlet_states(state)
            return(jsonify(res))
        elif outlet == "cycle":
            res = w.cycle_outlet_states(state)
            return(jsonify(res))
        else:
            try:
                assert 1 <= int(outlet) <= 8, "outlet number not valid"
            except:
                abort(401)

            outlet = int(outlet)
            outlet_index = outlet-1

            if state == None:
                res = w.outlets[outlet_index]
                return(jsonify(res))
            else:
                if state == "ON":
                    state=True
                elif state == "OFF":
                    state=False
                else:
                    abort(401)
                res = w.set_outlet(str(outlet),state)
                return(jsonify(res))




def get_bridge():
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(display_name="Bridge")
    temp_sensor = TemperatureSensor("Termometer")
    temp_sensor2 = TemperatureSensor("Termometer2")
    bridge.add_accessory(temp_sensor)
    bridge.add_accessory(temp_sensor2)

    # Uncomment if you have RPi module and want a LED LightBulb service on pin 16.
    # from pyhap.accessories.LightBulb import LightBulb
    # bulb = LightBulb("Desk LED", pin=16)
    # bridge.add_accessory(bulb)
    return bridge


def get_accessory():
    """Call this method to get a standalone Accessory."""
    acc = WebPowerOutlet("MyFirstOutlet")
    return acc


acc = get_accessory()  # Change to get_bridge() if you want to run a Bridge.

# Start the accessory on port 51826
driver = AccessoryDriver(acc, port=51826)
# We want KeyboardInterrupts and SIGTERM (kill) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGINT, driver.signal_handler)
signal.signal(signal.SIGTERM, driver.signal_handler)
# Start it!
driver.start()
