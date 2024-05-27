from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    phone = db.Column(db.String(20))
    photo_item = db.relationship('PhotoItem', backref='customer', lazy='dynamic')
    address = db.Column(db.String(120))
    notes = db.Column(db.String(255))
    status = db.Column(db.String(25))
    process = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<Customer {}>'.format(self.name)
    
class PhotoItem(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('customer.id', ondelete='CASCADE'))
    photo = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<PhotoItem {}>'.format(self.photo)