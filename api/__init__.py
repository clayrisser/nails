from flask import Flask
from api.models import db, initialize

initialize()

app = Flask(__name__)

@app.before_request
def _db_connect():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
