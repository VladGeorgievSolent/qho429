import os
from typing import Optional
from tabulate import tabulate
import helpers
import tui
from db.basket import get_todays_shopper_basket_id, add_item_to_basket, \
    display_basket_contents, update_item_quantity_in_basket_contents, delete_item_from_basket_contents, \
    get_baskets_contents, check_if_item_exists_in_basket, delete_basket_from_shopper_baskets, delete_basket_contents, \
    create_ordered_products, create_shopper_order
from db.connect import open_database_connection, close_database_connection
from db.inventory import get_product_categories, get_category_products, get_product_sellers, get_sellers_product_price
from db.shoppers import check_if_shopper_exists, get_order_history


def run():
    os.system('cls' if os.name == 'nt' else 'clear')
    tui.header()
    user_shopper_id_entry: int = tui.user_numerical_entry('Enter your shopper_id: ')

    if user_shopper_id_entry:
        connection = open_database_connection()
        cursor = connection.cursor()
        shopper_id = check_if_shopper_exists(cursor, user_shopper_id_entry)

        while shopper_id:
            user_menu_selection: Optional[int] = tui.menu()
            basket_id = get_todays_shopper_basket_id(cursor, shopper_id)

            if user_menu_selection == 1:
                order_history = get_order_history(cursor, shopper_id)
                if len(order_history):
                    print(tabulate(order_history, headers=(
                        'Order ID', 'Order Date', 'Product Description', 'Seller', 'Price', 'Qty', 'Status')))
                    print('\n')

            if user_menu_selection == 2:
                categories = get_product_categories(cursor)

                if categories:
                    helpers.print_options(categories, 'Product Categories')
                    category_id = helpers.get_chosen_option_id(categories, 'Please enter the number against the '
                                                                           'product category you want to choose: ')

                    if category_id:
                        products = get_category_products(cursor, category_id)

                        if products:
                            helpers.print_options(products, 'Products')
                            product_id = helpers.get_chosen_option_id(products, 'Enter the number against the '
                                                                                'product you want to choose: ')

                            if product_id:
                                exists = check_if_item_exists_in_basket(cursor, product_id)
                                if exists:
                                    helpers.error('This product already exists in your basket. Use option 4 from the '
                                                  'main menu to edit the quantity')
                                    continue
                                sellers = get_product_sellers(cursor, product_id)

                                if sellers:
                                    helpers.print_options(sellers, 'Sellers who sell this product')
                                    seller_id = helpers.get_chosen_option_id(sellers, 'Enter the number against '
                                                                                      'the seller you want to '
                                                                                      'choose: ')
                                    if seller_id:
                                        price = get_sellers_product_price(sellers, seller_id)
                                        quantity = helpers.user_numerical_entry('Enter the quantity of the selected '
                                                                                'product you want to buy: ')
                                        add_item_to_basket(cursor,
                                                           shopper_id,
                                                           seller_id,
                                                           product_id,
                                                           quantity,
                                                           price,
                                                           basket_id)

            if user_menu_selection == 3:
                basket_to_view = get_baskets_contents(cursor, basket_id)
                if basket_to_view:
                    display_basket_contents(cursor, basket_to_view, basket_id)
                else:
                    print(f'{helpers.PrintColors.BLUE}Your basket is empty{helpers.PrintColors.END} \n')

            if user_menu_selection == 4:
                basket_to_update = get_baskets_contents(cursor, basket_id)
                if basket_to_update:
                    display_basket_contents(cursor, basket_to_update, basket_id)
                    while True:
                        if len(basket_to_update) == 1:
                            new_quantity = tui.user_numerical_entry('Enter the new quantity you want to buy: ')
                            update_item_quantity_in_basket_contents(cursor, basket_id, basket_to_update[0][1], new_quantity)
                            updated_basket = get_baskets_contents(cursor, basket_id)
                            display_basket_contents(cursor, updated_basket, basket_id)
                            break
                        else:
                            user_input: str = input(f'{helpers.PrintColors.CYAN}Enter the basket item no. of the item '
                                                    f'you want to change: {helpers.PrintColors.END}').strip()
                            print(f'')
                        try:
                            chosen_number: int = int(user_input)
                            chosen_option = [item for item in basket_to_update if item[0] == chosen_number]
                            if len(chosen_option):
                                new_quantity = tui.user_numerical_entry('Enter the new quantity of the selected product you '
                                                                  'want to buy: ')
                                update_item_quantity_in_basket_contents(cursor, basket_id, chosen_option[0][1], new_quantity)
                                updated_basket = get_baskets_contents(cursor, basket_id)
                                display_basket_contents(cursor, updated_basket, basket_id)
                                break
                            else:
                                helpers.error(f'The basket item no. you have entered is invalid')
                                continue
                        except ValueError as e:
                            helpers.error(f'Options available range from 1 to {len(basket_to_update)}')
                            continue
                else:
                    print(f'{helpers.PrintColors.BLUE}Your basket is empty{helpers.PrintColors.END} \n')

            if user_menu_selection == 5:
                basket_to_remove_from = get_baskets_contents(cursor, basket_id)
                if basket_to_remove_from:
                    display_basket_contents(cursor, basket_to_remove_from, basket_id)
                    while True:
                        user_input: str = input(f'{helpers.PrintColors.CYAN}Enter the basket item no. of the item '
                                                f'you want to remove: {helpers.PrintColors.END}').strip()
                        print(f'')
                        try:
                            chosen_number: int = int(user_input)
                            chosen_option = [item for item in basket_to_remove_from if item[0] == chosen_number]
                            if len(chosen_option):
                                confirmed = tui.user_confirmation('Do you definitely want to delete this product from '
                                                                  'your basket (Y/N)? ')
                                if confirmed:
                                    delete_item_from_basket_contents(cursor, basket_id, chosen_option[0][1])
                                    basket_to_remove_from = get_baskets_contents(cursor, basket_id)
                                    if not basket_to_remove_from:
                                        delete_basket_from_shopper_baskets(cursor, basket_id, shopper_id)
                                        print(
                                            f'{helpers.PrintColors.BLUE}Your basket is empty{helpers.PrintColors.END} \n')
                                        break
                                    else:
                                        display_basket_contents(cursor, basket_to_remove_from, basket_id)
                                        break
                                else:
                                    break
                            else:
                                helpers.error(f'The basket item no. you have entered is not in your basket')
                                continue
                        except ValueError:
                            helpers.error(f'Options available range from 1 to {len(basket_to_remove_from)}')
                            continue
                else:
                    print(f'{helpers.PrintColors.BLUE}Your basket is empty{helpers.PrintColors.END} \n')

            if user_menu_selection == 6:
                basket_to_checkout = get_baskets_contents(cursor, basket_id)
                if basket_to_checkout:
                    display_basket_contents(cursor, basket_to_checkout, basket_id)
                    confirmed = tui.user_confirmation('Do you wish to proceed with the checkout (Y or N)? ')
                    if confirmed:
                        shopper_order_id = create_shopper_order(cursor, shopper_id)
                        create_ordered_products(cursor, basket_id, shopper_order_id)
                        delete_basket_contents(cursor, basket_id)
                        delete_basket_from_shopper_baskets(cursor, basket_id, shopper_id)
                        print(f'{helpers.PrintColors.GREEN}Checkout complete, your order has been placed.{helpers.PrintColors.END} \n')
                    else:
                        continue
                else:
                    print(f'{helpers.PrintColors.BLUE}Your basket is empty{helpers.PrintColors.END} \n')

            if user_menu_selection == 7:
                close_database_connection(connection)
                break

            if not user_menu_selection:
                print(
                    f'{helpers.PrintColors.WARNING}'
                    f'Please select a valid option from the menu.{helpers.PrintColors.END}')


if __name__ == '__main__':
    run()
