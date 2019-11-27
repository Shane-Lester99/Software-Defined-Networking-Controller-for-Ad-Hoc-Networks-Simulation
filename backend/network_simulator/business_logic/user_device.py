import wireless_element

class UserDevice(wireless_element.WirelessElement):
    def __init__(self, elem_id):
        self.set_id(elem_id)
        self.base_station = ""
        
    def connect(self, base_station):
        self.base_station = base_station
        
    def is_connected(self):
        return "" != self.base_station
        
    def get_base_station(self):
        return self.base_station