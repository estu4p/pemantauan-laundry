from app.model.customer import Customer, PhotoItem

from app import response, app, db
from flask import request, redirect, render_template, make_response, jsonify
import random
import string
from cryptography.fernet import Fernet


def index():
    try:
        customer = Customer.query.all()
        data = formatArray(customer)
        # return response.success(data, "success")
        key_fernet = app.config['KEY_FERNET']
        decrypted_data = []
        for entry in data:
            decrypt_entry = entry.copy()
            decrypt_entry['phone'] = decrypt_data(entry['phone'], key_fernet)
            decrypt_entry['address'] = decrypt_data(entry['address'], key_fernet)
            decrypted_data.append(decrypt_entry)

        # return response.success(decrypted_data, "success")
        return render_template('listLink.html', data=decrypted_data)
    except Exception as e:
        print(e)

def details(id):
    try:
        customer = Customer.query.filter_by(id=id).first()
        photos = PhotoItem.query.filter_by(customer_id=id).all()

        if not customer:
            return response.badRequest([], 'Empty....')
        
        key_fernet = app.config['KEY_FERNET']


        dataPhoto = formatDetail(photos)
        data = singleDetailCustomer(customer, dataPhoto)
        data['address'] = decrypt_data(data['address'], key_fernet)
        data['phone'] = decrypt_data(data['phone'], key_fernet)

        # return response.success(data, "success")
        return render_template('edit.html', customer=data)
    except Exception as e:
        print(e)

def store():
    try:
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        notes = request.form.get('notes')
        status = request.form.get('status')
        price = request.form.get('price')

        process_str = request.form.get('process')
        process = int(process_str)

        character = string.ascii_letters + string.digits
        url = ''.join(random.choices(character, k=10))

        key_fernet = app.config['KEY_FERNET']
        customer = Customer(name=name, phone=phone, address=address, notes=notes, status=status, process=process, price=price ,url=url , key_fernet=key_fernet)

        db.session.add(customer)
        db.session.commit()

        # return response.success('', 'success')
        return redirect('/customer')
    except Exception as e:
        print(e)

def update(id):
    try:
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        notes = request.form.get('notes')
        status = request.form.get('status')
        process = request.form.get('process')
        price = request.form.get('price')

        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return response.badRequest([], 'Empty....')
        
        key_fernet = app.config['KEY_FERNET']

        phone = encrypt_data(phone, key_fernet)
        address = encrypt_data(address, key_fernet)

        customer.name = name
        customer.phone = phone
        customer.address = address
        customer.notes = notes
        customer.status = status
        customer.process = process
        customer.price = price

        db.session.commit()

        # return response.success('', 'success')
        return redirect('/customer')
    except Exception as e:
        print(e)

def delete(id):
    try:
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return response.badRequest([], 'Empty....')

        db.session.delete(customer)
        db.session.commit()

        # return response.success('', 'success')
        return redirect('/customer')
    except Exception as e:
        print(e)

def linkDetails(url):
    try:
        customer = Customer.query.filter_by(url=url).first()
        photos = PhotoItem.query.filter_by(customer_id=id).all()

        if not customer:
            return response.badRequest([], 'Empty....')
        
        key_fernet = app.config['KEY_FERNET']

        dataPhoto = formatDetail(photos)
        data = singleDetailCustomer(customer, dataPhoto)
        data['address'] = decrypt_data(data['address'], key_fernet)
        data['phone'] = decrypt_data(data['phone'], key_fernet)

        # return response.success(data, "success")
        return render_template('linkDetail.html', customer=data)
    except Exception as e:
        print(e)

def singleDetailCustomer(data, photos):
    data = {
        'id': data.id,
        'name': data.name,
        'phone': data.phone,
        'address': data.address,
        'notes': data.notes,
        'status': data.status,
        'price': data.price,
        'process': data.process,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
        'photos': photos
    }

    return data

def formatArray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))

    return array

def singleObject(data):
    data = {
        'id': data.id,
        'name': data.name,
        'phone': data.phone,
        'address': data.address,
        'notes': data.notes,
        'status': data.status,
        'price': data.price,
        'url': data.url,
        'process': data.process,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
    }

    return data

def formatDetail(data):
    array = []
    
    for i in data:
        array.append(singlePhoto(i))

    return array

def singlePhoto(data):
    data = {
        'id': data.id,
        'photo': data.photo,
        'created_at': data.created_at,
        'updated_at': data.updated_at,
    }

    return data

def decrypt_data(data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data).decode()
    return decrypted_data

def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data


# API
def apiCustomer():
    try:
        customer = Customer.query.all()
        data = formatArray(customer)
        key_fernet = app.config['KEY_FERNET']
        decrypted_data = []
        for entry in data:
            decrypt_entry = entry.copy()
            decrypt_entry['phone'] = decrypt_data(entry['phone'], key_fernet)
            decrypt_entry['address'] = decrypt_data(entry['address'], key_fernet)
            decrypted_data.append(decrypt_entry)

        return response.success(decrypted_data, "success")
    except Exception as e:
        print(e)

def apiDetails(id):
    try:
        customer = Customer.query.filter_by(id=id).first()
        photos = PhotoItem.query.filter_by(customer_id=id).all()

        if not customer:
            return response.badRequest([], 'Empty....')
        
        key_fernet = app.config['KEY_FERNET']


        dataPhoto = formatDetail(photos)
        data = singleDetailCustomer(customer, dataPhoto)
        data['address'] = decrypt_data(data['address'], key_fernet)
        data['phone'] = decrypt_data(data['phone'], key_fernet)

        return response.success(data, "success")
    except Exception as e:
        print(e)

def apiStore():
    try:
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        notes = request.form.get('notes')
        status = request.form.get('status')
        price = request.form.get('price')

        process_str = request.form.get('process')
        process = int(process_str)

        character = string.ascii_letters + string.digits
        url = ''.join(random.choices(character, k=10))

        key_fernet = app.config['KEY_FERNET']
        customer = Customer(name=name, phone=phone, address=address, notes=notes, status=status, process=process, price=price ,url=url , key_fernet=key_fernet)

        db.session.add(customer)
        db.session.commit()

        customerDetail = singleDetailCustomer(customer, [])
        return response.success(customerDetail, 'success')
    except Exception as e:
        print(e)

def apiUpdate(id):
    try:
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        notes = request.form.get('notes')
        status = request.form.get('status')
        process = request.form.get('process')
        price = request.form.get('price')

        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return response.badRequest([], 'Empty....')
        
        key_fernet = app.config['KEY_FERNET']

        phone = encrypt_data(phone, key_fernet)
        address = encrypt_data(address, key_fernet)

        customer.name = name
        customer.phone = phone
        customer.address = address
        customer.notes = notes
        customer.status = status
        customer.process = process
        customer.price = price

        db.session.commit()

        customerDetail = singleDetailCustomer(customer, [])
        return response.success(customerDetail, 'success')
    except Exception as e:
        print(e)

def apiDelete(id):
    try:
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return response.badRequest([], 'Empty....')

        db.session.delete(customer)
        db.session.commit()

        return response.success('delelte', 'success')
    except Exception as e:
        print(e)