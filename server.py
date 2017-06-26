from api import app

@app.route('/')
def index():
    return 'Hello from Nails.py'

app.run(
    host='0.0.0.0',
    port=8804,
    debug=True
)
