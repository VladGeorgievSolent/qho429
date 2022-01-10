import sqlite3
from sqlite3 import Cursor, Connection
from typing import Union

import helpers


def open_database_connection() -> Connection:
    """
    Function establishing connection with SQL database.

    :return: Connection
    """
    try:
        connection = sqlite3.connect('/Users/Vlad/PycharmProjects/pythonProject/qho429.db')
        return connection

    except Exception as e:
        helpers.error(f'Database connection could not be established: \'{e}\'')


def close_database_connection(connection: Connection) -> None:
    """
    Function closing an existing connection with SQL database.

    :return: None
    """
    try:
        connection.close()
        return None

    except Exception as e:
        helpers.error(f'Database connection could not be closed: \'{e}\'')


def load_shoppers_data(cursor: Cursor) -> Union[list[int], None]:
    """
    Function loading shopper_ids from shoppers table.

    :return: None if no records found or a list of shopper ids
    """
    cursor.execute("""SELECT 
                            shoppers.shopper_id
                      FROM shoppers;""")
    shopper_ids = cursor.fetchall()

    if len(shopper_ids):
        return [shopper_id[0] for shopper_id in shopper_ids]

    return None


def check_if_shopper_id_exists(cursor: Cursor, shopper_id: int) -> int:
    """
    Function checking if the provided shopper_id matches any existing records in the shoppers table.

    :return: Current shopper id
    """
    shopper_ids = load_shoppers_data(cursor)

    if shopper_ids:
        if shopper_id in shopper_ids:
            return shopper_id

        helpers.error(f'Invalid shopper_id. Shopper with id: \'{shopper_id}\' not found')


def get_todays_shopper_basket_id(cursor: Cursor, shopper_id: int) -> Union[int, None]:
    """
    Function returning the most recent basket_id if the user has created one on the same day.

    :return: Most recent basket id
    """
    cursor.execute("""SELECT 
                            shopper_baskets.basket_id
                      FROM shopper_baskets
                      WHERE shopper_baskets.shopper_id = ?
                      AND DATE(shopper_baskets.basket_created_date_time) = DATE('now')
                      ORDER BY shopper_baskets.basket_created_date_time DESC
                      LIMIT 1""", (shopper_id,))
    shopper_basket = cursor.fetchone()

    if shopper_basket:
        return shopper_basket[0]

    return None


def get_order_history(cursor: Cursor, shopper_id: int):
    """
    Function returning the most recent basket_id if the user has created one on the same day.

    :return: Most recent basket id
    """
    cursor.execute("""SELECT 
                            shopper_orders.order_id AS 'Order ID',
                            shopper_orders.order_date AS 'Order Date',
                            products.product_description AS 'Product Description',
                            sellers.seller_name AS 'Seller',
                            '£ '||PRINTF("%.2f", ordered_products.price) AS 'Price',
                            ordered_products.quantity AS 'Qty',
                            ordered_products.ordered_product_status AS 'Status'
                       FROM shopper_orders
                       INNER JOIN ordered_products ON ordered_products.order_id = shopper_orders.order_id
                       INNER JOIN product_sellers ON product_sellers.product_id = ordered_products.product_id
                       INNER JOIN products ON products.product_id = ordered_products.product_id
                       INNER JOIN sellers ON sellers.seller_id = ordered_products.seller_id
                       WHERE shopper_orders.shopper_id = ?
                       GROUP BY shopper_orders.order_id
                       ORDER BY shopper_orders.order_date DESC""", (shopper_id,))
    shopper_baskets = cursor.fetchall()

    if shopper_baskets:
        return shopper_baskets

    print(f'{helpers.PrintColors.BLUE}No orders placed by this customer{helpers.PrintColors.END}')

    return None