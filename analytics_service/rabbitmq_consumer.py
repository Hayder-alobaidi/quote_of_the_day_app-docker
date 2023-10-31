import pika
import os

class RabbitMQConsumer:
    def __init__(self, callback):
        self.rabbitmq_url = os.getenv('CLOUDAMQP_URL', 'amqps://rhhvlgxm:qUM7u0oJtYvNBS-csko-RAbc9AXxAEEL@fish.rmq.cloudamqp.com/rhhvlgxm')
        self.queue_name = 'quote_queue'
        self.callback = callback

    def start_listening(self):
        params = pika.URLParameters(self.rabbitmq_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)

        channel.basic_consume(queue=self.queue_name,
                              on_message_callback=self.callback,
                              auto_ack=True)

        print("Starting to consume from RabbitMQ")
        channel.start_consuming()