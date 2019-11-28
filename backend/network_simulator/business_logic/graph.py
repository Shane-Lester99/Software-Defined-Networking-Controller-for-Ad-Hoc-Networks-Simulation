import channel
from collections import namedtuple

class RoutingSystemMasterGraph:
    
    def __init__(self, base_station_map):
        self.graph = self._generate_graph(base_station_map) 
    
    def __repr__(self):
        return ""
        
    def _generate_graph(self, base_station_map):
        adj_list = {}
        for base_station_name in base_station_map:
            # flatten list of all routers to start with router, base_station
            create_device_entry = namedtuple("RotaubleDeviceEntry",
            "base_station_name base_station_coordinates routable_device_coordinates")
            for routable_device in base_station_map[base_station_name].routable_devices:
                adj_list[routable_device.routable_device_name] = \
                    create_device_entry(
                        base_station_name,
                        base_station_map[base_station_name].base_station_coordinates,
                        routable_device.coordinates
                    )
                
    def find_shortest_path(self, device_1, device_2):
        pass
    
    def output_system_stats(self):
        pass
    
    