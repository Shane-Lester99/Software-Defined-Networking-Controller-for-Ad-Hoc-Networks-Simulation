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
    print("To set up the network topology, write a list of 1 to 8 numbers.")
    print("Each number signifies how many user devices are associated with that base station.\n")
    bs_str = input("Please enter these numbers now as a single space seperated list:")
    bs_list = [int(char) for char in bs_str if char != " "]
    chan_amount_str = input("Please enter an amount of channels between 4 and 10:")
    chan_amount = int(chan_amount_str)
    entry = NetworkSimulationEntryPoint(bs_list, chan_amount)
    entry.run_cli()

class NetworkSimulationEntryPoint:
    """
    Entry point of NetworkSimulation application. It provides an 
    interface over the application modules and returns the results as JSON.
    It also allows for backend debugging with a CLI version of the application.
    
    To run the CLI version run the module from the main function
    """
    
    def __init__(self, base_station_list, channel_amount):
        self._entry_grid = grid.Grid(base_station_list)
        self._entry_graph = graph.RoutingSystemMasterGraph(
            self._entry_grid.device_data,
            self._entry_grid.TRANSMISSION_RADIUS,
            channel_amount)
            
    def run_cli(self):
        """
        This will allow the user to run the app as a cli without the use of the API. 
        THe user can write queries on the command line and once they exit they
        will retrieve the system output stats. The purpose of this function is
        for backend debugging.
        """
        print(self._entry_grid)
        print(self._entry_graph.channels)
        print(self.retrieve_random_graph_as_json())
        while True:
            exit_string = input("Would you like to specify a query path (Y/N):")
            if exit_string == "N" or exit_string == "n":
                print(self.retrieve_system_results_as_json())
                break
            x = input("Please specify query path in form <device_id_1><device_id2>:")
            source, dest = x[:3], x[3:]
            print(self.retrieve_query_results_as_json(source, dest))
            
    def retrieve_random_graph_as_json(self):
        """
        For the initialization function call of the API. This function will return
        the random graph that will remain static after initialization.
        JSON is of form:
        {
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
        """
        json_dict = dict()
        for node_name, entries in self._entry_graph.graph.items():
            metadata = entries[0]
            connected_edges = entries[1]
            string_connected_edges = [node_name for node_name in connected_edges]
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
        route = self._entry_graph.retrieve_optimal_path_and_allocate_channels(
                                                                    source_node,
                                                                    dest_node)
        return json.dumps(route)
    
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
        """
        Converts statistics from query into a dictionary that can be converted
        to json string by json.dumps. 
        JSON is in form:
        {
            date_str: {
                cost: <Float>,
                path: <List>,
                results: {
                    R22_R02: {
                        channel: {
                            id: <int>
                            weight: <float>
                            channels: <List>
                        },
                        selections: [
                            {
                                had_success: <bool>,
                                chan_selected: <int>,
                                prob_success: <float>
                            }, ...
                        ]
                    }
                }
            }, ...
        }
        This json string is used for both
        self.retrieve_system.. and self.retrieve_query... . The only difference
        is that the former contains all the values in the session and the 
        latter contains just that particular query.
        """
        def parse_exp(result_list):
            json_dict = dict()
            for result in result_list:
                node_key = result.nodes[0] + "_" + result.nodes[1]
                channel = self._convert_channel_to_dict(result.channel)
                channel_selections = \
                    [
                        {
                            "had_success": chan_result.had_success,
                            "chan_selected": chan_result.channel_selected,
                            "prob_success": chan_result.prob_of_success
                        } for chan_result in result.channel_selection
                    ]
                json_dict[node_key] = {
                    "channel": channel,
                    "selections": channel_selections
                }
            return json_dict
            
        date_string, stat_block = stat_pkg
        json_dict[date_string] = {
            "cost": round(stat_block.cost,4),
            "path": stat_block.best_route,
            "results": parse_exp(stat_block.exp_results)
        }
        return json_dict
    
    def _convert_channel_to_dict(self, chan):
        return {
            "id": chan.c_id,
            "weight": chan.channel_weight,
            "channels": chan.channel_system
        }

if __name__ == "__main__":
    """
    Run this file as the entry to envoke the CLI version of this application
    """
    run_cli_in_main()