from flask import Flask
from flask_wizard import Wizard 

app = Flask(__name__, static_url_path='', static_folder='public')
wizard = Wizard(app)

@app.route('/admin')
def admin():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()