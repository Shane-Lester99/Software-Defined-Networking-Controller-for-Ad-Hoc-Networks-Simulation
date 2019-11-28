import random
from collections import namedtuple

class ChannelSystemNode:
    """
    Models randomly selected channels by choosing a random number from 1 to 
    CHANNEL_RANDOMIZATION and records it to an array of size AMOUNT_OF_CHANNELS.
    A channel is randomly selected and then with probably x from 0 to 1 that we
    have succesful packet run. The weight of the channel is 5 - sum(channel_values)
    and the lower the channel weight is the higher the probability of success
    """
    
    AMOUNT_OF_CHANNELS = 5
    
    def __init__(self):
        """
        Creates a channel system of size AMOUNT_OF_CHANNELS and assignes each
        channel a random variable from 0 to 1.
        """
        self.channel_system = [round(random.uniform(0, 1),4) for _ in range(self.AMOUNT_OF_CHANNELS)]
        
    def __repr__(self):
        return "ChannelSystemNode(total_weight: {}, channels: {})".format(self.report_weight(), self.channel_system)
        
    def report_weight(self):
        return round(5 - sum(self.channel_system), 4)
        
    def choose_channel_and_report_result(self):
        channel_choice = random.randint(0, self.AMOUNT_OF_CHANNELS-1)
        prob_of_success = self.channel_system[channel_choice]
        had_success = random.uniform(0, 1) < prob_of_success
        create_result = namedtuple("ChannelResult", "result channel_selected prob_of_success")
        return create_result(had_success, channel_choice, prob_of_success)
        
        
if __name__ == "__main__":
    c = ChannelSystemNode()
    print(c)
    for _ in range(5):
        print(c.choose_channel_and_report_result())