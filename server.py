from nails import Nails, config
import api

print(config['debug'])

server = Nails(__name__)

@server.route('/')
def route_index():
    return 'Hello, Nails.py!'

if __name__ == '__main__':
    server.register_app(api.app)
    server.run()
