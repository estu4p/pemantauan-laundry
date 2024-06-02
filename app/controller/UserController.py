from app.model.user import User
from app.model.customer import PhotoItem

from flask_jwt_extended import *
from app import response, app, db, uploadConfig
from flask import request, session, url_for, redirect, render_template
import uuid
import os
from datetime import datetime
import datetime
from werkzeug.utils import secure_filename

def store():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(username=username, email=email, password=password)
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()

        # return response.success('', 'success')
        return render_template('login.html')
    except Exception as e:
        print(e)

def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            return response.badRequest([], 'Empty....')

        if not user.checkPassword(password):
            return response.badRequest([], 'Password not match....')

        data = singleObject(user)

        expires = datetime.timedelta(days=3)
        expires_refresh = datetime.timedelta(days=3)

        access_token = create_access_token(identity=data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=data, expires_delta=expires_refresh)

        session['jwt_token'] = access_token

        # return response.success({
        #     'data': data,
        #     'access_token': access_token,
        #     'refresh_token': refresh_token,
        # }, 'success')
        return render_template('index.html')
    
    except Exception as e:
        print(e)

def singleObject(data):
    data = {
        'id': data.id,
        'username': data.username,
        'email': data.email,
        'created_at': data.created_at,
        'updated_at': data.updated_at
    }

    return data

def uploadPhoto():
    try:
        # check if the post request has the file part
        if 'file' not in request.files:
            return response.badRequest([], 'No file part')

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return response.badRequest([], 'No selected file')

        if file and uploadConfig.allowed_file(file.filename):
            uuid = uuid.uuid4()
            filename = secure_filename(file.filename)
            renamefile = str(uuid) + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], renamefile))

            photoItem = PhotoItem(photo=renamefile, created_at=datetime.now())
            db.session.add(photoItem)
            db.session.commit()

            return response.success('', 'success')
        else:
            return response.badRequest([], 'Allowed file type is png, jpg, jpeg')
    except Exception as e:
        print(e)


# API
def apiStore():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(username=username, email=email, password=password)
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()

        return response.success('', 'success')
    except Exception as e:
        print(e)

def apiLogin():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            return response.badRequest([], 'Empty....')

        if not user.checkPassword(password):
            return response.badRequest([], 'Password not match....')

        data = singleObject(user)

        expires = datetime.timedelta(days=3)
        expires_refresh = datetime.timedelta(days=3)

        access_token = create_access_token(identity=data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=data, expires_delta=expires_refresh)

        session['jwt_token'] = access_token

        return response.success({
            'data': data,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, 'success')
    
    except Exception as e:
        print(e)