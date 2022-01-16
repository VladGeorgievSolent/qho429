import sqlite3
from sqlite3 import Cursor
from typing import Union

import helpers


def load_shoppers_data(cursor: Cursor) -> Union[list[int], None]:
    """
    Function loading shopper_ids from shoppers table.

    :param: db cursor
    :return: None if no records found or a list of shopper ids
    """
    try:
        cursor.execute("""SELECT 
                                shoppers.shopper_id
                          FROM shoppers;""")
        shopper_ids = cursor.fetchall()

        if len(shopper_ids):
            return [shopper_id[0] for shopper_id in shopper_ids]
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation:\'{e}\'')

    return None


def check_if_shopper_exists(cursor: Cursor, shopper_id: int) -> int:
    """
    Function checking if the provided shopper_id matches any existing records in the shoppers table.

    :param: db cursor
    :param: shopper_id
    :return: Current shopper id
    """
    shopper_ids = load_shoppers_data(cursor)

    if shopper_ids:
        if shopper_id in shopper_ids:
            return shopper_id

        helpers.error(f'Invalid shopper_id. Shopper with id: \'{shopper_id}\' not found')


def get_order_history(cursor: Cursor, shopper_id: int) -> Union[list, None]:
    """
    Function returning the most recent basket_id if the user has created one on the same day.

    :param: db cursor
    :param: shopper_id
    :return: order history
    """
    try:
        cursor.execute("""SELECT 
                                shopper_orders.order_id,
                                shopper_orders.order_date,
                                products.product_description,
                                sellers.seller_name AS 'Seller',
                                '£ '||PRINTF("%.2f", ordered_products.price),
                                ordered_products.quantity,
                                ordered_products.ordered_product_status
                           FROM shopper_orders
                           INNER JOIN ordered_products ON ordered_products.order_id = shopper_orders.order_id
                           INNER JOIN product_sellers ON product_sellers.product_id = ordered_products.product_id
                           INNER JOIN products ON products.product_id = ordered_products.product_id
                           INNER JOIN sellers ON sellers.seller_id = ordered_products.seller_id
                           WHERE shopper_orders.shopper_id = ?
                           GROUP BY products.product_id, sellers.seller_id
                           ORDER BY shopper_orders.order_date DESC""", (shopper_id,))
        shopper_baskets = cursor.fetchall()

        if shopper_baskets:
            return shopper_baskets
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation:\'{e}\'')

    print(f'{helpers.PrintColors.BLUE}No orders placed by this customer{helpers.PrintColors.END}')
    return None
