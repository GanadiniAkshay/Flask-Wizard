# from flask import Flask 
# from flask_wizard import Wizard 

# app = Flask(__name__)

# wizard = Wizard(app)

# if __name__ == '__main__':
#     app.run()
import getpass
import requests
import json
import time
import jwt
import os


# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUxLCJuYW1lIjoiQWtzaGF5IEt1bGthcm5pIiwiZW1haWwiOiJhZG1pbkBvenouYWkifQ.yKu6APBCJbT6nbFwmfscv4RyrOfUkMG_eUlG_8GZy-s"
# super_secret = "hdh%&D*%^^%$8767VHGSDFT5$%SD$658"

# data = jwt.decode(token,super_secret,algorithms=['HS256'])

# user_id = data["id"]
# print(user_id)

#Setup bot name
arguments = []
main_name = os.getcwd().split(os.sep)[-1]
if len(arguments) < 3:
    prompt = "Name of the bot? (default: " + main_name + "):"
    bot_name = str(input(prompt))
    if len(bot_name) == 0:
        bot_name = main_name
else:
    bot_name = ' '.join(arguments[2:])

prompt = "Name of the Creator:"
user_name = str(input(prompt))
if len(user_name) == 0:
    user_name = "wizard_user"

#Setup Password
prompt = "Set a password for admin panel (typing hidden):"
password = str(getpass.getpass(prompt))

user_name_email = user_name.replace(" ","")
time_email = str(time.time()).replace(".","")
email = "admin" + time_email + user_name_email + "@ozz.ai"

url = "https://api.ozz.ai/users"
headers = {
'content-type': "application/json",
'cache-control': "no-cache"
}
payload = {
    "name":user_name,
    "email":email,
    "password":password
}
response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
print(response.text)

response_token = json.loads(response.text)['token']
super_secret = "hdh%&D*%^^%$8767VHGSDFT5$%SD$658"

data = jwt.decode(response_token,super_secret,algorithms=['HS256'])

user_id = data["id"]

token = "kfkshjfsd"
nlp_name = "api"

url = "https://api.ozz.ai/bots"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'authorization': 'Bearer ' + response_token
}
payload = {
    "user_id":user_id,
    "name":bot_name,
    "platform":"wizard",
    "app_secret":token,
    "nlp_platform":nlp_name,
    "webhook":""
}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
print(response.text)
