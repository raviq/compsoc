"""
This module contains utility functions for the compsoc website.
"""


# int-str converters
def int_list_to_str(int_list: list[int]) -> str:
    """
    Converts a list of integers to a comma-separated string.

    :param int_list: A list of integers.
    :type int_list: list[int]
    :return: A comma-separated string.
    :rtype: str
    """
    return ','.join(map(str, int_list))


def str_list_to_in(str_list: str) -> list[int]:
    """
    Converts a comma-separated string to a list of integers.

    :param str_list: A comma-separated string.
    :type str_list: str
    :return: A list of integers.
    :rtype: list[int]
    """
    return list(map(int, str_list.split(',')))
