from app import app, response
from app.controller import CustomerController, UserController
from flask import request, render_template, session, redirect, url_for
from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('/login'))
        return f(*args, **kwargs)
    return decorated_function   

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    if 'jwt_token' in session:
        try:
            token = session['jwt_token']
            current_user = get_jwt_identity()
            return response.success(current_user, 'success')
        except:
            return response.error('Invalid token', 'error')
        
    return response.error('Token not found', 'error')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return UserController.login()
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('jwt_token', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        return UserController.store()
    else:
        return render_template('register.html')


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        return CustomerController.store()
    else:
        return CustomerController.index()

# link / customer detail
@app.route('/customer/<id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def customerDetail(id):
    if request.method == 'PUT':
    # if request.form.get('_edit'):
        return CustomerController.update(id)
    elif request.method == 'DELETE':
    # elif request.form.get('_delete'):
        return CustomerController.delete(id)
    else:
        return CustomerController.details(id)
    
@app.route('/createUser', methods=['POST'])
def createUser():
    return UserController.store()

@app.route('/uploadPhoto', methods=['POST'])
def uploadPhoto():
    return UserController.uploadPhoto()

# form tambah
@app.route('/add/link', methods=['GET'])
def addLink():
    return render_template('tambah.html')

# lihat link
@app.route('/link/<url>', methods=['GET'])
def link(url):
    return CustomerController.linkDetails(url)
