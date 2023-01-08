def to_upper(function):
    def wrapper(args):
        args = args.upper()
        return args

    return wrapper
