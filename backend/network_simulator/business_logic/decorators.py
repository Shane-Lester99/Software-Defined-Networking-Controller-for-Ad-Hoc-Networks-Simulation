def validate_key(func):
    def ck(*args, **kwargs):
        input_val = args[1]
        if isinstance(input_val, tuple) and len(input_val) == 2 and isinstance(input_val[0], float):
            func(*args, **kwargs)
        else:
            raise ValueError
    return ck