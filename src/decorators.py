def log(filename=None):
    """Декоратор для логирования выполнения функций в консоль или файл"""
    def decorator(func):
        """Оборачивает функцию для добавления логирования"""
        def log_line(line):
            """Записывает строку лога в файл или консоль"""
            if filename is None:
                print(line)
            else:
                with open(filename, "a") as file:
                    file.write(line + "\n")

        def wrapper(*args, **kwargs):
            """Выполняет функцию и логирует результат"""
            try:
                result = func(*args, **kwargs)
                log_line(f"{func.__name__} ok: {result}. Inputs: {args}, {kwargs}")
            except Exception as e:
                log_line(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
        return wrapper
    return decorator
