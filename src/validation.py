import json
import os

import jsonschema

from common import get_root, read_file
from errors import BadRequest


def validate(body, schema):
    try:
        jsonschema.validate(body, schema)
    except jsonschema.exceptions.ValidationError as error:
        raise BadRequest(error.message) from error


def get_schema(schema_name, resource):
    root = get_root()
    schema_path = f'{root}resources/{resource}/schemas/{schema_name}.json'
    schema = read_file(schema_path)

    return json.loads(schema)
