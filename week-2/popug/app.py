from threading import Thread

import pika
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy_session import flask_scoped_session
from models import db
from popug_api import popug_api
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_mapping(
    {
        "SQLALCHEMY_DATABASE_URI": (
            "postgresql://user:password@psql-popug:5432/popug"
        ),
    }
)
app.register_blueprint(popug_api)

db.init_app(app)
flask_scoped_session(sessionmaker(bind=db.get_engine(app=app)), app=app)
Migrate(app, db)


data = []

QUEUE_NAME = "popug-queue"


connection = pika.BlockingConnection(
    pika.URLParameters("amqp://user:password@habbit:5672/%2F")
)

channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)


def callback(ch, method, properties, body):
    data.append(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

thread = Thread(target=channel.start_consuming)
thread.start()


@app.route("/")
def get():
    return jsonify({"messages": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
