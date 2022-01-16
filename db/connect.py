import sqlite3
from sqlite3 import Connection

import helpers


def open_database_connection() -> Connection:
    """
    Function establishing connection with SQL database.

    :return: Connection
    """
    try:
        root_dir = helpers.get_root_dir()
        connection = sqlite3.connect('{}/db/qho429.db'.format(root_dir))
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
