class RoutingSystemMasterGraph:
    
    def __init__(self, base_station_map):
        self.graph = self._generate_graph(base_station_map) 
    
    def __repr__(self):
        return ""
        
    def _generate_graph(self, base_station_map):
        print(base_station_map)
    
    def find_shortest_path(self, device_1, device_2):
        pass
    
    def output_system_stats(self):
        pass