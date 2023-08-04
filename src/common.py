import os
from datetime import datetime

from bottle import request


def get_root():
    root = os.getcwd()

    if 'back' in root:
        if 'src' not in root[-4:]:
            if root[-1] != '/':
                root += '/'
            root += 'src'

    if root[-1] != '/':
        root += '/'

    return root[1:] if os.environ['APP_PORT'] == '8080' else 'src/'


def read_file(file_path):
    with open(file_path, encoding='utf-8') as file:
        content = file.read()

    return content


def dict_omit(data):
    if not isinstance(data, dict):
        raise TypeError('data should be dict')

    return {key: value
            for key, value in data.items()
            if value or value == 0}


def get_int_query_param(param):
    try:
        value = request.query.get(param)
        value = int(value)
        return value
    except (ValueError, TypeError):
        return value


# TODO: Considere remover caso não use parametros booleanos
def get_bool_query_param(param):
    value = request.query.get(param)
    param_values = {'true': True,
                    'false': False}

    param_value = param_values.get(value)

    return param_value if param_value else value


def handle_response_data(data, next_page_number):
    response_data = {'data': data}

    if next_page_number:
        response_data['next_page_number'] = next_page_number

    if data:
        response_data['count'] = len(data)

    return response_data
