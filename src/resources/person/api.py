from http import HTTPStatus

from bottle import request, response
from common import get_int_query_param, handle_response_data
from create_app import create_app

from .create_person import create_person
from .get_person_by_id import get_person_by_id
from .list_person import list_person

APP = create_app()


@APP.get('/person/<person_id>')
def _get_by_id(person_id):
    return get_person_by_id(person_id)


@APP.get('/person')
def _list_person():
    query_params = {'page_number': get_int_query_param('page-number'),
                    'page_size': get_int_query_param('page-size')}

    data, next_page_number = list_person(query_params)
    response_data = handle_response_data(data, next_page_number)

    return response_data


@APP.post('/person')
def _create_person():
    data = request.json

    result = create_person(data)
    response.status = HTTPStatus.CREATED

    return result
