from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testPassword@localhost:5432/prybar'
db.init_app(app)

CORS(app)

from models import *


@app.route('/api')
def index():
    print("API endpoint accessed")
    return jsonify({"message": "Welcome to the API!"})

# Get all accounts
@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return jsonify([{
        'id': account.id, 
        'created_at': account.created_at, 
        'name': account.name, 
        'personal_id': account.personal_id
        } for account in accounts])

# Get all items w/ category
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

# Get all categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = ItemCategory.query.all()
    return jsonify([{
        'id': category.id, 
        'created_at': category.created_at, 
        'name': category.name
        } for category in categories])

# Get all settings
@app.route('/api/settings', methods=['GET'])
def get_settings():
    settings = Settings.query.all()
    return jsonify([{
        'id': setting.id, 
        'created_at': setting.created_at, 
        'key': setting.key, 
        'value': setting.value
        } for setting in settings])

# Get sales. If user is specified, return sales for that user.
# If no user is specified, return all sales.
# user is specified by account_id.
# If count is specified, return that many sales.
@app.route('/api/get-latest-sale', methods=['GET'])
def get_latest_sale():
    count = request.args.get('count', default=1, type=int)
    account = request.args.get('account', default=None, type=int)
    if account:
        print(f"Received request for latest {count} sales for user: {account}")
        sales = Sale.query.filter_by(void=False, account_id=account).order_by(Sale.created_at.desc()).limit(count).all()
    else:
        print(f"Received request for latest {count} sales")
        sales = Sale.query.filter_by(void=False).order_by(Sale.created_at.desc()).limit(count).all()

    return jsonify([{
        'id': sale.id,
        'created_at': sale.created_at,
        'account_id': sale.account_id,
        'account': sale.account.name if sale.account else None,
        'void': sale.void,
        'items': [{
            'item_id': item.item_id,
            'quantity': item.quantity,
            'sale_price': str(item.sale_price), # Convert Decimal to string for JSON serialization
            'name': Item.query.get(item.item_id).name if item.item_id else None
        } for item in sale.items],
        'total': sale.total  # Calculate total
    } for sale in sales])

# Get the item or account associated with a barcode.
@app.route('/api/get-barcode', methods=['GET'])
def get_barcode(barcode = None):
    if not barcode:
        barcode = request.args.get('barcode', default=None, type=str)
    if not barcode:
        return jsonify({'error': 'Barcode parameter is required'}), 400
    
    barcode_lookup = BarcodeLookup.query.filter_by(barcode=barcode).all()
    if len(barcode_lookup) > 1:
        return jsonify({'error': 'Multiple entries found for this barcode'}), 400
    elif not barcode_lookup:
        return jsonify({'error': 'No entry found for this barcode'}), 404
    
    barcode_lookup = barcode_lookup[0]
    
    print(f"Barcode found: {barcode_lookup.barcode}, ID: {barcode_lookup.id}, Source Table: {barcode_lookup.source_table}")
    
    if barcode_lookup.source_table == 'item':
        response = get_item(barcode_lookup.id)
        data = response.get_json()
        data['type'] = 'item'
        return jsonify(data)
    elif barcode_lookup.source_table == 'account':
        response = get_account(barcode_lookup.id)
        data = response.get_json()
        data['type'] = 'account'
        return jsonify(data)
    else:
        return jsonify({'error': 'Unknown source table'}), 400

@app.route('/api/get-account', methods=['GET'])
def get_account(account_id = None):
    if not account_id:
        account_id = request.args.get('account_id', default=None, type=int)
    if not account_id:
        return jsonify({'error': 'Account ID parameter is required'}), 400
    
    account = Account.query.get(account_id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify({
        'id': account.id,
        'created_at': account.created_at,
        'name': account.name,
        'personal_id': account.personal_id
    })

@app.route('/api/get-item', methods=['GET'])
def get_item(item_id = None):
    if not item_id:
        item_id = request.args.get('item_id', default=None, type=int)
    if not item_id:
        return jsonify({'error': 'Item ID parameter is required'}), 400
    
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    # Get latest price for the item
    price = Price.query.filter_by(item_id=item.id).order_by(Price.created_at.desc()).first()
    # Get internal markup setting
    markup_setting_internal = Settings.query.filter_by(key='abs_markup_internal').first()
    abs_markup_internal = float(markup_setting_internal.value) if markup_setting_internal else 0.0
    markup_setting_external = Settings.query.filter_by(key='abs_markup_external').first()
    abs_markup_external = float(markup_setting_external.value) if markup_setting_external else 0.0

    # Calculate internal price unless already set
    if price:
        if price.internal is not None:
            price_internal = float(price.internal)
        else:
            price_internal = float(price.price) + abs_markup_internal
        
        if price.external is not None:
            price_external = float(price.external)
        else:
            price_external = float(price.price) + abs_markup_external

    else:
        price_internal = None
        price_external = None

    return jsonify({
        'id': item.id,
        'created_at': item.created_at,
        'name': item.name,
        'barcode': item.barcode,
        'category_id': item.category_id,
        'category': item.category.name if item.category else None,
        'price_internal': price_internal,
        'price_external': price_external
    })

if __name__ == '__main__':
    app.run(debug=True)