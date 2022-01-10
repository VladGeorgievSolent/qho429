from typing import NewType


class PrintColors:
    """
    Set of colors to be used in the CLI interface.

    :param: None
    :return: None
    """

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def error(error_msg: str) -> None:
    """
    Function displaying an error message in the following format:
    'Error! {error_msg}.'
    Where {error_msg} is the value of the parameter passed to this function

    :param error_msg: A string containing an error message
    :return: Does not return anything
    """
    # TODO: Your code here
    print(f'{PrintColors.FAIL}Error! {error_msg}.{PrintColors.END}')


Record = NewType('Record', list[str])
"""Custom type representing a single record"""

"""Separator "line" used to improve the visual representation of CLI logical blocks"""
separator: str = '-' * 50
