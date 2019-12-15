from collections import defaultdict


class StatManager:
    """
    Manages the statistics of the route simulator for generating performance
    charts.
    
    We keep track of four variables, number of nodes, number of channels on the
    x axis and hops and channels used on the y axis. We generate four charts:
    (number_of_channels, channel_switches), (number_of_channels, number_of_hops),
    (number_of_nodes, channel_switches), (number_of_nodes, number_of_hops)
    
    When we keep track of each chart, the other two variables must be held constant.
    To do this, we keep track of statistics with four maps. The key of each
    map is the variables that we hold constant.
    
    E.g. for (number_of_channels, channel_switches)
    20_4: {5: [2, 3, 4], 6: [1,3,4,6], 7: [6,4]}
    this means when holding number of nodes to 20 and hops to 4, we have
    generated the scatter plot of 5 on the x axis with values 2 3 and 4 on the
    y axis for 5 channels the amount of channel switches we had holding those
    other two variables constant. Same for 6 and 7.
    """
    
    CHAN_SWITCH = "chan_switch"
    CHAN_HOP = "chan_hop"
    NODE_SWITCH = "node_switch"
    NODE_HOP = "node_hop"
    
    
    def ___init___(self):
        self.stats = {
            self.CHAN_SWITCH : defaultdict(list),
            self.CHAN_HOP: defaultdict(list),
            self.NODE_SWITCH: defaultdict(list),
            self.NODE_HOP: defaultdict(list)
        }
        
    def __repr__(self):
        return "StatManager(Channels/Switches(...), Channels/Hops(...), Nodes/Switches(...), Nodes/Hops(...)"
    
    def collect_stats_from_route_data(self, num_channels, num_nodes,
                                      num_hops, num_switches):
        """
        Will take data from route job and package it into statistics that can
        be queried into charts
        """
        # NOTE: gen_key will generate a key of the variables we hold constant
        gen_key = lambda x, y: str(x) + "_" + str(y)
        # CHAN_SWITCH CHART
        chan_switch_key = gen_key(num_nodes, num_hops)
        self.stats[self.CHAN_SWITCH][chan_switch_key][str(num_channels)].append(num_switches)
        
        # CHAN_HOP chart
        chan_hop_key = gen_key(num_nodes, num_switches)
        self.stats[self.CHAN_HOP][chan_hop_key][str(num_channels)].append(num_hops)
        
        # NODE_SWITCH chart
        node_switch_key = gen_key(num_channels, num_hops)
        self.stats[self.NODE_SWITCH][node_switch_key][str(num_nodes)].append(num_switches)
        
        # NODE_HOP chart
        node_hop_key = gen_key(num_channels, num_switches)
        self.stats[self.NODE_HOP][node_switch_key][str(num_nodes)].append(num_hops)
        
if __name__ == "__main__":
    x = StatManager()
    print(x)