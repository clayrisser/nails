from nails import init_app
from api import controllers, models

app = init_app(__file__, '/api/v1/', controllers, models)
