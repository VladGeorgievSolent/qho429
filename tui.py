from typing import Union

import helpers


def header() -> None:
    """
    A header message displaying the application name.

    :param: None
    :return: None
    """
    print(f'{helpers.PrintColors.HEADER}ORINOCO – SHOPPER MAIN MENU'
          f'{helpers.PrintColors.END}')
    print(f'{helpers.PrintColors.HEADER}{helpers.separator}'
          f'{helpers.PrintColors.END}')


def user_numerical_entry(message: str) -> int:
    """
    Message prompting the user for a numerical entry.

    :param: None
    :return: integer
    """
    while True:
        user_input: str = input(f'{helpers.PrintColors.CYAN}{message}{helpers.PrintColors.END}').strip()
        print(f'')
        try:
            value: int = int(user_input)
        except ValueError as e:
            helpers.error(f'Invalid entry: \'{e}\'. Your selection must be a numerical value')
            continue

        if value < 0:
            helpers.error('The value must be greater than 0')
            continue
        else:
            return value


def user_confirmation(message: str) -> bool:
    """
    Message prompting to confirm an action.

    :param: None
    :return: boolean
    """
    while True:
        user_input: str = input(f'{helpers.PrintColors.CYAN}{message}{helpers.PrintColors.END}').strip().upper()
        print(f'')
        if user_input == 'Y':
            return True
        elif user_input == 'N':
            return False
        else:
            helpers.error('The answer must by one of: Y, N')
            continue



def menu(menu_options: dict[int, str] = None) -> Union[int, None]:
    """
    A menu consisting of the following options: 'Display your order history', 'Add an item to
    your basket', 'View your basket', 'Change the quantity of an item in your basket ', 'Remove an item from your
    basket', 'Checkout' and 'Exit'

    The user's response is read in and returned as an integer corresponding to the selected option.

    If the user enters a invalid option then a suitable error message is displayed and the value
    None is returned.

    :return: None if invalid selection otherwise an integer corresponding to a valid menu option
    """
    if menu_options is None:
        menu_options = {1: "Display your order history", 2: "Add an item to your basket", 3: "View your basket",
                        4: "Change the quantity of an item in your basket ", 5: "Remove an item from your basket",
                        6: "Checkout", 7: "Exit"}

    for key, value in menu_options.items():
        print(f'{key}. {value}')

    user_input: str = input(f'{helpers.PrintColors.CYAN}Enter your selection: {helpers.PrintColors.END}').strip()
    print(f'')

    try:
        convert_to_int = int(user_input)
    except Exception as e:
        helpers.error(f'Invalid option: \'{e}\'. Your selection must be a numerical value')
        return None

    if convert_to_int in menu_options.keys():

        return convert_to_int
    else:
        helpers.error(f'Invalid option: \'{convert_to_int}\'')
        return None
