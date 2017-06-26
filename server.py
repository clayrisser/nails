from flask import Flask
from nailspy import config
from pydash import _
import api

app = Flask(__name__)

@app.route('/')
def route_index():
    return 'The root'

if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    app.run(
        host=config.web['host'],
        port=config.web['port'],
        debug=True
    )
