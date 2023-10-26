import pika
from flask import Flask, jsonify, request

app = Flask(__name__)

message = "Hello World, its me appone"

QUEUE_NAME = "popug-queue"


connection = pika.BlockingConnection(
    pika.URLParameters("amqp://user:password@habbit:5672/%2F")
)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)


@app.route("/")
def get():
    channel.basic_publish(
        exchange="",
        routing_key="popug-queue",
        body=request.args.get("msg"),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    return jsonify({"message": request.args.get("msg")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    connection.close()
