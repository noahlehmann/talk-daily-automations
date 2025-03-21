import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'db.sqlite')}")
ADD_CORS_ALLOW_ALL_HEADER = os.getenv("ADD_CORS_ALLOW_ALL_HEADER", "true").lower() in ["true", "1"]
CORS_ALLOW_PATTERN = os.getenv("CORS_ALLOW_PATTERN", "*")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, default=0)


@app.route('/increment', methods=['GET'])
def increment():
    counter = Counter.query.first()

    if not counter:
        counter = Counter(value=0)
        db.session.add(counter)

    counter.value += 1
    db.session.commit()

    response = jsonify({'counter': counter.value})
    if ADD_CORS_ALLOW_ALL_HEADER:
        response.headers.add('Access-Control-Allow-Origin', CORS_ALLOW_PATTERN)
    return response

@app.route('/', methods=['GET'])
def health():
    response = jsonify({'message': 'OK'})
    if ADD_CORS_ALLOW_ALL_HEADER:
        response.headers.add('Access-Control-Allow-Origin', CORS_ALLOW_PATTERN)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
