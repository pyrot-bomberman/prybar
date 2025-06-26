from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Replace with your actual PostgreSQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testPassword@localhost:5432/prybar'
db = SQLAlchemy(app)

@app.route('/api')
def index():
    return jsonify({"message": "Welcome to the API!"})

class Account(db.Model):
    __tablename__ = 'account'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)
    personal_id = db.Column(db.Text, nullable=False)

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return jsonify([{
        'id': acc.id, 
        'created_at': acc.created_at, 
        'name': acc.name, 
        'personal_id': acc.personal_id
        } for acc in accounts])

class Category(db.Model):
    __tablename__ = 'item_category'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)

class Item(db.Model):
    __tablename__ = 'item'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)
    barcode = db.Column(db.Text, nullable=False)
    category_id = db.Column('category', db.Integer, db.ForeignKey('item_category.id'), nullable=False)
    category = db.relationship('Category', backref='items')

@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{
        'id': item.id, 
        'created_at': item.created_at, 
        'name': item.name, 
        'barcode': item.barcode, 
        'category_id': item.category_id,
        'category': item.category.name if item.category else None
        } for item in items])


if __name__ == '__main__':
    app.run(debug=True)