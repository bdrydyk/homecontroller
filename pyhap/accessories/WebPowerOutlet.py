from pyhap.accessory import Accessory, Category
import pyhap.loader as loader

class WebPowerOutlet(Accessory):
    """Implementation of a mock temperature sensor accessory."""

    category = Category.OUTLET  # This is for the icon in the iOS Home app.

    def __init__(self, *args, **kwargs):
        """Here, we just store a reference to the current temperature characteristic and
        add a method that will be executed every time its value changes.
        """
        # If overriding this method, be sure to call the super's implementation first,
        # because it calls _set_services and performs some other important actions.
        super(WebPowerOutlet, self).__init__(*args, **kwargs)

    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_outlet(self, value):
        if value:
            #GPIO.output(self.pin, GPIO.HIGH)
            print("Setting High")
        else:
            # GPIO.output(self.pin, GPIO.LOW)
            print("Setting Low")

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