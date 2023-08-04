from datetime import date, datetime
from json import JSONEncoder, dumps

from bottle import Bottle, JSONPlugin, response

from errors import ApiError


def __error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ApiError as error:
            response.status = error.status_code
            response.set_header('Content-Type', 'application/json')

            return dumps({'status': error.status_code,
                          'message': error.message})

    return wrapper


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%d-%m-%Y')

        if isinstance(obj, datetime):
            return obj.isoformat()[0:19]

        return JSONEncoder.default(self, obj)


def create_app():
    app = Bottle(autojson=False)
    app.install(__error_handler)
    app.install(JSONPlugin(json_dumps=lambda obj: dumps(obj, cls=CustomJSONEncoder)))

    return app
