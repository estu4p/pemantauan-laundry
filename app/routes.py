from app import app, response
from app.controller import CustomerController, UserController
from flask import request, render_template, session, redirect, url_for
from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required, decode_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'jwt_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function   

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    if 'jwt_token' in session:
        try:
            token = session['jwt_token']
            # token = get_jwt_identity()
            # decode = decode_token(token)
            # user_identity = decode['sub']['username']
            return response.success(token, 'success')
        except:
            return response.badRequest('Invalid token', 'error')
        
    return response.badRequest('Token not found', 'error')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chatbot.html')

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
@login_required
def customer():
    if request.method == 'POST':
        return CustomerController.store()
    else:
        return CustomerController.index()

# link / customer detail
@app.route('/customer/<id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
@login_required
def customerDetail(id):
    # if request.method == 'PUT':
    if request.form.get('_edit'):
        return CustomerController.update(id)
    # elif request.method == 'DELETE':
    elif request.form.get('_delete'):
        return CustomerController.delete(id)
    else:
        return CustomerController.details(id)
    
@app.route('/createUser', methods=['POST'])
@login_required
def createUser():
    return UserController.store()

@app.route('/uploadPhoto', methods=['POST'])
@login_required
def uploadPhoto():
    return UserController.uploadPhoto()

# form tambah
@app.route('/add/link', methods=['GET'])
@login_required
def addLink():
    return render_template('tambah.html')

# lihat link
@app.route('/link/<url>', methods=['GET'])
def link(url):
    return CustomerController.linkDetails(url)


# api
@app.route('/api/login', methods=['POST'])
def apiLogin():
    return UserController.apiLogin()
    
@app.route('/api/logout')
def apiLogout():
    session.pop('jwt_token', None)
    return response.success('Logout', 'success')

@app.route('/api/register', methods=['POST'])
def apiRegister():
    return UserController.apiStore()

@app.route('/api/customer', methods=['GET', 'POST'])
@login_required
def apiCustomer():
    if request.method == 'POST':
        return CustomerController.apiStore()
    else:
        return CustomerController.apiCustomer()

# link / customer detail
@app.route('/api/customer/<id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def apiCustomerDetail(id):
    if request.method == 'PUT':
    # if request.form.get('_edit'):
        return CustomerController.apiUpdate(id)
    elif request.method == 'DELETE':
    # elif request.form.get('_delete'):
        return CustomerController.apiDelete(id)
    else:
        return CustomerController.apiDetails(id)
