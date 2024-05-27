from app.model.customer import Customer, PhotoItem

from app import response, app, db
from flask import request, redirect, render_template
import random
import string

def index():
    try:
        customer = Customer.query.all()
        data = formatArray(customer)
        return response.success(data, "success")
        # return render_template('listLink.html', data=data)
    except Exception as e:
        print(e)

def details(id):
    try:
        customer = Customer.query.filter_by(id=id).first()
        photos = PhotoItem.query.filter_by(customer_id=id).all()

        if not customer:
            return response.badRequest([], 'Empty....')
        
        dataPhoto = formatDetail(photos)
        data = singleDetailCustomer(customer, dataPhoto)
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

        process_str = request.form.get('process')
        process = int(process_str)

        character = string.ascii_letters + string.digits
        url = ''.join(random.choices(character, k=10))

        customer = Customer(name=name, phone=phone, address=address, notes=notes, status=status, process=process, url=url)

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

        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return response.badRequest([], 'Empty....')

        customer.name = name
        customer.phone = phone
        customer.address = address
        customer.notes = notes
        customer.status = status
        customer.process = process

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

def singleDetailCustomer(data, photos):
    data = {
        'id': data.id,
        'name': data.name,
        'phone': data.phone,
        'address': data.address,
        'notes': data.notes,
        'status': data.status,
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

def linkDetails(url):
    try:
        customer = Customer.query.filter_by(url=url).first()
        # photos = PhotoItem.query.filter_by(customer_id=id).all()

        if not customer:
            return response.badRequest([], 'Empty....')
        
        # dataPhoto = formatDetail(photos)
        # data = singleDetailCustomer(customer, dataPhoto)
        # return response.success(data, "success")
        return render_template('linkDetail.html', customer=customer)
    except Exception as e:
        print(e)