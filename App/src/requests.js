/*
This module will be used to call the Python/django backend REST interface

To see how the JSON is formatted, go to 
backend.network_simulator.application_logic.network_simulation_entry_point.py
and read the comments above the API calls
*/
const fetch = require("node-fetch")

// baseURL is for localhost for demo, this will be deleted if this app
// is used past demos.


// Constants to use when building a url for the API
const CREATE_GRAPH = "create_graph"
const FIND_ROUTE = "find_route"
const GET_SYS_STATS = "get_sys_stats"
const GET_REACHABLE_NODES = "get_reachable_nodes"
const RESET_GRAPH = "reset_graph"
const RUN_METRICS_COLLECTION = "run_metrics_collection"
const BASE_URL = "http://127.0.0.1:8080/network_simulator"


function buildUrl(argumentsArray) {
    // This function will have the name of the argument in the 0th index and
    // after that it will have the rest of the arguments necessary
    const argKey = argumentsArray[0]
    switch (argKey) {
        case CREATE_GRAPH:
            let baseStationList = argumentsArray[1]
            let channelAmount = argumentsArray[2]
            console.log(BASE_URL + `/init_sim/${baseStationList}/${channelAmount}`)
            return BASE_URL + `/init_sim/${baseStationList}/${channelAmount}`
        case FIND_ROUTE:
            let sourceNode = argumentsArray[1]
            let destNode = argumentsArray[2]
            return BASE_URL + `/route_data/${sourceNode}/${destNode}`
        case GET_SYS_STATS:
           return BASE_URL + `/collect_stats`
        case GET_REACHABLE_NODES:
            let source = argumentsArray[1]
            return BASE_URL + `/get_reachable_nodes/${source}`
        case RESET_GRAPH:
           return BASE_URL + `/reset/`
        default:
            throw new Error("Requesting non existent route. Exiting.")
    }
    
}

async function queryApi(url) {
    const res = await fetch(url)
        .then(res => res.json())
        .then(json_random_graph => json_random_graph)
        .catch(err => err)
    return res
}

// This is an example of how to call these async functions. Note that 
// callInitSystem is what has to be called first (or else 400 response). 
// After it is called if it is called again it won't reinit the graph, 
// it will instead return the same json graph.

// Also note that the django sever must be launches with ./run_backend.sh before
// we call the API on path network-routing-simulation.backend.run_backend.sh

const initSim = queryApi(buildUrl([CREATE_GRAPH, [5,5,5, 5, 5], 10]))
initSim.then(x=> console.log("graph init", x))
        .then(function() {
             let query = queryApi(buildUrl([FIND_ROUTE, "R05", "R03"]))
             query.then(x => console.log("Query1", x))
             .catch(err => console.log(err))
        })
        .then(function() {
             let query = queryApi(buildUrl([FIND_ROUTE, "R05", "R03"]))
             query.then(x => console.log("Query2", x))
             .catch(err => console.log(err))
        })
        .then(function() {
             let query = queryApi(buildUrl([FIND_ROUTE, "R05", "R03"]))
             query.then(x => console.log("Query3", x))
             .catch(err => console.log(err))
        })
        .then(function() {
            let query = queryApi(buildUrl([GET_REACHABLE_NODES, "R03"]))
            query.then(x => console.log("Reachable", x))
            .catch(err => console.log(err))
       })
// const initSim = callInitSystem([4,4,4], 5)
// initSim.then(x => console.log("graphinit ", x))
//       .then(function() {
//             const query = callQueryRoute("R02", "R03")
//             query.then(x => console.log("Query1", x))
//             .catch(err => console.log(err))
//         })
//         .then(function() {
//             const query = callQueryRoute("R02", "R04")
//             query.then(x => console.log("Query2", x))
//             .catch(err => console.log(err))
//         })
//         .then(function() {
//             const outputStats = callSystemStats()
//             outputStats.then(x => console.log("sys stats", x))
//             .catch(err => console.log(err))
//         })
//         .catch(err => err)
