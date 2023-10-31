from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class QuoteCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, unique=True)
    count = db.Column(db.Integer, default=0)

@app.route('/increment/<int:quote_id>', methods=['POST'])
def increment_quote_count(quote_id):
    record = QuoteCount.query.filter_by(quote_id=quote_id).first()
    if record:
        record.count += 1
    else:
        record = QuoteCount(quote_id=quote_id, count=1)
        db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Count incremented for quote {}".format(quote_id), "current_count": record.count})

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
    return jsonify({"counts": [{ "quote_id": record.quote_id, "current_count": record.count } for record in records]})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
