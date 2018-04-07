from flask import Flask, request, render_template, jsonify
from flask_wizard import Wizard

import os 
import json
import redis
import sys
import requests

application = Flask(__name__)

wizard = Wizard(application)

config_path = os.path.join(os.getcwd(),'config.json')
with open(config_path,'r') as jsonFile:
	data = json.load(jsonFile)
	pat = data["channels"]["facebook"]["pat"]
	host = data['redis']['host']
	if data['redis']['port'] and data['redis']['port'] != "":
		port = data['redis']['port']
	else:
		port = 6379
	
	if data['redis']['password']:
		password = data['redis']['password']
	else:
		password = ""
redis_db = redis.StrictRedis(host=host,port=int(port),password=password)
print(redis_db)

@application.route("/login")
def login():
	return render_template('login.html')

@application.route("/getaccesstoken",methods=["POST"])
def token():
	pdata = request.get_json()
	eat = pdata['at']
	uid = pdata['uid']

	key = uid
	if redis_db.exists(key):
		return jsonify({"logged_in":True})
	else:
		event = {
			"uid":uid,
			"eat":eat,
			"pat":pat
		}
		redis_db.hmset(key, event)
		redis_db.expire(key, 85000)

		prompt_key = "prompt"
		event = {
			"followup":"link_account.verify_phone"
		}

		redis_db.hmset(prompt_key, event)
		redis_db.expire(key, 85000)

		send_message(pat,uid,"You need to verify your number using OTP")
		send_message(pat,uid,"What is your phone number?")
		return jsonify({"pat":pat,"eat":eat,"uid":uid})

def send_message(token, recipient, text):
	"""Send the message text to recipient with id recipient.
	"""
	if sys.version_info >= (3, 0):
		message = text
	else:
		message = text.decode('unicode_escape')
	
	r = requests.post("https://graph.facebook.com/v2.6/me/messages",
		params={"access_token": token},
		data=json.dumps({
		"recipient": {"id": recipient},
		"message": {"text": message}
		}),
		headers={'Content-type': 'application/json'})
	if r.status_code != requests.codes.ok:
		print(r.text)


if __name__ == "__main__":
    application.run(host='0.0.0.0',port=5000)