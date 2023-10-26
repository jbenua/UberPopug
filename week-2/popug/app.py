from threading import Thread

import pika
from flask import Flask, jsonify

app = Flask(__name__)

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
