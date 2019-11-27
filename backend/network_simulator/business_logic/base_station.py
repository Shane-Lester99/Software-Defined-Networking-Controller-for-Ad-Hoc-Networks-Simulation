import wireless_element

class BaseStation(wireless_element.WirelessElement):
    
    def __init__(self, elem_id):
        self.set_id(elem_id)
        self.connected_devices = []
        
    def connect(self, user_device_id):
        self.connected_devices.append(user_device_id)
        
    def get_connected_devices(self):
        return self.connected_devices