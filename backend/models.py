from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    name = db.Column(db.Text, nullable=False)
    personal_id = db.Column(db.Text, nullable=False)
    
class ItemCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    name = db.Column(db.Text, nullable=False)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    key = db.Column(db.Text, nullable=False, unique=True)
    value = db.Column(db.Text, nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account')
    void = db.Column(db.Boolean, nullable=False, default=False)
    items = db.relationship('SaleItem')

    @property
    def total(self):
        return sum(item.sale_price * item.quantity for item in self.items)

class SaleItem(db.Model):
    sale_id = db.Column( db.Integer, db.ForeignKey('sale.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    sale_price = db.Column(db.Numeric(60, 2), nullable=False)
    sale = db.relationship('Sale', back_populates='items')
    item = db.relationship('Item')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    name = db.Column(db.Text, nullable=False)
    barcode = db.Column(db.Text, nullable=False)
    category_id = db.Column('category', db.Integer, db.ForeignKey('item_category.id'), nullable=False)
    category = db.relationship('ItemCategory')

class Price(db.Model):
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    price = db.Column(db.Numeric(60, 2), nullable=False)
    external = db.Column(db.Numeric(60, 2))
    internal = db.Column(db.Numeric(60, 2))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=True)
    account = db.relationship('Account')
    sale = db.relationship('Sale', uselist=False, backref='transaction')
    amount = db.Column(db.Numeric(60, 2), nullable=False)

class BarcodeLookup(db.Model):
    barcode = db.Column(db.Text, nullable=False, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    source_table = db.Column(db.Text, nullable=False) 

class AccountDebt(db.Model):
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, primary_key=True)
    account = db.relationship('Account')
    total_sale = db.Column(db.Numeric(60, 2), nullable=False, default=0.0)
    total_deposit = db.Column(db.Numeric(60, 2), nullable=False, default=0.0)
    total_debt = db.Column(db.Numeric(60, 2), nullable=False, default=0.0)