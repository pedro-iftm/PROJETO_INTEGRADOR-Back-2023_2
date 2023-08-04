import database
from common import dict_omit
from errors import NotFound


def get_person_by_id(person_id):
    record = database.fetchone('get_person_by_id', 'person', {'person_id': person_id})

    if not record:
        raise NotFound('person not found')

    return dict_omit(record)
