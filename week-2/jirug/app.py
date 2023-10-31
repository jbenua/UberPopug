import pika
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy_session import flask_scoped_session
from models import db
from sqlalchemy.orm import sessionmaker
from tasks_api import tasks_api

app = Flask(__name__)
app.register_blueprint(tasks_api)

app.config.from_mapping(
    {
        "SQLALCHEMY_DATABASE_URI": (
            "postgresql://user:password@psql-jirug:5432/jirug"
        ),
    }
)

db.init_app(app)
flask_scoped_session(sessionmaker(bind=db.get_engine(app=app)), app=app)
Migrate(app, db)

message = "Hello World, its me appone"

QUEUE_NAME = "popug-queue"


@app.route("/")
def get():
    connection = pika.BlockingConnection(
        pika.URLParameters("amqp://user:password@habbit:5672/%2F")
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="popug-queue",
        body=request.args.get("msg"),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()
    return jsonify({"message": request.args.get("msg")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
