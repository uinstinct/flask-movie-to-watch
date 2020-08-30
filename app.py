from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return 'initialized the app'

if __name__ == '__main__':
    app.run(debug=True)