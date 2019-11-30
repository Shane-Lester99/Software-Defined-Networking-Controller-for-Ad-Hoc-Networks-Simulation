import channel
from collections import namedtuple
from priority_queue import PriorityQueue

create_best_route = namedtuple("BestRoute", "cost best_route")

class RoutingSystemMasterGraph:
    
    def __init__(self, base_station_map, transmission_radius):
        # Adj list is of form {device_name: (metadata, {some_connected_node: channel_node})}
        # where the metadata contains the base station, base station coord, and the
        # router coordinates, and the dictionary is the edges connected to the device.
        # The channel represents the weight of the edge
        self._global_channel_id = 1
        self._transmission_radius = transmission_radius
        self._graph = self._generate_graph(base_station_map)
        self.sys_stats = list()
    
    def __repr__(self):
        repr_str = "***Graph of Network Routing System***\n"
        for source_device_name, edges in self._graph.items():
            bs_name = self._graph[source_device_name][0].base_station_name
            # Router is connected to base station -> ...
            repr_str = (repr_str + source_device_name
                + " connected to {} -> ".format(bs_name))
            # ... Edges and channel weights:
            repr_str = (repr_str + str(["(DeviceName:{}, ChannelId:{}, ChannelWeight:{})".format(
                                                                  dest_device_name,
                                                                  channel.c_id,
                                                                  channel.channel_weight) 
                for (dest_device_name, channel) in edges[1].items()]) + "\n")
        return repr_str
        
    
    
    def query_for_optimal_route(self, device_name_source, device_name_dest):
        """
        Finds the shortest path between the source and destination by first
        running a breadth first search to create a set of all the reachable nodes.
        If the destination is there we can run the shortest path on this subset
        of the graph. We can then return a data structure containing all the 
        stats from this run and save it in our system stats.
        """
        reachable_nodes_set = self._bfs(device_name_source)
        if device_name_dest not in reachable_nodes_set:
            return create_best_route(-1, None)
        graph_subset = ({key: value for (key, value) in self._graph.items()
                          if key in reachable_nodes_set})
        # If we have paths that exist for this query, then we will use this
        # subset of the graph for our shortest path algorithm
         
        # This will feed our shortest path algorithm only the needed graph subset
        # Which will make dijkstra more straightfoward to implement
        
        best_route = self._calc_shortest_path(graph_subset,
                                              device_name_source,
                                              device_name_dest)
        if best_route.best_route:
            output_stats = self._run_simulation(best_route)
            self.sys_stats.append(output_stats)
            return output_stats
        return []

    def output_system_stats(self):
        return self.sys_stats
    
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
                        device_channel = channel.ChannelSystemNode(self._global_channel_id)
                        self._global_channel_id += 1
                        adj_list[router_name_source][1][router_name_destination] = device_channel
                        adj_list[router_name_destination][1][router_name_source] = device_channel
        return adj_list  
        
    def _scan_area_for_connected_devices(self, coord_source, coord_dest):
        return (True if abs(coord_source[0] - coord_dest[0]) <= self._transmission_radius and
                abs(coord_source[1] - coord_dest[1]) <= self._transmission_radius else False)
                
    def _bfs(self, node):
        """
        Runs breadth first search on a graph node to see all reachable nodes.
        Will then return a set with all the reachabe nodes
        """
        if node not in self._graph:
            return set()
        reachable_nodes = set()
        visited = {node_name: False for node_name in self._graph.keys()}
        queue = [node]
        visited[node] = True
        while queue:
            curr_node = queue.pop()
            reachable_nodes.add(curr_node)
            for pot_new_node in self._graph[curr_node][1]:
                if visited[pot_new_node] == False:
                    queue.append(pot_new_node)
                    visited[pot_new_node] = True
        return reachable_nodes 
        
    def _calc_shortest_path(self, graph_subset, source_node, dest_node):
        """
        Runs the shortest path algorithm on a graph subset. Outputs a list of the
        best path. Assume our graph subset is all nodes reachable from our source and
        our destination node is one of them
        """
        def create_input_for_pq(node_1, node_2):
            return (graph_subset[node_1][1][node_2].channel_weight, node_2)
        # Creating the initial data structure of {node: {distance_from_source: <float>,
        # prev_node: <str>}} and other ds for dijkstra
        DISTANCE_KEY = "shortest_distance_from_source"
        PREVIOUS_VERTEX_KEY = "previous_vertex"
        shortest_path_info = ({device_names: {DISTANCE_KEY: float("inf"), 
            PREVIOUS_VERTEX_KEY: None} for device_names in graph_subset.keys()})
        visited = {key:False for key in graph_subset.keys()}
        shortest_path_info[source_node][DISTANCE_KEY] = 0
        visited[source_node] = True
        # Begin dijkstra
        pq = PriorityQueue()
        pq.add_task((0.0, source_node))
        while pq:
            new_node = pq.pop_task()[1]
            visited[new_node] = True
            for connected_node in graph_subset[new_node][1]:
                if not visited[connected_node]:
                    pq_input = create_input_for_pq(new_node, connected_node)
                    new_dist = pq_input[0] + shortest_path_info[new_node][DISTANCE_KEY]
                    if new_dist < shortest_path_info[connected_node][DISTANCE_KEY]:
                        shortest_path_info[connected_node][DISTANCE_KEY] = new_dist
                        shortest_path_info[connected_node][PREVIOUS_VERTEX_KEY] = new_node
                    pq.add_task(pq_input)
        # Checks if ther is an optimal path (There always should be one)
        if shortest_path_info[dest_node][PREVIOUS_VERTEX_KEY] != None:
            best_route = create_best_route(
                          shortest_path_info[dest_node][DISTANCE_KEY],
                          [dest_node]
                        )
            curr_node = shortest_path_info[dest_node][PREVIOUS_VERTEX_KEY]
            while True:
                best_route.best_route.append(curr_node)
                if curr_node == source_node:
                    break
                curr_node = shortest_path_info[curr_node][PREVIOUS_VERTEX_KEY]
            best_route.best_route.reverse()
        else:
            # In case of bugs or unexpected behavior, this will make it easier to
            # debug. This should never execute
            best_route = create_best_route(-1, None)
        return best_route
    
    def _run_simulation(self, best_route):
        """
        Runs a single routing simulation given a shortest path and outputs the stats of
        that path being taken (i.e. what channels are used and the results of
        the selected channels)
        Our stats data structure will be:
        [RouteData(nodes:(node_1, node_2), channel:channel_string,
            channel_data:channels_selection), ...]
        """
        def get_channel_obj(source, dest):
            """
            Given two adjacent nodes, return there edge (which is a channel obj)
            """
            return self._graph[source][1][dest]
        results = list()
        output_stat_record = namedtuple("RouteData", "nodes channel channel_selection")
        prev_node = best_route.best_route[0]
        for next_node_id in range(1, len(best_route.best_route)):
            next_node = best_route.best_route[next_node_id]
            chan = get_channel_obj(prev_node, next_node)
            curr_test = output_stat_record((prev_node, next_node), chan, [])
            sel = chan.choose_channel_and_report_result()
            curr_test.channel_selection.append(sel)
            while not sel.had_success:
                sel = chan.choose_channel_and_report_result()
                curr_test.channel_selection.append(sel)
            results.append(curr_test)
            prev_node = next_node
        return results
    
    
    