from app import app
import os

if __name__ == '__main__':
    app.run(debug=True)
    # cert_path = os.path.expanduser('~/ssl/fullchain.pem')
    # key_path = os.path.expanduser('~/ssl/privkey.pem')
    # app.run(host='0.0.0.0', port=5000, ssl_context=(cert_path, key_path))