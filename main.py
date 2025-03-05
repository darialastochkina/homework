from src.decorators import log


@log()
def func_print(x, y):
    return x / y


@log(filename="test.log")
def func_file(x, y):
    return x / y


def test_log_ok(capsys):
    func_print(22, 2)
    captured = capsys.readouterr()
    assert captured.out == "func_print!"


# my_function2(3, 0)
