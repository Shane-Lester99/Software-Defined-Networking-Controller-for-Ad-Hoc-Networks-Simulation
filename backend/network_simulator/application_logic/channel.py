import numpy


class Channels:
    def __init__(self, amount):
        self.channels = [numpy.random.exponential() for _ in range(amount)]
        
    def __repr__(self):
        chan_str = str(["Channel {}: {}".format(i, exp) for i, exp in enumerate(self.channels)])
        return "Channels({})".format(chan_str)

if __name__ == "__main__":
    x = Channels(5)
    print(x)



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