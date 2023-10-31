import pika

class RabbitMQPublisher:
    def __init__(self, amqp_url):
        self.params = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='quote_request')

    def notify_analytics_service(self):
        self.channel.basic_publish(
            exchange='',
            routing_key='quote_request',
            body='Quote Requested'
        )
        print(" [x] Sent 'Quote Requested' message")

    def close_connection(self):
        self.connection.close()