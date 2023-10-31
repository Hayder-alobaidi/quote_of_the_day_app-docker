import pika, os
  
url = os.environ.get("CLOUDAMQP_URL", "amqp://admin:admin@localhost:5672/")
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # Create a channel
channel.exchange_declare(exchange='test_exchange', exchange_type='direct')  # Declare the exchange
channel.queue_declare(queue="test_queue")  # Declare the queue
channel.queue_bind(queue="test_queue", exchange="test_exchange", routing_key="tests")  # Bind the queue to the exchange
channel.basic_publish(exchange="test_exchange",
                      routing_key="tests",
                      body="Hello CloudAMQP!")
channel.close()
connection.close()
