import os
from flask import Flask
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

# Detect environment (PostgreSQL in Docker, SQLite otherwise)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

@app.route('/increment', methods=['GET'])
def increment():
    session = SessionLocal()
    counter = session.query(Counter).first()

    if not counter:
        counter = Counter(value=0)
        session.add(counter)

    counter.value += 1
    session.commit()
    session.close()

    return {'counter': counter.value}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
