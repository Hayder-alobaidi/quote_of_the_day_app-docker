from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

quote_service_url = 'http://localhost:5000/random'  # URL of the Quote Service
analytics_service_url = 'http://localhost:5001'  # URL of the Analytics Service

@app.route('/quote', methods=['GET'])
def get_quote():
    # Get a random quote from the Quote Service
    quote_response = requests.get(quote_service_url)
    if quote_response.status_code == 200:
        # Notify the Analytics Service
        requests.post(f"{analytics_service_url}/increment")
        return quote_response.json()
    else:
        return jsonify({"error": "Quote service is unavailable"}), 503

@app.route('/analytics', methods=['GET'])
def get_analytics():
    # Get analytics data from the Analytics Service
    analytics_response = requests.get(f"{analytics_service_url}/count")
    if analytics_response.status_code == 200:
        return analytics_response.json()
    else:
        return jsonify({"error": "Analytics service is unavailable"}), 503

if __name__ == '__main__':
    app.run(debug=True, port=5002)
