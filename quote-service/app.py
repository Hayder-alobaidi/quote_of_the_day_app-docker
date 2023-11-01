import os
import random
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from rabbitmq_publisher import RabbitMQPublisher

app = Flask(__name__)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)

# Configure RabbitMQ URL
rabbitmq_url = os.environ['RABBITMQ_URL']
rabbitmq_publisher = RabbitMQPublisher(rabbitmq_url)

# Endpoint to get all quotes
@app.route('/quotes', methods=['GET'])
def get_all_quotes():
    all_quotes = Quote.query.all()
    quotes_list = [{'id': quote.id, 'text': quote.text} for quote in all_quotes]
    return jsonify(quotes_list)

# Endpoint to get a random quote
@app.route('/quote', methods=['GET'])
def get_random_quote():
    quotes = Quote.query.all()
    random_quote = random.choice(quotes) if quotes else None
    if random_quote:
        rabbitmq_publisher.notify_analytics_service(random_quote.id)
        return jsonify({'id': random_quote.id, 'text': random_quote.text})
    return jsonify({'message': 'No quotes available'})

# Endpoint to create a new quote
@app.route('/quotes', methods=['POST'])
def create_quote():
    data = request.json
    new_quote = Quote(text=data.get('text'))
    db.session.add(new_quote)
    db.session.commit()
    return jsonify({'message': 'Quote created', 'quote': {'id': new_quote.id, 'text': new_quote.text}}), 201

# Endpoint to get a specific quote by ID
@app.route('/quotes/<int:id>', methods=['GET'])
def get_quote_by_id(id):
    quote = Quote.query.get_or_404(id)
    return jsonify({'id': quote.id, 'text': quote.text})

# Endpoint to update an existing quote
@app.route('/quotes/<int:id>', methods=['PUT'])
def update_quote(id):
    quote = Quote.query.get_or_404(id)
    data = request.json
    quote.text = data.get('text', quote.text)
    db.session.commit()
    return jsonify({'message': 'Quote updated', 'quote': {'id': quote.id, 'text': quote.text}})

# Endpoint to delete a quote
@app.route('/quotes/<int:id>', methods=['DELETE'])
def delete_quote(id):
    quote = Quote.query.get_or_404(id)
    db.session.delete(quote)
    db.session.commit()

    rabbitmq_publisher.notify_quote_deletion(id)

    return jsonify({'message': 'Quote deleted'})

if __name__ == '__main__':
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    finally:
        rabbitmq_publisher.close_connection()
