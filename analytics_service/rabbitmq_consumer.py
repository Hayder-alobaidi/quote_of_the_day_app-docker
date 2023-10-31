import pika
import json

class RabbitMQConsumer:
    def __init__(self, amqp_url, queue_name, callback):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.callback = callback
        self.connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)

    def start_listening(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.connection.close()

    def stop_listening(self):
        self.channel.stop_consuming()
        self.connection.close()
