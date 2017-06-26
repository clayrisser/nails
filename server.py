from nails import Nails
import api

app = Nails(__name__)

@app.route('/')
def route_index():
    return 'The root'

if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    app.run()
