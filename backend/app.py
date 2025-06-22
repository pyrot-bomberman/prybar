from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Replace with your actual PostgreSQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testPassword@localhost:5432/prybar'
db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = 'account'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)
    pid = db.Column(db.Text, nullable=False)

@app.route('/api')
def index():
    return jsonify({"message": "Welcome to the API!"})

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return jsonify([{
        'id': acc.id, 
        'timestamp': acc.timestamp, 
        'name': acc.name, 
        'pid': acc.pid
        } for acc in accounts])

@app.route('/api/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    name = data.get('name')
    pid = data.get('pid')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    elif not pid:
        return jsonify({'error': 'PID is required'}), 400
    account = Account(name=name, pid=pid, timestamp=db.func.now())
    db.session.add(account)
    db.session.commit()
    return jsonify({
        'id': account.id, 
        'timestamp': account.timestamp, 
        'name': account.name, 
        'pid': account.pid
    }), 201

if __name__ == '__main__':
    app.run(debug=True)