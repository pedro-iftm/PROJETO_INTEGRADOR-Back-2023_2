from datetime import date
from uuid import uuid4

import database
from constants import DEFAULT_PAGE_SIZE
from errors import BadRequest
from validation import get_schema, validate


def create_person(data):
    __validation(data)
    person_id = __insert_person(data)

    return {'person_id': person_id}


def __validation(data):
    schema = get_schema('create_person', 'person')
    validate(data, schema)


def __insert_person(params):
    base_params = __generate_base_params()
    params = {**base_params,
              **params}
    database.upinsert('insert_person', 'person', params)

    return base_params['person_id']


def __generate_base_params():
    return {'person_id': str(uuid4()),
            'name': None,
            'address_id': None}
