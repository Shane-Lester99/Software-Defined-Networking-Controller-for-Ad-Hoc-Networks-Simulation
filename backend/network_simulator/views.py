from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#from restframework import viewset

import sys
import os
sys.path.append("/".join([os.getcwd(), "network_simulator", "application_logic"]))

import network_simulation_entry_point as sim

network_routing_system = sim.NetworkSimulationEntryPoint()

def init_sim(req, base_station_list, channel_amount):
    """
    Initializes the system and returns the graph as json. If it is called and
    the system is already initialized, then it will just return the json graph of the
    first initialization since the server was launched. To create a new graph altogether
    the server must be reset.
    """
    global network_routing_system
    if not network_routing_system.entry_graph:
        try:
            base_station_list = [int(device) for device in base_station_list if device != ","]
            json_graph = network_routing_system.retrieve_random_graph_as_json(base_station_list,
                                                                              channel_amount)
            return HttpResponse(json_graph, content_type="application/json", status=200)
        except ValueError as err: 
            return HttpResponse(content="Error: " + str(err), status=400)
    else:
        json_graph = network_routing_system.retrieve_random_graph_as_json()
        return HttpResponse(json_graph, content_type="application/json", status = 200)
    
def route_data(req, source, dest):
    """
    Query and retrieve the stats from the graph here
    """
    global network_routing_system
    if not network_routing_system.entry_graph:
        return HttpResponse("Error: Must initialize graph before query", status=400)
    json_stats = network_routing_system.retrieve_query_results_as_json(source, dest)
    return HttpResponse(json_stats, content_type="application/json", status=200)
    
def get_reachable_nodes(req, source_node):
    global network_routing_system
    if not network_routing_system.entry_graph:
        return HttpResponse("Error: Must initialize graph before query", status=400)
    json_nodes = network_routing_system.get_reachable_nodes_as_json(source_node)
    return HttpResponse(json_nodes, content_type="application/json", status=200)
    
    
def reset_graph(req):
    global network_routing_system
    if not network_routing_system.entry_graph:
        return HttpResponse("Error: Must initialize graph before query", status=400)
    network_routing_system.reset_graph()
    return HttpResponse(status=200)
    
    
def collect_stats(req):
    """
    Retrieve all the system stats
    """
    global network_routing_system
    if not network_routing_system:
        return HttpResponse("Error: Must initialize app before query", status=400)
    json_stats = network_routing_system.retrieve_system_results_as_json()
    return HttpResponse(json_stats, content_type="application/json", status=200)
    
def run_many_simulations(req):
    """
    This will run lots of simulations and then return the system stats
    """
    global network_routing_system
    network_routing_system.reset_graph
    metrics_report_stats = network_routing_system.generate_metrics_report()
    return HttpResponse(metrics_report_stats,
                        content_type="application/json",
                        status=200)
    