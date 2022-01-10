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


def user_shopper_id_entry() -> int:
    """
    Message prompting the user for the their shopper_id.

    :param: None
    :return: None if invalid shopper_id otherwise an integer
    """
    header()
    user_input: str = input(f'{helpers.PrintColors.CYAN}Enter your shopper_id: {helpers.PrintColors.END}').strip()

    try:
        shopper_id: int = int(user_input)
        return shopper_id
    except Exception as e:
        helpers.error(f'Invalid entry: \'{e}\'. Your selection must be a numerical value')


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

    print(f'{helpers.PrintColors.CYAN}Please choose one of the following options:{helpers.PrintColors.END}')

    for key, value in menu_options.items():
        print(key, ':', value)

    user_input: str = input(f'{helpers.PrintColors.CYAN}Enter your selection: {helpers.PrintColors.END}').strip()

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
