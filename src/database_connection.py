import os
from contextlib import contextmanager

from psycopg2.extras import DictCursor
from psycopg2.pool import SimpleConnectionPool

from errors import InternalServerError

POOL = None


def get_pool():
    global POOL
    if not POOL:
        POOL = SimpleConnectionPool(minconn=os.environ['POSTGRES_MINCONN'],
                                    maxconn=os.environ['POSTGRES_MAXCONN'],
                                    host=os.environ['POSTGRES_HOST'],
                                    database=os.environ['POSTGRES_DATABASE'],
                                    user=os.environ['POSTGRES_USER'],
                                    password=os.environ['POSTGRES_PASSWORD'],
                                    port=os.environ['POSTGRES_PORT'])

    return POOL


@contextmanager
def get_connection():
    connection = get_pool().getconn()

    try:
        yield connection
        connection.commit()

    except Exception as error:
        connection.rollback()
        raise InternalServerError('Error during database process') from error

    finally:
        POOL.putconn(connection)


@contextmanager
def get_cursor():
    with get_connection() as connection:
        yield connection.cursor()


@contextmanager
def get_dict_cursor():
    with get_connection() as connection:
        yield connection.cursor(cursor_factory=DictCursor)
