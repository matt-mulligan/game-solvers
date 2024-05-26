"""Module to hold common methods for access to resources within the package."""

import csv
from pathlib import Path


def resources_path() -> Path:
    """Provide path to the resources folder within the package."""
    return Path(__file__).parent.parent.absolute().joinpath("resources")


def read_data_resource(resource_name: str) -> list[list[str]]:
    """Read the data resource from the resources folder using csv reader.

    :param resource_name: name of the resource in the data folder.

    :return: list of lists containing the data from the resource.
    """
    resource_path = resources_path().joinpath("data", resource_name)

    if not resource_path.exists():
        raise FileNotFoundError(f"Data resource '{resource_path}' not found.")

    with resource_path.open("r", encoding="UTF-8") as f_open:
        reader = csv.reader(f_open)
        return list(reader)
