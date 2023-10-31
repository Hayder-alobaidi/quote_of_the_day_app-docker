from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# URL of the Quote Service
quote_service_url = 'http://localhost:5000'

@app.route('/')
def admin():
    return render_template('admin.html')

@app.route('/admin/quotes', methods=['GET', 'POST'])
def manage_quotes():
    if request.method == 'GET':
        # Get all quotes from the Quote Service
        response = requests.get(f"{quote_service_url}/quotes")
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch quotes from quote service"}), response.status_code

    elif request.method == 'POST':
        # Add a new quote using the Quote Service
        quote_text = request.json.get('text')
        response = requests.post(f"{quote_service_url}/quotes", json={"text": quote_text})
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to add quote using quote service"}), response.status_code

@app.route('/admin/quotes/<int:quote_id>', methods=['PUT', 'DELETE'])
def manage_single_quote(quote_id):
    if request.method == 'PUT':
        # Update an existing quote
        quote_text = request.json.get('text')
        response = requests.put(f"{quote_service_url}/quotes/{quote_id}", json={"text": quote_text})
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to update quote using quote service"}), response.status_code

    elif request.method == 'DELETE':
        # Delete a quote
        response = requests.delete(f"{quote_service_url}/quotes/{quote_id}")
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to delete quote using quote service"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')
