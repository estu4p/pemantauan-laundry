from app import db
from datetime import datetime
from cryptography.fernet import Fernet
class Customer(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    phone = db.Column(db.String(255))
    photo_item = db.relationship('PhotoItem', backref='customer', lazy='dynamic')
    address = db.Column(db.String(255))
    notes = db.Column(db.String(255))
    status = db.Column(db.String(25))
    process = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(25))
    url = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, phone, address, notes, status, process, price, url, key_fernet):
        self.name = name
        self.phone = encrypt_data(phone, key_fernet)
        self.address = encrypt_data(address, key_fernet)
        self.notes = notes
        self.status = status
        self.process = process
        self.price = price
        self.url = url    

    # def get_phone(self, key_fernet):
    #     return decrypt_data(self.phone, key_fernet)
    
    # def get_address(self, key_fernet):
    #     return decrypt_data(self.address, key_fernet)

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
    

def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data).decode()
    return decrypted_data