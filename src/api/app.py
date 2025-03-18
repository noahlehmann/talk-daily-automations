import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'db.sqlite')}")

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
    return {'counter': counter.value}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
