import sqlite3
from datetime import datetime
from sqlite3 import Cursor
from typing import Union, Optional
from tabulate import tabulate
import copy
import helpers


def get_todays_shopper_basket_id(cursor: Cursor, shopper_id: int) -> Union[int, None]:
    """
    Function returning the most recent basket_id if the user has created one on the same day.

    :param: db cursor
    :param: shopper_id
    :return: Most recent basket id
    """
    try:
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
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation: \'{e}\'')

    return None


def add_item_to_basket(
        cursor: Cursor,
        shopper_id: int,
        seller_id: int,
        product_id: int,
        quantity: int,
        price: int,
        basket_id: int = False,
) -> None:
    """
    Function adding an item to an existing basket or creating a new one.

    :param: db cursor
    :param: shopper_id
    :param: seller_id
    :param: product_id
    :param: quantity
    :param: price
    :param: basket_id
    :return: None
    """
    if basket_id:
        try:
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute("""INSERT INTO
                                    basket_contents (basket_id, product_id, seller_id, quantity, price)
                                    VALUES(?,?,?, ?,?) """, (basket_id, product_id, seller_id, quantity, price))
            cursor.execute("COMMIT")
        except sqlite3.Error as e:
            helpers.error(f'Unsuccessful database operation. Rolling back... \'{e}\'')
            cursor.execute("ROLLBACK")
    else:
        try:
            cursor.execute("""PRAGMA foreign_keys=ON""")
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute("""SELECT seq+1 FROM sqlite_sequence WHERE name='shopper_baskets'""")
            seq_row = cursor.fetchone()
            new_id = seq_row[0]
            date = datetime.today().strftime('%Y-%m-%d')
            cursor.execute("""INSERT INTO
                                    shopper_baskets (basket_id, shopper_id, basket_created_date_time)
                                    VALUES(?,?,?) """, (new_id, shopper_id, date))
            cursor.execute("""INSERT INTO
                                    basket_contents (basket_id, product_id, seller_id, quantity, price)
                                    VALUES(?,?,?, ?,?) """, (new_id, product_id, seller_id, quantity, price))
            cursor.execute("COMMIT")
        except sqlite3.Error as e:
            helpers.error(f'Unsuccessful database operation. Rolling back... \'{e}\'')
            cursor.execute("ROLLBACK")

    print(f'{helpers.PrintColors.GREEN}Item added to your basket{helpers.PrintColors.END} \n')

    return None


def get_baskets_contents(cursor: Cursor, basket_id: int) -> Union[list[list], None]:
    """
    Function returning basket's content

    :param: basket_id
    :return: basket contents
    """
    try:
        cursor.execute("""SELECT 
                                products.product_id,
                                products.product_description,
                                sellers.seller_name,
                                basket_contents.quantity,
                                '£ '||PRINTF("%.2f", basket_contents.price),
                                '£ '||PRINTF("%.2f", basket_contents.quantity * basket_contents.price)
                           FROM basket_contents 
                           INNER JOIN product_sellers ON product_sellers.seller_id = basket_contents.seller_id
                           INNER JOIN sellers ON product_sellers.seller_id = sellers.seller_id
                           INNER JOIN products ON products.product_id = basket_contents.product_id
                           WHERE basket_contents.basket_id = ?
                           GROUP BY products.product_id""", (basket_id,))
        basket_contents = cursor.fetchall()

        if basket_contents:
            list_of_lists: list[list] = [list(elem) for elem in basket_contents]
            numbered: list[list[Union[int, list]]] = []
            for item in list_of_lists:
                index = list_of_lists.index(item)
                numbered.append(list([int(index) + 1] + item))
            return numbered
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation: \'{e}\'')

    return None


def get_basket_total(cursor: Cursor, basket_id: int) -> Union[list, None]:
    """
    Function returning basket's total sum

    :param: basket_id
    :return: str
    """
    try:
        cursor.execute("""SELECT 
                                '£ '||PRINTF("%.2f", SUM(basket_contents.quantity * basket_contents.price))
                           FROM basket_contents 
                           WHERE basket_contents.basket_id = ?""", (basket_id,))
        total = cursor.fetchall()

        if total:
            return total
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation: \'{e}\'')

    return None


def display_basket_contents(cursor: Cursor, basket_contents: Union[list[list], None], basket_id: int) -> None:
    """
    Function fetching basket contents and displaying as table

    :param: cursor
    :param: basket_contents
    :param: basket_id
    :return: None
    """
    if basket_contents and len(basket_contents):
        edited_for_printing = copy.deepcopy(basket_contents)
        for item in edited_for_printing:
            del item[1]
        total = get_basket_total(cursor, basket_id)
        print(f'{helpers.PrintColors.BLUE}Basket Contents{helpers.PrintColors.END}')
        print(f'{helpers.PrintColors.HEADER}{helpers.separator}'
              f'{helpers.PrintColors.END}')
        edited_for_printing.append(['', '', '', 'Basket Total', '', total[0][0]])
        print(tabulate(edited_for_printing, headers=(
            'Basket Item', 'Product Description', 'Seller Name', 'Qty', 'Price', 'Total')))
        print('\n')

    return None


