def log(filename=None):
    def decorator(func):
        def log_line(line):
            if filename is None:
                print(line)
            else:
                with open(filename, "a") as file:
                    file.write(line + "\n")

        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_line(f"{func.__name__} ok: {result}. Inputs: {args}, {kwargs}")
            except Exception as e:
                log_line(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
        return wrapper
    return decorator
