from channel import Channels
from collections import namedtuple, defaultdict
from priority_queue import PriorityQueue
from datetime import datetime

create_best_route = namedtuple("BestRoute", "cost best_route")
create_stat_package = namedtuple("StatPackage", "cost best_route exp_results")

def change_coor_to_key(coor_pair):
    return str(coor_pair[0]) + "_" + str(coor_pair[1])

class RoutingSystemMasterGraph:
    """
    Routing system graph. The graph is fed data by a base_station_map (which 
    contains coordinates and a transmission radius) so that a graph can be 
    generated. Once the graph is generated it can run routing simulations given
    a source node and a destination node.
    """
    
    def __init__(self, base_station_map, transmission_radius, channel_amount):
        # Adj list is of form {device_name: (metadata, {some_connected_node: channel_node})}
        # where the metadata contains the base station, base station coord, and the
        # router coordinates, and the dictionary is the edges connected to the device.
        # The channel represents the weight of the edge
        self.channels = Channels(channel_amount, transmission_radius)
        # clogged_at_node is a global interference map. It defaults to
        # -1, -1 as the coordinates and a list with no channels. Once
        # we run a route, we will have a user device which maps to the
        # coordinates and to the channels that have interference
        self._clogged_at_node = defaultdict(lambda: [[-1,-1], []])
        self._transmission_radius = transmission_radius
        self.graph = self._generate_graph(base_station_map)
        # timestamp is key with output data as value
        self.sys_stats = {}
    
    def __repr__(self):
        repr_str = "***Graph of Network Routing System***\n"
        for source_device_name, edges in self.graph.items():
            bs_name = self.graph[source_device_name][0].base_station_name
            # Router is connected to base station -> ...
            repr_str = (repr_str + source_device_name
                + " connected to {} -> ".format(bs_name))
            # ... Edges and channel weights:
            repr_str = (repr_str + str(["(DeviceName:{})".format(dest_device_name) 
                for (dest_device_name) in edges[1]]) + "\n")
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
            create_device_entry = namedtuple("RoutableDeviceEntry",
            "base_station_name base_station_coordinates routable_device_coordinates")
            for routable_device in base_station_map[base_station_name].routable_devices:
                adj_list[routable_device.routable_device_name] = \
                    (create_device_entry(
                        base_station_name,
                        base_station_map[base_station_name].base_station_coordinates,
                        routable_device.coordinates
                    ), set(),)
        # Now add in all the edges to the adjacency list so we will have:
        # adj_list = {RoutableDeviceName: (RoutableDeviceEntry(),
        # [{connected_router: channel_edge}])}
        for router_name_source in adj_list.keys():
            for router_name_destination in adj_list.keys():
                if router_name_destination != router_name_source:
                    coord_source = adj_list[router_name_source][0].routable_device_coordinates
                    coord_dest = adj_list[router_name_destination][0].routable_device_coordinates
                    if self._scan_area_for_connected_devices(coord_source, coord_dest):
                        adj_list[router_name_source][1].add(router_name_destination)
                        adj_list[router_name_destination][1].add(router_name_source)
        return adj_list  
        
    def _scan_area_for_connected_devices(self, coord_source, coord_dest):
        return (True if abs(coord_source[0] - coord_dest[0]) <= self._transmission_radius and
                abs(coord_source[1] - coord_dest[1]) <= self._transmission_radius else False)
                
        
    def retrieve_optimal_path_and_allocate_channels(self, source, dest):
        """
        This will retrieve the optimal path using this algorithm:
        - Find all the paths such that they are the minimum amount of hops with
            no global interference or they have less hops then that amount but
            have global interference
        - From those paths, use the Channels.find_cheapest_channels_for_path which
            will map channel ids on to the edges of the graph such that interarrival
            rate at those channels is minimal
        - Update the global interference list to allow the system to know that those
            channels are now clogged
        """
        candidate_path_pq = self._find_candidate_paths(source, dest)
        if not candidate_path_pq:
            return {}
        # TODO: we shouldn't just pop the first path, we need to modify the scheme
        # so we try some amount of paths with minumum interference and the one
        # with the minimum amount of hops
        while candidate_path_pq:
            chosen_path_nodes = candidate_path_pq.pop_task()[1]
            chosen_path_coordinates = [self.graph[node][0].routable_device_coordinates 
                                       for node in chosen_path_nodes]
            global_blockage = self.channels.find_cheapest_channels_for_path(self._clogged_at_node,
                                                                            chosen_path_coordinates)
            if global_blockage:
                break
            
        if not global_blockage:
            return {}
       
        path_chosen_data = defaultdict(list)
        for blocked_chan_record in global_blockage:
            chan_coor = change_coor_to_key(blocked_chan_record.chan_coor)
            chan_used = blocked_chan_record.chan_used
            path_chosen_data[chan_coor].append(chan_used)
        output_route = dict()
        for node in chosen_path_nodes:
            coors = self.graph[node][0].routable_device_coordinates
            chan_used = path_chosen_data[change_coor_to_key(coors)]
            self._clogged_at_node[node][0] = coors
            self._clogged_at_node[node][1].extend(chan_used)
            output_route[node] = chan_used
        return output_route
    
    def _find_candidate_paths(self, source, dest):
        """
        create a Priority Queue of all the paths between source and dest. Weigh
        the priority queue this way:
        - The base number is the amount of hops as a float (e.g. 4.0)
        - if there is channel interference add 0.5 to that base number
        - Filter the priority queue to only contain the first integer number and
            all values less.
        E.g. 2.5,2.5,3,3.5,3.5,4,4 will output (2.5,2.5,and 3) as either one of the
        shorter paths with global channel interference will be cheapest or the 3 hop
        path without channel interference. Note that all keys bigger then 3 in this
        example can't be cheaper then 3 hops.
        E.g. 3,3,3.5,4.5,4.5 will output the first 3 only because it has no channel
        interferences and is the lowest amount of hops so we know it will be the
        cheapest
          We find all the paths of a undirected graph with cycles by:
        - Running a dfs, where we store paths in the stack
        - We add a value to a path in a stack if that connected edge isn't already in
            path
        """
        def calc_interference(node_path):
            """
            We will add total_path_interference / 100 to the the path value
            """
            # node_coordinates = change_coor_to_key(
            #                     self.graph[node_label].routable_device_coordinates
            #                   )
            blockage_sum = 0
            channel_list = list()
            for node_label in node_path:
                if self._clogged_at_node.get(node_label):
                    channels_used = self._clogged_at_node[node_label][1]
                    channel_list.extend([self.channels.channels[chan_num] 
                                         for chan_num in 
                                         self._clogged_at_node[node_label][1]])
            return sum(channel_list) / 1000
        if source not in self.graph or dest not in self.graph:
            return list()
        # visited = {node_name: False for node_name in self.graph.keys()}
        stack = list()
        stack.append([source])
        output = PriorityQueue()
        while stack:
            curr_path = stack.pop()
            if len(curr_path) > 7:
                continue
            if curr_path[len(curr_path)-1] == dest:
                path_value = float(len(curr_path) - 1) + calc_interference(curr_path)
                output.add_task((path_value, curr_path))
                continue
            for connected_node in self.graph[curr_path[len(curr_path)-1]][1]:
                if connected_node not in curr_path:
                    temp_curr_path = curr_path.copy()
                    temp_curr_path.append(connected_node)
                    stack.append(temp_curr_path)
        return output