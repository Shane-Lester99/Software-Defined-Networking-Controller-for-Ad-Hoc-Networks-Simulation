import channel
from collections import namedtuple
from priority_queue import PriorityQueue

class RoutingSystemMasterGraph:
    
    def __init__(self, base_station_map, transmission_radius):
        # Adj list is of form {device_name: (metadata, {some_connected_node: channel_node})}
        # where the metadata contains the base station, base station coord, and the
        # router coordinates, and the dictionary is the edges connected to the device.
        # The channel represents the weight of the edge
        self._transmission_radius = transmission_radius
        self._graph = self._generate_graph(base_station_map)
    
    def __repr__(self):
        repr_str = "***Graph of Network Routing System***\n"
        for source_device_name, edges in self._graph.items():
            bs_name = self._graph[source_device_name][0].base_station_name
            # Router is connected to base station -> ...
            repr_str = (repr_str + source_device_name
                + " connected to {} -> ".format(bs_name))
            # ... Edges and channel weights:
            repr_str = (repr_str + str(["(DeviceName:{}, ChannelWeight:{})".format(
                                                                  dest_device_name,
                                                                  channel.report_weight()) 
                for (dest_device_name, channel) in edges[1].items()]) + "\n")
        return repr_str
        
    def _generate_graph(self, base_station_map):
        """
        Generates the adjanency list used to model the graph for the network
        routing system. 
        """
        # Create adj list beginning structure of adj_list = {routable_name: 
        # RoutableDeviceEntry(base_station_name, base_station_coordinates,
        # routable_device_coordinated)}
        adj_list = {}
        for base_station_name in base_station_map:
            create_device_entry = namedtuple("RotaubleDeviceEntry",
            "base_station_name base_station_coordinates routable_device_coordinates")
            for routable_device in base_station_map[base_station_name].routable_devices:
                adj_list[routable_device.routable_device_name] = \
                    (create_device_entry(
                        base_station_name,
                        base_station_map[base_station_name].base_station_coordinates,
                        routable_device.coordinates
                    ), {},)
        # Now add in all the edges to the adjacency list so we will have:
        # adj_list = {RoutableDeviceName: (RoutableDeviceEntry(),
        # [{connected_router: channel_edge}])}
        for router_name_source in adj_list.keys():
            for router_name_destination in adj_list.keys():
                if router_name_destination != router_name_source:
                    coord_source = adj_list[router_name_source][0].routable_device_coordinates
                    coord_dest = adj_list[router_name_destination][0].routable_device_coordinates
                    if self._scan_area_for_connected_devices(coord_source, coord_dest):
                        device_channel = channel.ChannelSystemNode()
                        adj_list[router_name_source][1][router_name_destination] = device_channel
                        adj_list[router_name_destination][1][router_name_source] = device_channel
        return adj_list  
    
    
    def find_shortest_path(self, device_name_source, device_name_dest):
        # First: Find all reacable nodes using breadth first search of the graph,
        # if source -> dest isnt there then we can return here
        
        
        # This will return all the reachable nodes in a set data structure
        reachable_nodes = self._bfs(device_name_source)
        if device_name_dest not in reachable_nodes:
            return None
        
        return 1
        
        
        DISTANCE_KEY = "shortest_distance_from_source"
        PREVIOUS_VERTEX_KEY = "previous_vertex"
        distance_from_start = 0
        shortest_path_info = ({device_names: {DISTANCE_KEY: float("inf"), 
            PREVIOUS_VERTEX_KEY: None} for device_names in self._graph.keys()})
        shortest_path_info[device_name_source][DISTANCE_KEY] = 0
        for device_entries in self._graph.values():
            device_data = device_entries[1]
            for device_name, channel_node in device_data.items():
                print(device_name, channel_node.report_weight(), end='\n\n')
        # print('here')
        # print([value[1], value[1].total_weight for value in self._graph.values()])
        # pq = PriorityQueue([(channel_weight, )])
        

    def output_system_stats(self):
        pass
    
    def _scan_area_for_connected_devices(self, coord_source, coord_dest):
        return (True if abs(coord_source[0] - coord_dest[0]) <= self._transmission_radius and
                abs(coord_source[1] - coord_dest[1]) <= self._transmission_radius else False)
                
    def _bfs(self, node):
        """
        Runs breadth first search on a graph node to see all reachable nodes.
        Will then return a set with all the reachabe nodes
        """
        reachable_nodes = set()
        visited = {node_name: False for node_name in self._graph.keys()}
        queue = [node]
        visited[node] = True
        while queue:
            curr_node = queue.pop()
            if curr_node != node:
                reachable_nodes.add(curr_node)
            for pot_new_node in self._graph[curr_node][1]:
                if visited[pot_new_node] == False:
                    queue.append(pot_new_node)
                    visited[pot_new_node] = True
        return reachable_nodes 
    