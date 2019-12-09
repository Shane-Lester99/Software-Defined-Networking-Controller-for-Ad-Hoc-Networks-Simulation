from channel import Channels
from collections import namedtuple
from priority_queue import PriorityQueue
from datetime import datetime

create_best_route = namedtuple("BestRoute", "cost best_route")
create_stat_package = namedtuple("StatPackage", "cost best_route exp_results")

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
        self._global_interference = []
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
        
    # def query_for_optimal_route(self, device_name_source, device_name_dest):
    #     """
    #     Finds the shortest path between the source and destination by first
    #     running a breadth first search to create a set of all the reachable nodes.
    #     If the destination is there we can run the shortest path on this subset
    #     of the graph. We can then return a data structure containing all the 
    #     stats from this run and save it in our system stats.
    #     """
    #     reachable_nodes_set = self._bfs(device_name_source)
    #     if device_name_dest not in reachable_nodes_set:
    #         failed_exp_time = str(datetime.now())
    #         return failed_exp_time, -1
    #     graph_subset = ({key: value for (key, value) in self.graph.items()
    #                       if key in reachable_nodes_set})
    #     # If we have paths that exist for this query, then we will use this
    #     # subset of the graph for our shortest path algorithm
         
    #     # This will feed our shortest path algorithm only the needed graph subset
    #     # Which will make dijkstra more straightfoward to implement
        
    #     best_route = self._calc_shortest_path(graph_subset,
    #                                           device_name_source,
    #                                           device_name_dest)
    #     exp_time = str(datetime.now())
    #     if best_route.best_route:
    #         output_stats = create_stat_package(best_route.cost,
    #                                           best_route.best_route,
    #                                           self._run_simulation(best_route)
    #                                           )
    #         self.sys_stats[exp_time] = output_stats
    #         return exp_time, output_stats
    #     return exp_time, -1
    
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
        # TODO: For now just pick minimum amount of hops, will optimize for 
        # global interference later
        chosen_path_nodes = candidate_path_pq.pop_task()[1]
        chosen_path_coordinates = [self.graph[node][0].routable_device_coordinates 
                                   for node in chosen_path_nodes]
        print(chosen_path_coordinates)
        id_mapping = self.channels.find_cheapest_channels_for_path(self._global_interference,
                                                                   chosen_path_coordinates)
        print(id_mapping)
        return candidate_path_pq
    
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
        def calc_interference():
            # TODO: Fill this in
            return 0.0
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
                path_value = float(len(curr_path) - 1) + calc_interference()
                output.add_task((path_value, curr_path))
                continue
            for connected_node in self.graph[curr_path[len(curr_path)-1]][1]:
                if connected_node not in curr_path:
                    temp_curr_path = curr_path.copy()
                    temp_curr_path.append(connected_node)
                    stack.append(temp_curr_path)
        return output
        
    # def _find_all_paths(self, source, dest):
    #     """
    #     Runs breadth first search on a graph to find all paths between source and
    #     destination. Stores them in a priority queue based on hops and 
    #     """
    #     if node not in self.graph:
    #         return set()
    #     reachable_nodes = set()
    #     visited = {node_name: False for node_name in self.graph.keys()}
    #     queue = [node]
    #     visited[node] = True
    #     while queue:
    #         curr_node = queue.pop()
    #         reachable_nodes.add(curr_node)
    #         for pot_new_node in self.graph[curr_node][1]:
    #             if visited[pot_new_node] == False:
    #                 queue.append(pot_new_node)
    #                 visited[pot_new_node] = True
    #     return reachable_nodes 
        
    # def _calc_shortest_path(self, graph_subset, source_node, dest_node):
    #     """
    #     Runs the shortest path algorithm on a graph subset. Outputs a list of the
    #     best path. Assume our graph subset is all nodes reachable from our source and
    #     our destination node is one of them
    #     """
    #     def create_input_for_pq(node_1, node_2):
    #         return (graph_subset[node_1][1][node_2].channel_weight, node_2)
    #     # Creating the initial data structure of {node: {distance_from_source: <float>,
    #     # prev_node: <str>}} and other ds for dijkstra
    #     DISTANCE_KEY = "shortest_distance_from_source"
    #     PREVIOUS_VERTEX_KEY = "previous_vertex"
    #     shortest_path_info = ({device_names: {DISTANCE_KEY: float("inf"), 
    #         PREVIOUS_VERTEX_KEY: None} for device_names in graph_subset.keys()})
    #     visited = {key:False for key in graph_subset.keys()}
    #     shortest_path_info[source_node][DISTANCE_KEY] = 0
    #     visited[source_node] = True
    #     # Begin dijkstra
    #     pq = PriorityQueue()
    #     pq.add_task((0.0, source_node))
    #     while pq:
    #         new_node = pq.pop_task()[1]
    #         visited[new_node] = True
    #         for connected_node in graph_subset[new_node][1]:
    #             if not visited[connected_node]:
    #                 pq_input = create_input_for_pq(new_node, connected_node)
    #                 new_dist = pq_input[0] + shortest_path_info[new_node][DISTANCE_KEY]
    #                 if new_dist < shortest_path_info[connected_node][DISTANCE_KEY]:
    #                     shortest_path_info[connected_node][DISTANCE_KEY] = new_dist
    #                     shortest_path_info[connected_node][PREVIOUS_VERTEX_KEY] = new_node
    #                 pq.add_task(pq_input)
    #     # Checks if ther is an optimal path (There always should be one)
    #     if shortest_path_info[dest_node][PREVIOUS_VERTEX_KEY] != None:
    #         best_route = create_best_route(
    #                       shortest_path_info[dest_node][DISTANCE_KEY],
    #                       [dest_node]
    #                     )
    #         curr_node = shortest_path_info[dest_node][PREVIOUS_VERTEX_KEY]
    #         while True:
    #             best_route.best_route.append(curr_node)
    #             if curr_node == source_node:
    #                 break
    #             curr_node = shortest_path_info[curr_node][PREVIOUS_VERTEX_KEY]
    #         best_route.best_route.reverse()
    #     else:
    #         # In case of bugs or unexpected behavior, this will make it easier to
    #         # debug. This should never execute.
    #         best_route = create_best_route(-1, None)
    #     return best_route
    
    # def _run_simulation(self, best_route):
    #     """
    #     Runs a single routing simulation given a shortest path and outputs the stats of
    #     that path being taken (i.e. what channels are used and the results of
    #     the selected channels)
    #     Our stats data structure will be:
    #     [RouteData(nodes:(node_1, node_2), channel:channel_string,
    #         channel_data:channels_selection), ...]
    #     """
    #     def get_channel_obj(source, dest):
    #         """
    #         Given two adjacent nodes, return there edge (which is a channel obj)
    #         """
    #         return self.graph[source][1][dest]
    #     results = list()
    #     output_stat_record = namedtuple("RouteData", "nodes channel channel_selection")
    #     prev_node = best_route.best_route[0]
    #     for next_node_id in range(1, len(best_route.best_route)):
    #         next_node = best_route.best_route[next_node_id]
    #         chan = get_channel_obj(prev_node, next_node)
    #         curr_test = output_stat_record((prev_node, next_node), chan, [])
    #         sel = chan.choose_channel_and_report_result()
    #         curr_test.channel_selection.append(sel)
    #         while not sel.had_success:
    #             sel = chan.choose_channel_and_report_result()
    #             curr_test.channel_selection.append(sel)
    #         results.append(curr_test)
    #         prev_node = next_node
    #     return results