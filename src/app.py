from create_app import create_app
from resources.person.api import APP as person_app

APP = create_app()
APP.merge(person_app)
