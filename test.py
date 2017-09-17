from flask import Flask, request, render_template
from flask_wizard import Wizard

app = Flask(__name__)

wizard = Wizard(app)

@app.route("/")
def hello():
    return "hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)