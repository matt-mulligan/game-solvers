from game_solvers.common.resources import read_data_resource
from pytest import raises


def test_when_read_data_resource_and_not_exist_then_raise_error():
    err_pattern = r"Data resource '.*silly_resource_file.csv' not found\."

    with raises(FileNotFoundError, match=err_pattern):
        read_data_resource("silly_resource_file.csv")


def test_when_read_data_resource_and_exist_then_read_data():
    actual = read_data_resource("example_data.csv")
    assert actual == [
        ["name", "runs", "centuries"],
        ["Hayden", "8625", "30"],
        ["Langer", "7696", "23"],
        ["Ponting", "13378", "41"],
    ]
