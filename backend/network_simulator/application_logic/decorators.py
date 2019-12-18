"""
Decorators for input validation of various modules
"""

import random

def validate_key(pq_add_task_func):
    """
    Validate priority queue key s.t. it is of form (<Number>, some_obj)
    """
    def check_key(*args, **kwargs):
        input_val = args[1]
        if (isinstance(input_val, tuple)
            and len(input_val) == 2
            and isinstance(input_val[0], float)):
            pq_add_task_func(*args, **kwargs)
        else:
            raise ValueError("PriorityQueue input must be of type (<float>, some_obj)")
    return check_key
    
def validate_amount(init_channel_func):
    """
    Channel amount should be between 4 and 10 or else ValueError
    """
    def check_amount(*args, **kwargs):
        amount = args[1]
        if (4 <= amount <= 10):
            init_channel_func(*args, **kwargs)
        else:
            raise ValueError("Channel amount must have length between 4 and 10")
    return check_amount
    
def validate_path(try_path_func):
    """
    Path length must be no greater then 7 and no less then 2 or else ValueError
    Note that this gives us between 1 to 6 hops
    """
    def check_path(*args, **kwargs):
        path = args[2]
        if 2 <= len(path) <= 7:
            return try_path_func(*args, **kwargs)
        else:
            raise ValueError("Path must be between length 2 and 8")
    return check_path
    
def validate_grid_input(grid_init_func):
    """
    Validate grid input s.t. it is an array of size 1 to 8 (number of base stations
    we can have) and each base station dooesn't have more then 5 values. Therefore
    we can have a maximum of 40 + 8 = 48 devices on the board (8 base stations and 5 
    devices per base station (8*5 devices))
    """
    def check_input(*args, **kwargs):
        base_station_list = args[1]
        if 1 <= len(base_station_list) <= 8:
            for num_devices in base_station_list:
                if not (1 <= num_devices <= 5):
                    raise ValueError("Must have between 1 to 5 user devices per base station")
        else:
            raise ValueError("Must have between 1 to 8 base stations")
        grid_init_func(*args, **kwargs)
    return check_input