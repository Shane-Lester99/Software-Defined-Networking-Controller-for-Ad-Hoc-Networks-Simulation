import random

def validate_key(func):
    """
    Validate priority queue key s.t. it is of form (<float>, some_obj)
    """
    def ck(*args, **kwargs):
        input_val = args[1]
        if (isinstance(input_val, tuple)
            and len(input_val) == 2
            and isinstance(input_val[0], float)):
            func(*args, **kwargs)
        else:
            raise ValueError("PriorityQueue input must be of type (<float>, some_obj)")
    return ck
    
def validate_grid_input(func):
    """
    Validate grid input s.t. it is an array of size 1 to 9 (number of base stations
    we can have) and each base station dooesn't have more then 5 values. Therefore
    we can have a maximum of 45 + 9 = 54 devices on the board (9 base stations and 5 
    devices per base station)
    """
    def ci(*args, **kwargs):
        base_station_list = args[1]
        if 1 <= len(base_station_list) <= 9:
            for num_devices in base_station_list:
                if not (1 <= num_devices <= 5):
                    raise ValueError("Must have between 1 to 5 user devices per base station")
        else:
            raise ValueError("Must have between 1 to 9 base stations")
        func(*args, **kwargs)
    return ci
        