from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)
    personal_id = db.Column(db.Text, nullable=False)

class ItemCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    key = db.Column(db.Text, nullable=False, unique=True)
    value = db.Column(db.Text, nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account')
    void = db.Column(db.Boolean, nullable=False, default=False)
    items = db.relationship('SalesItem')

    @property
    def total(self):
        return sum(item.sale_price * item.quantity for item in self.items)

class SalesItem(db.Model):
    sale_id = db.Column( db.Integer, db.ForeignKey('sale.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    sale_price = db.Column(db.Numeric(60, 2), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.Text, nullable=False)
    barcode = db.Column(db.Text, nullable=False)
    category_id = db.Column('category', db.Integer, db.ForeignKey('item_category.id'), nullable=False)
    category = db.relationship('ItemCategory')

class Price(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(60, 2), nullable=False)
    external = db.Column(db.Numeric(60, 2))
    internal = db.Column(db.Numeric(60, 2))

class BarcodeLookup(db.Model):
    barcode = db.Column(db.Text, nullable=False, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    source_table = db.Column(db.Text, nullable=False) 