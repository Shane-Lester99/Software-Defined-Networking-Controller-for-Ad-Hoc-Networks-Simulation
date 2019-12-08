import numpy
from decorators import validate_amount, validate_path
from collections import namedtuple

blocked_channel_entry = namedtuple("BlockedChannel", "chan_coor chan_used")

class Channels:
    
    @validate_amount
    def __init__(self, amount, transmission_radius):
        self.transmission_radius = transmission_radius
        self.channels = [numpy.random.exponential() for _ in range(amount)]
        
    def __repr__(self):
        chan_str = str(["Channel {}: {}".format(i, exp) for i, exp in enumerate(self.channels)])
        return "Channels({})".format(chan_str)
    
    # @validate_path   
    # def enumerate_available_channels(self, global_interference, coor_path):
    #     def find_paths():
    #         if len(curr) == len(coor_path) - 1:
    #             output.append(curr.copy())
    #         for edge_num in len(coor_path-1):
    #             pass
    #     output = [] 
    #     find_pathts(coor_path, curr, output)
    #     return False
    
    def _check_blocked_channels(self, blocked_channels, curr_coor):
        """
        This checks if given coordinate if there all blocked channels that
        are unavailable. It returns a set of unavailable channels give a coor
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
        return dont_use_channels
        
if __name__ == "__main__":
    sys_channels = Channels(5, 2)
    x = [blocked_channel_entry((6,5), 0), blocked_channel_entry((6,6), 2), blocked_channel_entry((7,8), 4)]
    print(sys_channels._check_blocked_channels(x, (6,8)))
    # path = [(6,5,), (6,6,), (7,8,), (9,7,)]
    # print(sys_channels)
    # x = sys_channels.enumerate_available_channels(None, path)
    # print(x)



# import random
# from collections import namedtuple

# class ChannelSystemNode:
#     """
#     Models randomly selected channels by choosing a random number from 1 to 
#     CHANNEL_RANDOMIZATION and records it to an array of size AMOUNT_OF_CHANNELS.
#     A channel is randomly selected and then with probably x from 0 to 1 that we
#     have succesful packet run. The weight of the channel is 5 - sum(channel_values)
#     and the lower the channel weight is the higher the probability of success
#     """
    
#     AMOUNT_OF_CHANNELS = 5
    
#     def __init__(self, channel_id):
#         """
#         Creates a channel system of size AMOUNT_OF_CHANNELS and assignes each
#         channel a random variable from 0 to 1.
#         """
#         self.c_id = channel_id
#         self.channel_system = [round(random.uniform(0, 1),4) for _ in range(self.AMOUNT_OF_CHANNELS)]
#         self.channel_weight = round(5 - sum(self.channel_system), 4)
        
#     def __repr__(self):
#         return "ChannelSystemNode(id: {},total_weight: {}, channels: {})".format(
#             self.c_id,
#             self.channel_weight,
#             self.channel_system)
        
#     def choose_channel_and_report_result(self):
#         """
#         Randomly chooses a channel and reports whether the packet was successfully
#         transmitted or not.
#         """
#         channel_choice = random.randint(0, self.AMOUNT_OF_CHANNELS-1)
#         prob_of_success = self.channel_system[channel_choice]
#         had_success = random.uniform(0, 1) < prob_of_success
#         create_result = namedtuple("ChannelResult", "had_success channel_selected prob_of_success")
#         return create_result(had_success, channel_choice, prob_of_success)