def update_item_quantity_in_basket_contents(cursor: Cursor,
                                            basket_id: int,
                                            product_id: int,
                                            quantity: int
                                            ) -> None:
    """
    Function updating basket contents

    :param: cursor
    :param: basket_id
    :param: product_id
    :param: quantity
    :return: None
    """
    try:
        cursor.execute("""PRAGMA foreign_keys=ON""")
        cursor.execute("""UPDATE
                                basket_contents
                           SET quantity = ?
                           WHERE basket_id = ? AND product_id = ?""", (quantity, basket_id, product_id))
        cursor.execute("COMMIT")
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation. Rolling back... \'{e}\'')
        cursor.execute("ROLLBACK")

    return None


def delete_item_from_basket_contents(cursor: Cursor, basket_id: int, product_id: int) -> None:
    """
    Function deleting item from basket

    :param: cursor
    :param: basket_id
    :param: product_id
    :return: None
    """
    try:
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("""DELETE  
                           FROM basket_contents
                           WHERE basket_id = ? AND product_id = ?""", (basket_id, product_id))
        cursor.execute("COMMIT")
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation. Rolling back... \'{e}\'')
        cursor.execute("ROLLBACK")

    return None


def delete_basket_contents(cursor: Cursor, basket_id: int) -> None:
    """
    Function deleting basket contents

    :param: cursor
    :param: basket_id
    :return: None
    """
    try:
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("""DELETE  
                           FROM basket_contents
                           WHERE basket_id = ?""", (basket_id,))
        cursor.execute("COMMIT")
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation. Rolling back... \'{e}\'')
        cursor.execute("ROLLBACK")

    return None


def check_if_item_exists_in_basket(cursor: Cursor, product_id: int) -> bool:
    """
    Function checking if passed in product_id already exists in the basket

    :param: connection
    :param: cursor
    :param: basket_id
    :param: product_id
    :return: None
    """
    try:
        cursor.execute("""SELECT 
                                basket_contents.product_id
                          FROM basket_contents
                          WHERE basket_contents.product_id = ?;""", (product_id,))
        product_ids = cursor.fetchall()

        if len(product_ids):
            if id in product_ids:
                return False
            else:
                return True
        else:
            return False
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation: \'{e}\'')


def delete_basket_from_shopper_baskets(cursor: Cursor, basket_id: int, shopper_id: int) -> None:
    """
    Function deleting basket

    :param: cursor
    :param: basket_id
    :param: shopper_id
    :return: None
    """
    try:
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("""DELETE  
                           FROM shopper_baskets
                           WHERE basket_id = ? AND shopper_id = ?""", (basket_id, shopper_id))
        cursor.execute("COMMIT")
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation. Rolling back... \'{e}\'')
        cursor.execute("ROLLBACK")

    return None


def create_shopper_order(cursor: Cursor, shopper_id: int) -> Optional[int]:
    """
    Function creating shopper order

    :param: cursor
    :param: shopper_id
    :return: None
    """
    try:
        cursor.execute("""PRAGMA foreign_keys=ON""")
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("""SELECT seq+1 FROM sqlite_sequence WHERE name='shopper_orders'""")
        seq_row = cursor.fetchone()
        new_id = seq_row[0]
        date = datetime.today().strftime('%Y-%m-%d')
        cursor.execute("""INSERT INTO
                                shopper_orders (order_id, shopper_id, order_date, order_status)
                                VALUES(?,?,?,?) """, (new_id, shopper_id, date, 'Placed'))
        cursor.execute("COMMIT")
        return cursor.lastrowid
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation. Rolling back... \'{e}\'')
        cursor.execute("ROLLBACK")

    return None


def create_ordered_products(cursor: Cursor, basket_id: int, shopper_order_id: int) -> None:
    """
    Function creating ordered-products

    :param: cursor
    :param: shopper_id
    :return: None
    """
    try:
        cursor.execute("""SELECT 
                                basket_contents.product_id,
                                basket_contents.seller_id,
                                basket_contents.quantity,
                                basket_contents.price
                          FROM basket_contents
                          WHERE basket_contents.basket_id = ?""", (basket_id,))
        basket_contents = cursor.fetchall()
        records = []
        for item in basket_contents:
            records.append((shopper_order_id, item[0], item[1], item[2], item[3], 'Placed'))
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("BEGIN TRANSACTION")
        cursor.executemany('INSERT INTO ordered_products VALUES(?, ?, ?, ?, ?, ?);', records)
        cursor.execute("COMMIT")
    except sqlite3.Error as e:
        helpers.error(f'Unsuccessful database operation. Rolling back... \'{e}\'')
        cursor.execute("ROLLBACK")

    return None
