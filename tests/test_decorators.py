import os
from src.decorators import log


@log()
def func_print(x, y):
    return x / y

filename = "test.log"
@log(filename=filename)
def func_file(x, y):
    return x / y


def test_log_print_ok(capsys):
    func_print(22, 2)
    assert capsys.readouterr().out == "func_print ok: 11.0. Inputs: (22, 2), {}\n"


def test_log_print_error(capsys):
    func_print(3, 0)
    assert capsys.readouterr().out == "func_print error: division by zero. Inputs: (3, 0), {}\n"


def test_log_file():
    if os.path.exists(filename):
        os.remove(filename)
    func_file(3, 0)
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0


