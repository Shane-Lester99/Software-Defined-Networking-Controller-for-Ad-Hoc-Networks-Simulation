/*
Request wrapper functions to call the Django backend. PLEASE ONLY USE
THESE TO COMMUNICATE WITH BACKEND
*/

const apiCalls = require("./request_api_calls")

function initSystem(baseStationArray) {
    /*
    This is to retrieve the random graph and init the system. It will return the
    graph as json. To do this, feed this function an array of size 1-8 (number
    of base stations) with values 1-5 at each entry. Make sure to not pass these
    parameters, or else you will recieve a 400 (bad request)
    
    JSON is of this form:
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
    */
    
    
}