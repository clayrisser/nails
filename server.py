from nails import Nails
import app

server = Nails(app)

if __name__ == '__main__':
    server.start()
