"""Pytest Configuration File."""

from pathlib import Path

from pytest import fixture

HERE = Path(__file__).absolute()


@fixture
def fixture_path():
    return HERE.parent.parent / "fixtures"


@fixture
def data_fixture_path(fixture_path):
    return fixture_path / "data"
