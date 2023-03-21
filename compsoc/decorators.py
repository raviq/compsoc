def rename(newname):
    def decorator(fn):
        fn.__name__ = newname
        return fn

    return decorator
