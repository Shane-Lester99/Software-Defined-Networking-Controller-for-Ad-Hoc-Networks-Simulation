from stat_manager import StatManager
import grid
import graph
import json
from datetime import datetime
import random

def run_cli_in_main():
    """
    This will run a test so that the user can query from the command line to
    debug the backend
    """
    print("This is the CLI version of the Network Routing Simulation.")
    entry = NetworkSimulationEntryPoint()
    while True:
        x = input("Would you like to build a random graph. (Y/N):")
        if x == "y" or x == "Y":
            print("\nTo set up the network topology, write a list of 1 to 8 numbers.")
            print("Each number signifies how many user devices are associated with that base station.\n")
            bs_str = input("Please enter these numbers now as a comma seperated list:")
            bs_list = [int(char) for char in bs_str if char != ","]
            chan_amount_str = input("Please enter an amount of channels between 4 and 10:")
            chan_amount = int(chan_amount_str)
            entry.run_cli_instance(bs_list, chan_amount)
        else:
            break
        entry.reset_graph()
    print("Goodbye.")

class NetworkSimulationEntryPoint:
    """
    Entry point of NetworkSimulation application. It provides an 
    interface over the application modules and returns the results as JSON.
    It also allows for backend debugging with a CLI version of the application.
    Lastly, it collects the stats for each run.
    
    To run the CLI version run the module from the main function
    """
    
    def __init__(self):
        self._stat_manager = StatManager()
        self._entry_grid = None
        self.entry_graph = None
        
    def retrieve_random_graph_as_json(self, bs_list= None, channel_amount= None):
        """
        For the initialization function call of the API. This function will return
        the random graph that will remain static after initialization.
        JSON is of form:
        {
            "channels": [0.91,0.33,...]
            "graph": {
                "R02": {
                    "metadata": {
                        base_station_name: "B02",
                        base_station_coordinates: [6,9],
                        node_coordinates: [4,8]
                    },
                    "edges" : {
                        "R03" : {
                            "id": <int>,
                            "weight": <float>,
                            "channels": <List>
                        }, ...
                    }
                }
            }
        }
        """
        if not self._entry_grid and not self.entry_graph:
            self._entry_grid = grid.Grid(bs_list)
            self.entry_graph = graph.RoutingSystemMasterGraph(self._entry_grid.device_data,
                                                              self._entry_grid.TRANSMISSION_RADIUS,
                                                              channel_amount)
        CHANNEL_KEY = "channels"
        GRAPH_KEY = "graph"
        json_dict = {CHANNEL_KEY: self.entry_graph.channels.channels, GRAPH_KEY: {}}
        for node_name, entries in self.entry_graph.graph.items():
            metadata = entries[0]
            connected_edges = entries[1]
            string_connected_edges = [node_name for node_name in connected_edges]
            json_dict[GRAPH_KEY][node_name] = {
                 "metadata": {
                     "base_station_name": metadata.base_station_name,
                     "base_station_coordinates": metadata.base_station_coordinates,
                     "node_coordinates": metadata.routable_device_coordinates
                 },
                 "edges": string_connected_edges
            }
        return json.dumps(json_dict)
        
    def reset_graph(self):
        self._entry_grid = None
        self.entry_graph = None
        
    def get_reachable_nodes_as_json(self, node_label):
        """
        Querys all the nodes that can be reached from a node label
        """
        return json.dumps(self.entry_graph.get_reachable_nodes(node_label))
            
    def run_cli_instance(self, bs_list, channel_amount):
        """
        This will allow the user to run the app as a cli without the use of the API. 
        THe user can write queries on the command line and once they exit they
        will retrieve the system output stats. The purpose of this function is
        for backend debugging.
        """
        self.retrieve_random_graph_as_json(bs_list, channel_amount)
        print(self._entry_grid)
        print(self.retrieve_random_graph_as_json())
        while True:
            exit_string = input("Would you like to specify a query path (Y/N):")
            if exit_string == "N" or exit_string == "n":
                print("\nSystem Stats:\n")
                print("\t", self.retrieve_system_results_as_json(), end="\n\n")
                break
            x = input("Please specify query path in form <device_id_1><device_id2>:")
            source, dest = x[:3], x[3:]
            print(self.retrieve_query_results_as_json(source, dest))
    
    def retrieve_query_results_as_json(self, source_node, dest_node):
        """
        The API allows for running a single query, and this will be the output.
        """
        route = self.entry_graph.retrieve_optimal_path_and_allocate_channels(
                                                                    source_node,
                                                                    dest_node)
        number_of_channels = len(self.entry_graph.channels.channels)
        number_of_nodes = len(self.entry_graph)
        number_of_hops = len(route) - 1
        number_of_switches = len(set([channel for channels_used in route.values()
                                 for channel in channels_used]))
        if route:
            self._stat_manager.collect_stats_from_route_data(number_of_channels,
                                                             number_of_nodes,
                                                             number_of_hops,
                                                             number_of_switches)
        return json.dumps(route)
   
   
    def retrieve_system_results_as_json(self):
        return json.dumps(self._stat_manager.stats)
        
        
    def generate_metrics_report(self):
        """
        This method will generate a large amount of graphs and a large amount of
        queries to collect a lot of system stats to collect metrics on 
        routing interarrival rates.
        
        The algorithm works like this:
        
        start with 5 nodes to one base station
        allow for 6, 8, 10 channels on it
        query a random node in that graph to a random reachable value 5 times

        do this same algorithm for 1 - 8 base stations each with 5 nodes to a
        a base station.
        
        In total this will generate 8 * 5 * 3 * 5 = 600 queries to generate
        stable state routing data. However, a lot of those might not have worked,
        so the ceiling is 600 but will be less then that
        """
        self._stat_manager.reset()
        successful_queries = 0
        
        queryId = 0
        node_amounts = [[5] * i for i in range(1,9)]
        channel_amount = [6, 8, 10]
        for bs_list in node_amounts:
            for chan in channel_amount:
                self._entry_grid = grid.Grid(bs_list)
                self.entry_graph = graph.RoutingSystemMasterGraph(self._entry_grid.device_data,
                                                                  self._entry_grid.TRANSMISSION_RADIUS,
                                                                  chan)
                for _ in range(5):
                    # Generate a random node that has at least one edge
                    queryId += 1
                    try:
                        print(self.entry_graph.graph.items())
                        random_node =  random.choice([node_label for node_label, node_values in self.entry_graph.graph.items() if node_values[1]])
                    except IndexError:
                        continue
                    reachable_nodes = self.entry_graph.get_reachable_nodes(random_node)
                    print(random_node)
                    random_edge_node = random.choice(reachable_nodes)
                    print(random_edge_node)
                    query = self.retrieve_query_results_as_json(random_node, random_edge_node)
                    if query:
                        print("Query {} success with data: {}".format(queryId, query))
                        successful_queries += 1
                
        print("{} out of 600 queries successful.".format(successful_queries))
        return self.retrieve_system_results_as_json()
    
if __name__ == "__main__":
    """
    Run this file as the entry to envoke the CLI version of this application
    """
    # run_cli_in_main()
    x = NetworkSimulationEntryPoint()
    print(x.generate_metrics_report())