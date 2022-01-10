from typing import Optional

from pip._internal.utils.misc import tabulate

import data
import helpers
import tui


def run():
    user_shopper_id_entry: int = tui.user_shopper_id_entry()

    if user_shopper_id_entry:
        connection = data.open_database_connection()
        cursor = connection.cursor()
        shopper_id = data.check_if_shopper_id_exists(cursor, user_shopper_id_entry)
        shopper_basket = data.get_todays_shopper_basket_id(cursor, shopper_id)

        while True:
            user_menu_selection: Optional[int] = tui.menu()

            if user_menu_selection == 1:
                order_history = data.get_order_history(cursor, shopper_id)
                if len(order_history):
                    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('Order ID', 'Order Date', 'Product Description', 'Seller', 'Price', 'Qty', 'Status'))
                    for v in order_history:
                        order_id, order_history, product_description, seller_name, price, quantity, ordered_product_status = v
                        print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(order_id, order_history, product_description, seller_name, price, quantity, ordered_product_status))
                    # print(f'{helpers.PrintColors.BLUE}{order_history}{helpers.PrintColors.END}')
            if user_menu_selection == 2:
                print(user_menu_selection)
            if user_menu_selection == 3:
                print(user_menu_selection)
            if user_menu_selection == 4:
                print(user_menu_selection)
            if user_menu_selection == 5:
                print(user_menu_selection)
            if user_menu_selection == 6:
                print(user_menu_selection)
            if user_menu_selection == 7:
                break

            if not user_menu_selection:
                print(
                    f'{helpers.PrintColors.WARNING}'
                    f'Please select a valid option from the menu.{helpers.PrintColors.END}')


if __name__ == '__main__':
    run()
