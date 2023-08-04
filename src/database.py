from psycopg2.extras import DictCursor

from common import get_root, read_file
from constants import DEFAULT_PAGE_SIZE
from database_connection import get_dict_cursor

MARGIN_TO_CHECK_NEXT_PAGE = 1


def fetchone(query_name, resource, params=None):
    with get_dict_cursor() as cursor:
        query = __get_query(query_name, resource)
        cursor.execute(query, params)
        record = cursor.fetchone()

        return dict(record) if record else {}


def upinsert(query_name, resource, params=None):
    with get_dict_cursor() as cursor:
        query = __get_query(query_name, resource)
        cursor.execute(query, params)


def paginate(query_name, resource, page_number, params=None, page_size=DEFAULT_PAGE_SIZE):
    if not page_size:
        page_size = DEFAULT_PAGE_SIZE

    query = __get_query(query_name, resource)
    limit_offset = __build_limit_offset(page_number, page_size)
    query = f'{query} {limit_offset}'

    with get_dict_cursor() as cursor:
        cursor.execute(query, params)
        records = cursor.fetchall()
        has_next_page = len(records) > page_size
        next_page_number = None

        if has_next_page:
            records = records[:-MARGIN_TO_CHECK_NEXT_PAGE]
            next_page_number = page_number + 1

        records = __format_data(records, cursor.description)

        return records, next_page_number


def __format_data(records, description):
    columns = [column[0]
               for column in description]

    if records:
        return [dict(zip(columns, record))
                for record in records]

    return []


def __build_limit_offset(page_number, page_size):
    limit = page_size + MARGIN_TO_CHECK_NEXT_PAGE
    print('page_number', page_number)
    print('page_size', page_size)
    offset = (page_number - 1) * page_size

    return f'LIMIT {limit} OFFSET {offset}'


def __get_query(query_name, resource):
    root = get_root()
    query_path = f'{root}resources/{resource}/sql/{query_name}.sql'
    query = read_file(query_path)

    return query
