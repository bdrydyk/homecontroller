from pyhap.accessory import Accessory, Category
import pyhap.loader as loader

import requests
import csv
import os
import logging
import sched, time
import re, binascii

#ON OFF CCL
BASE_URL = "http://admin:seebeck10@10.0.1.67/"
STATE_STR= "<!-- state=ef lock=e6 -->"
OUTLET = 1

class WebPowerOutlet(Accessory):
    """docstring for Outlet"""

    category = Category.LIGHTBULB

    def __init__(self, display_name, outlet=None, aid=None, mac=None, pincode=None, iid_manager=None, setup_id=None):
        super(WebPowerOutlet, self).__init__(display_name, aid=None, mac=None, pincode=None, iid_manager=None, setup_id=None)

        self.base_url = "http://admin:seebeck10@10.0.1.67/"
        self.outlets = [False,False,False,False,False,False,False,False]
        self.outlet = outlet
        #self.get_outlet_states()
        print("Outlet: {}".format(self.outlet))
        print("outlet states: {}".format(self.outlets))

    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_outlet(self, value):

        if value:
            state=True
            #GPIO.output(self.pin, GPIO.HIGH)
            print("Setting High")
        else:
            state=False
            # GPIO.output(self.pin, GPIO.LOW)
            print("Setting Low")

        res = self.set_outlet_state(str(self.outlet),state)

    def _set_services(self):
        super(WebPowerOutlet, self)._set_services()

        outlet_service = loader.get_serv_loader().get("Outlet")
        self.add_service(outlet_service)
        outlet_service.get_characteristic("On").setter_callback = self.set_outlet
        
    def stop(self):
        """We override this method to clean up any resources or perform final actions, as
        this is called by the AccessoryDriver when the Accessory is being stopped (it is
        called right after run_sentinel is set).
        """
        print("Stopping accessory.")

    def int_to_bit_list(self,h):
        states = []
        for i in reversed(bin(h)[2:].zfill(8)):
            states.append(bool(int(i)))
        return states

    def str_to_int(self,hex_str):
        return int(hex_str, 16)

    def str_to_bit_list(self,hex_str):
        return self.int_to_bit_list(self.str_to_int(hex_str))

    def get_hex_state(self):
        r = requests.get(self.base_url + 'index.htm')
        m = re.search("<!-- state=(\S\S) lock=(\S\S) -->",r.text)
        print("Hex state: {}".format(m.group(1)))
        return(m.group(1))

    def set_outlet_state(self,outlet,state):
        if state == True:
            state="ON"
        elif state == False:
            state="OFF"
        print("Setting outlet {}: {}".format(str(outlet),state))
        requests.get(self.base_url + "outlet", params={str(outlet):state})
        return self.get_outlet_states()

    def get_outlet_states(self):
        self.outlets = self.str_to_bit_list(self.get_hex_state())
        return self.outlets

    def set_outlet_states(self,hex_str):
        new_states = self.str_to_bit_list(hex_str)
        current_states = self.get_outlet_states()

        print("current\t\t: {}".format(current_states))
        print("new\t\t: {}".format(new_states))
        
        for i,v in enumerate(new_states):
            v = bool(int(v))
            outlet_num = int(i) + 1
            print("{} == {}".format(bool(current_states[i]), v))
            if v != bool(current_states[i]):
                print("asking outlet num {} to be {}".format(outlet_num,v))
                self.set_outlet(outlet_num,v)
        return(self.get_outlet_states())

    def cycle_outlet_states(self,hex_str):

        swap_states = self.str_to_int(hex_str)
        current_states = self.str_to_int(self.get_hex_state())
        new_states = swap_states ^ current_states
        print("cycle states: {}".format(new_states))
        new_state_str = hex(new_states)[2:]
        res = self.set_outlet_states(new_state_str)
        return(res)


        
#bin(int('ff', base=16))[2:]

### WEB Power Stuff ##
# def set_web_power(hexstr):
#     w = WebPowerSwitch()
#     w.set_outlet_states(hexstr)
#     res = w.get_hex_states()
#     return(str(res))

# def set_outlet(outlet=None,state=None):
#     w = WebPowerSwitch()
#     states = w.get_outlet_states()


#     if outlet != None:
#         if outlet == "set":
#             res = w.set_outlet_states(state)
#             return(jsonify(res))
#         elif outlet == "cycle":
#             res = w.cycle_outlet_states(state)
#             return(jsonify(res))
#         else:
#             try:
#                 assert 1 <= int(outlet) <= 8, "outlet number not valid"
#             except:
#                 abort(401)

#             outlet = int(outlet)
#             outlet_index = outlet-1

#             if state == None:
#                 res = w.outlets[outlet_index]
#                 return(jsonify(res))
#             else:
#                 if state == "ON":
#                     state=True
#                 elif state == "OFF":
#                     state=False
#                 else:
#                     abort(401)
#                 res = w.set_outlet(str(outlet),state)
#                 return(jsonify(res))




