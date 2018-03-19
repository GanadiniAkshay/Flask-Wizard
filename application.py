from flask import Flask, request, render_template
from flask_wizard import Wizard

application = Flask(__name__)

wizard = Wizard(application)


if __name__ == "__main__":
    application.run(host='0.0.0.0',port=3000)