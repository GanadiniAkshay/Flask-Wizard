from flask import Flask 
from flask_wizard import Wizard 

app = Flask(__name__)
app.config["VERIFY_TOKEN"] = 'this_is_the_verify_token'
app.config["PAT"] = 'EAADr9SgIAX4BAHEnUvkC7zGyYq2VoxVC4caukaJ7fNaWEaECsQIzecUauy6fBtbJ2JARPZAHCnpIbDz8mGGZBBrHMGZCOKCZBMrx8ILB5ZAqxEerFrfOAOhI924o9vdjC8mgkJ1nybZBZAK2BYmFDWldZAFTJNclWoxfJWRMLS5drAZDZD'


wizard = Wizard(app)

if __name__ == '__main__':
    app.run()