import os
from typing import NewType, Union
from tui import user_numerical_entry


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
    print(f'{PrintColors.FAIL}Error! {error_msg}.{PrintColors.END}')


def get_root_dir() -> str:
    """
    Function returning the path to the root of the project

    :param: None
    :return: str
    """
    return os.path.dirname(os.path.abspath('main.py'))


def compile_options_for_printing(options: list[list]) -> list[list[Union[int, list]]]:
    """
    Function preparing options for printing

    :param: options list
    :return: compiled list of options
    """
    options.sort(key=lambda tup: tup[1])
    numbered: list[list[Union[int, list]]] = []
    for option in options:
        index = options.index(option)
        numbered.append([int(index) + 1, option])
    return numbered


def print_options(options: list[list[Union[int, list]]], title: str) -> None:
    """
    Function printing available options

    :param: options list
    :param: options title
    :return: None
    """
    print(f'{PrintColors.BLUE}{title} \n{PrintColors.END}')
    for option in options:
        additional_property = ''
        if len(option[1]) == 3:
            additional_property = '(£{})'.format(option[1][2])
        print(f'{option[0]}. {option[1][1]} {additional_property}')


def get_chosen_option_id(options: list[list[Union[int, list]]], message: str) -> Union[int, None]:
    """
    Function prompting the user for their chosen option and returning the option's id

    :param: options list
    :param: options title
    :return: str
    """
    chosen_number: int = user_numerical_entry(f'{message}')
    chosen_option = [item for item in options if item[0] == chosen_number]
    if len(chosen_option):
        return chosen_option[0][1][0]

    error(f'Options available range from 1 to {len(options)}')
    return None


"""Separator "line" used to improve the visual representation of CLI logical blocks"""
separator: str = '-' * 50
