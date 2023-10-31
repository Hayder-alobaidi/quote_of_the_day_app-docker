import pika, os

def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

url = os.environ.get("CLOUDAMQP_URL", "amqp://admin:admin@localhost:5672/")
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # Create a channel
channel.queue_declare(queue="test_queue")  # Declare the queue

# Set up the callback function to process incoming messages
channel.basic_consume(queue="test_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()