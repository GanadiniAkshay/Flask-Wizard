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

user_name = "akshay"
print("Your ozz account is used for accessing the GUI admin panel")
print("The admin panel lets you add/remove channels, access analytics and other services")
answer = str(input("Do you have an account on Ozz.ai?[Y/N]:"))

answer = answer.lower()
flag = True

while flag:
    if answer == 'y' or answer == 'yes' or answer == 'yeah' or answer == 'yup':
        email = str(input("Email:"))
        password = str(getpass.getpass('Password:'))

        url = "https://api.ozz.ai/auth"
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
        payload = {
            "email":email,
            "password":password
        }
        
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

        response = json.loads(response.text)

        if 'email' in response:
            print("\nNo account exists with that email. Try again")
        elif 'password' in response:
            print("\nInvalid password. Try Again")
        elif 'success' in response and response['success'] == 'true':
            flag = False
    else:
        #Setup Email
        prompt = "Email for admin panel:"
        email = str(input(prompt))
        #Setup Password
        prompt = "Password for admin panel (typing hidden):"
        password = str(getpass.getpass(prompt))

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
        print("Setting up admin account....")
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

        response = json.loads(response.text)

        if 'email' in response:
            print("\n\nAn email with that account already exists")
            
            while(True):
                result = input('Do you want to use the existing account or create a new one? \n 1) Use Existing 2) Create New \n Please choose 1 or 2:')
                try:
                    result = int(result)
                except ValueError:
                    continue
                if result == 1:
                    flag = False
                    break
                else:
                    break
        else:
            flag = False
            response_token = response['token']
            super_secret = "hdh%&D*%^^%$8767VHGSDFT5$%SD$658"

            data = jwt.decode(response_token,super_secret,algorithms=['HS256'])

            user_id = data["id"]
            print(user_id)
