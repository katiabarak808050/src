from __future__ import annotations
import json
from typing import Optional


class Path:
    """
    this class will be used for holding cycle path
    single - minimal path for each pair of source-destination
    path-sources stored in stack like list
    """
    def __init__(self, one_before_last: str, last_source: str):
        self._sources = [one_before_last, last_source]  # Stack

    def push(self, source: str):
        self._sources.append(source)

    def __str__(self):
        return " ".join(self._sources[::-1])

    def __len__(self):
        return len(self._sources)

    def __eq__(self, other: Path):
        return set(self._sources) == set(other._sources)


def check_cycles(source: str, data: dict[str, list]) -> Optional[Path]:
    """
    outer function for searching the shortest cycle path form source to source
    :param source: start/end point of cycle path
    :param data: the DB to search into
    :return: the shortest cycle path form source to source
    """
    def check_cycles_inner(src: str, destination: str, checked_keys: list[str]) -> Optional[Path]:
        """
        inner, recursive function for searching the shortest path form some source to the destination
        :param src: start point of a path
        :param destination: path end point
        :param checked_keys: all previously visited sources, to avoid infinite searching
        :return: the shortest path form source to source
        """

        # Converging path, to avoid getting the same source more than once
        if src in checked_keys[:-1]:
            return None

        if src not in data:           # Dead end, the key is not in dict
            return None

        if destination in data[src]:         # Path found
            return Path(src, destination)

        min_path = None
        for possible_scr in data[src]:      # Check for all the possibilities of the next step
            checked_keys.append(possible_scr)
            path = check_cycles_inner(possible_scr, destination, checked_keys)
            if path:                        # If some path found
                path.push(src)
                if min_path is None:
                    min_path = path
                elif len(path) < len(min_path):
                    min_path = path
            # All the steps at the same level should start with the same "visited sources"
            checked_keys.pop()

        return min_path

    # preparing for inner function call
    checked = [source]
    return check_cycles_inner(source, source, checked)


def find_all_uniq_cycles(data: dict[str, list]) -> list[Path]:
    """
    this function finds all non-duplicate minimal path
    :param data: DB as dictionary
    :return: list of all found non-duplicate minimal path
    """
    all_path: list[Path] = []
    for key_as_source in data:
        path = check_cycles(key_as_source, data)
        # if path found - check if it is already in result list
        # items will be compared by items, disregarding the order
        if path and path not in all_path:
            all_path.append(path)
    return all_path


def print_DB(data: dict[str, list]):
    """
    this function prints the key-values pairs of the given dict.
    :param data: DB as dictionary
    :return:
    """
    for k, v in data.items():
        print(k, v)


def main():
    # Opening JSON file
    f = open('data.json')

    # returns JSON object as a dictionary
    data = json.load(f)
    # print_DB(data)

    # find and print all minimal, uniq paths
    all_cycles_paths = find_all_uniq_cycles(data)
    for path in all_cycles_paths:
        print(path)


if __name__ == '__main__':
    main()

