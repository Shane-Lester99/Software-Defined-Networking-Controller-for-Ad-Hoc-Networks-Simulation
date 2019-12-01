import grid
import graph
import json
from datetime import datetime

def run_cli_in_main():
    """
    This will run a test so that the user can query from the command line to
    debug the backend
    """
    print("This is the CLI version of the Network Routing Simulation.")
    print("To set up the network topology, write a list of 1 to 9 numbers.")
    print("Each number signifies how many user devices are associated with that base station.\n")
    x = input("Please enter these numbers now as a single space seperated list:")
    bs_list = [int(char) for char in x if char != " "]
    entry = NetworkSimulationEntryPoint(bs_list)
    entry.command_line_test_exp()

class NetworkSimulationEntryPoint:
    """
    Entry point of NetworkSimulation application. It provides an 
    interface over the application modules and returns the results as JSON.
    It also allows for backend debugging with a CLI version of the application.
    
    To run the CLI version run the module from the main function
    """
    
    def __init__(self, base_station_list):
        self._entry_grid = grid.Grid(base_station_list)
        self._entry_graph = graph.RoutingSystemMasterGraph(
            self._entry_grid.device_data,
            self._entry_grid.TRANSMISSION_RADIUS)
            
    def command_line_test_exp(self):
        """
        This will allow the user to run a test without the use of the API. 
        THe user can write queries on the command line and once they exit they
        will retrieve the system output stats. The purpose of this function is
        for backend debugging.
        """
        print(self._entry_grid)
        print(self._entry_graph)
        while True:
            exit_string = input("Would you like to specify a query path (Y/N):")
            if exit_string == "N" or exit_string == "n":
                print(self._entry_graph.sys_stats)
                break
            x = input("Please specify query path in form <device_id_1><device_id2>:")
            source, dest = x[:3], x[3:]
            print(self._entry_graph.query_for_optimal_route(source, dest))
            
    def retrieve_random_graph_as_json(self):
        """
        For the initialization function call of the API. This function will return
        the random graph that will remain static after initialization.
        """
        json_dict = dict()
        for node_name, entries in self._entry_graph.graph.items():
            metadata = entries[0]
            connected_edges = entries[1]
            string_connected_edges = {node_name: str(channel) for node_name,
                                      channel in connected_edges.items()}
            json_dict[node_name] = {
                 "metadata": {
                     "base_station_name": metadata.base_station_name,
                     "base_station_coordinates": metadata.base_station_coordinates,
                     "node_coordinates": metadata.routable_device_coordinates
                 },
                 "edges": string_connected_edges
            }
        return json.dumps(json_dict)
    
    def retrieve_query_results_as_json(self, source_node, dest_node):
        """
        The API allows for running a single query, and this will be the output.
        """
        stat_pkg = self._entry_graph.query_for_optimal_route(source_node, dest_node)
        json_dict = dict()
        json_dict = self._convert_one_query_stat_block_to_json(json_dict, stat_pkg)
        return json.dumps(json_dict)
    
    def retrieve_system_results_as_json(self):
        """
        The API allows for seeing all the results of all the queries.
        """
        json_dict = dict()
        for date_str, stat_pkg in self._entry_graph.sys_stats.items():
            self._convert_one_query_stat_block_to_json(json_dict,
                                                       (date_str, stat_pkg,)
                                                      )
        return json.dumps(json_dict)
    
    def _convert_one_query_stat_block_to_json(self, json_dict, stat_pkg):
        def parse_exp(exp_list):
            return []
        date_string, stat_block = stat_pkg
        print(stat_block)
        json_dict[date_string] = {
            "cost": round(stat_block.cost,4),
            "path": stat_block.best_route,
            "exp_res": parse_exp(stat_block.exp_results)
        }
        return json_dict
    

if __name__ == "__main__":
    # run_cli_in_main()
    bs_list = [5 for _ in range(8)]
    network_sim = NetworkSimulationEntryPoint(bs_list)
    print(network_sim._entry_grid)
    #print(x.retrieve_random_graph_as_json())
    while True:
        x = input("Please give query")
        if x == 'no':
            break
        source, dest = x[:3], x[3:]
        print(network_sim.retrieve_query_results_as_json(source,dest))
    print(network_sim.retrieve_system_results_as_json())
    