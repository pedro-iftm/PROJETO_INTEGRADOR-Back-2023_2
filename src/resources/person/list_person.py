import database
from common import dict_omit, handle_response_data
from errors import BadRequest
from validation import get_schema, validate


def list_person(params):
    filtered_params = dict_omit(params)
    __validation(filtered_params)

    page_number = params.pop('page_number')
    page_size = params.pop('page_size')

    records, next_page_number = database.paginate('list_person', 'person', page_number, params, page_size)
    data = [dict_omit(record)
            for record in records]

    return data, next_page_number


def __validation(params):
    schema = get_schema('list_person', 'person')
    validate(params, schema)

    if params.get('page_number') == 0 or params.get('page_size') == 0:
        raise BadRequest('page-number and page-size should be integer greater than zero')
