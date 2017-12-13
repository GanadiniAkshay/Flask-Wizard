import apiai 
import json

CLIENT_ACCESS_TOKEN = '154daa2432a848debc87ba3187d36f85'

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.session_id = 'kjlgkjslg'
request.query = "Hello"

response = request.getresponse()
print(json.loads(response.read().decode('utf-8')))