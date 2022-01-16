import sqlite3
from sqlite3 import Cursor
from typing import Union

import helpers
from helpers import compile_options_for_printing, error


def get_product_categories(cursor: Cursor) -> Union[list[list[Union[int, list]]], None]:
    """
    Function returning a list of product categories.

    :param: db cursor
    :param: shopper_id
    :return: Most recent basket id
    """
    try:
        cursor.execute("""SELECT 
                                categories.category_id,
                                categories.category_description
                          FROM categories""")
        categories: list[tuple] = cursor.fetchall()

        if len(categories):
            list_of_lists = [list(elem) for elem in categories]
            return compile_options_for_printing(list_of_lists)
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation:\'{e}\'')

    helpers.error('No categories available')
    return None


def get_category_products(cursor: Cursor, category_id: int) -> Union[list[list[Union[int, list]]], None]:
    """
    Function returning a list of product categories.

    :param: db cursor
    :param: shopper_id
    :return: Most recent basket id
    """
    try:
        cursor.execute("""SELECT 
                                products.product_id,
                                products.product_description
                          FROM products
                          WHERE products.category_id = ?
                          """, (category_id,))
        products: list[tuple] = cursor.fetchall()

        if len(products):
            list_of_lists = [list(elem) for elem in products]
            return compile_options_for_printing(list_of_lists)
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation:\'{e}\'')

    helpers.error('No products available for the selected category')
    return None


def get_product_sellers(cursor: Cursor, product_id: int) -> Union[list[list[Union[int, list]]], None]:
    """
    Function returning a list of product categories.

    :param: db cursor
    :param: shopper_id
    :return: Most recent basket id
    """
    try:
        cursor.execute("""SELECT 
                                sellers.seller_id,
                                sellers.seller_name,
                                product_sellers.price
                          FROM sellers
                          INNER JOIN product_sellers ON sellers.seller_id = product_sellers.seller_id
                          WHERE product_sellers.product_id = ?
                          """, (product_id,))
        sellers: list[tuple] = cursor.fetchall()

        if len(sellers):
            list_of_lists = [list(elem) for elem in sellers]
            return compile_options_for_printing(list_of_lists)
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation:\'{e}\'')

    helpers.error('No sellers are currently offering this product')
    return None


def get_sellers_product_price(sellers: list[list[Union[int, list]]], seller_id: int) -> Union[int, None]:
    """
    Function returning seller's product price

    :param: sellers list
    :param: product_id
    :return: str
    """
    seller = [item for item in sellers if item[1][0] == seller_id]
    if len(seller):
        return seller[0][1][2]

    helpers.error(f'Price from {seller_id} not available')
    return None
