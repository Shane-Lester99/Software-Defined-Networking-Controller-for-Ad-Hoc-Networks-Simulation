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
    20_4: {5: [2, 3, 4], 6: [1,3,4, 6], 7: [6,4]}
    this means when holding number of nodes to 20 and hops to 4, we have
    generated the scatter plot of 5 on the x axis with values 2 3 and 4 on the
    y axis for 5 channels the amount of channel switches we had holding those
    other two variables constant. Same for 6 and 7.
    """
    def ___init___(self):
        pass
    
    def create_key(self, node_number, channel_number):
        return str(node_number) + "_" + str(channel_number)