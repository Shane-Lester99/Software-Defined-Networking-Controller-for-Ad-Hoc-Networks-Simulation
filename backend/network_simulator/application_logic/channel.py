import numpy
from decorators import validate_amount, validate_path
from collections import namedtuple
import priority_queue

blocked_channel_entry = namedtuple("BlockedChannel", "chan_coor chan_used")

def get_weight(index_list, channels):
    summ = 0
    for i in index_list:
        summ += channels[i]
    return summ

class Channels:
    
    @validate_amount
    def __init__(self, amount, transmission_radius):
        self.transmission_radius = transmission_radius
        self.channels = [numpy.random.exponential() for _ in range(amount)]
        
    def __repr__(self):
        chan_str = str(["Channel {}: {}".format(i, exp) for i, exp in enumerate(self.channels)])
        return "Channels({})".format(chan_str)
    
    @validate_path   
    def find_cheapest_channels_for_path(self, global_interference, coor_path):
        """
        This will return the cheapest channel combination for a given path subject
        to interference globally and from the path
        """
        def find_paths(coor_path, curr, output, blocked_channels):
            if len(curr) == len(coor_path) - 1:
                weight = get_weight(curr, self.channels)
                output.add_task((weight, curr.copy()))
                return
            for chan_num, _ in enumerate(self.channels):
                available_channels = self._check_available_channels(blocked_channels,
                                                                    coor_path[len(curr)])
                if chan_num in available_channels:
                    blocked_channels.append(blocked_channel_entry(coor_path[len(curr)],
                                                                  chan_num))
                    curr.append(chan_num,)
                    find_paths(coor_path, curr, output, blocked_channels)
                    blocked_channels.pop()
                    curr.pop()
        output = priority_queue.PriorityQueue()
        find_paths(coor_path, [], output, global_interference)
        return output[0]
    
    def _check_available_channels(self, blocked_channels, curr_coor):
        """
        This returns a list of available channels when given a cooridinate
        """
        dont_use_channels = set()
        for blocked_chan in blocked_channels:
            curr_coor_x, curr_coor_y = curr_coor
            block_coor_x, block_coor_y = blocked_chan.chan_coor
            if (abs(curr_coor_x - block_coor_x) <= self.transmission_radius and
                abs(curr_coor_y - block_coor_y) <= self.transmission_radius):
                    # If we find a channel with interference we don't use the
                    # adjaceny channels either
                    dont_use_channels.add(blocked_chan.chan_used)
                    dont_use_channels.add(blocked_chan.chan_used - 1)
                    dont_use_channels.add(blocked_chan.chan_used + 1)
        channels_total = set(i for i, _ in enumerate(self.channels))
        return list(channels_total - dont_use_channels)
        
if __name__ == "__main__":
    sys_channels = Channels(5, 2)
    path = [(0,2), (2,3), (3,5)]
    global_intf = []
    x = sys_channels.find_cheapest_channels_for_path(global_intf, path)
    print(x)