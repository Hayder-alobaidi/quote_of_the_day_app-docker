import os
import json
import threading
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from rabbitmq_consumer import RabbitMQConsumer

app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class QuoteCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, unique=True)
    count = db.Column(db.Integer, default=0)

@app.route('/count/<int:quote_id>', methods=['GET'])
def get_quote_count(quote_id):
    record = QuoteCount.query.filter_by(quote_id=quote_id).first()
    if record:
        return jsonify({"quote_id": quote_id, "current_count": record.count})
    else:
        return jsonify({"message": "No record found for quote {}".format(quote_id)}), 404

@app.route('/counts', methods=['GET'])
def get_all_counts():
    records = QuoteCount.query.all()
    return jsonify({"counts": [{"quote_id": record.quote_id, "current_count": record.count} for record in records]})

def process_message(quote_id, action):
    with app.app_context():
        if action == 'increment':
            record = QuoteCount.query.filter_by(quote_id=quote_id).first()
            if record:
                record.count += 1
            else:
                record = QuoteCount(quote_id=quote_id, count=1)
                db.session.add(record)
            db.session.commit()
            print(f"Count incremented for quote {quote_id}")
        elif action == 'delete':
            record = QuoteCount.query.filter_by(quote_id=quote_id).first()
            if record:
                db.session.delete(record)
                db.session.commit()
                print(f"Quote {quote_id} deleted from analytics.")

def start_rabbitmq_listener():
    def callback(ch, method, properties, body):
        data = json.loads(body)
        quote_id = data.get('quote_id')
        action = data.get('action')
        if quote_id is not None:
            process_message(quote_id, action)

    # Configure RabbitMQ URL
    rabbitmq_url = os.environ['RABBITMQ_URL']
    rabbitmq_consumer = RabbitMQConsumer(rabbitmq_url, 'quote_notifications', callback=callback)
    rabbitmq_consumer.start_listening()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    threading.Thread(target=start_rabbitmq_listener, daemon=True).start()
    app.run(debug=True, port=5001)
