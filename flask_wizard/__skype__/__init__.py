"""Defines Skype API
   Contains:
    -Class ~ SkypeBot
"""

import requests, sys, threading, time, json
from . import internal

class SkypeBot:
    
    _data = json.loads("{}")
    _botID = "someID"
    _url = "someURL"

    def __init__(self, client_id, client_secret):

        def token_func():
            global token
            payload = "grant_type=client_credentials&client_id="+client_id+"&client_secret="+client_secret+"&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default"
            response = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token?client_id="+client_id+"&client_secret="+client_secret+"&grant_type=client_credentials&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default",data=payload,headers={"Content-Type":"application/x-www-form-urlencoded"})
            data = response.json()
            token = data["access_token"]

        def runit():
            while True:
                token_func()
                time.sleep(3000)

        global _botID, _url
        _botID = client_id
        self.t = threading.Thread(target=runit)
        self.t.daemon = True
        self.t.start()
        
    "Functions:"
    def sendTextMessage(self, text, data=None):
        data = data or self.getData()
        return internal.SendTextMessage(token, self.getService(data), self.getSender(data), self.getBotId(), text)

    def sendMessage(self, message, data=None):
        data = data or self.getData()
        return internal.Send(token, self.getService(data), self.getSender(data), self.getBotId(), message)

    def createMessage(self, text, data=None):
        data = data or self.getData()
        return internal.CreateBasicPayload(self.getBotId(), text, self.getSender(data))

    def addButton(self, message, title, value, btype=None):
        btype = btype or "imBack"
        return internal.AddButton(message, btype, title, value)

    def addImage(self, message, url):
        return internal.AddImage(message, url)        

    def addMedia(self, message, imageurl, mediaurl):
        return internal.AddMedia(message, imageurl, mediaurl)
   
    def addCard(self, message, title, subtitle, text):
         return internal.AddCardDetails(message, title, subtitle, text)

    "All json data hooks start here:"
    def getService(self, data = None):
        data = data or self.getData()
        return data['serviceUrl']

    def getSender(self, data = None):
        data = data or self.getData()
        return data['conversation']['id']

    def getUserId(self, data = None):
        data = data or self.getData()
        return data['from']['id']

    def getUserName(self, data = None):
        data = data or self.getData()
        name = ""
        if "name" in data['from']:
          name = data['from']['name']
        return name

    def getUserStore(self, data = None):
        data = data or self.getData()
        return self.getUserName(data)+self.getUserId(data)

    def getType(self, data = None):
        data = data or self.getData()
        return data['type']

    def getText(self, data = None):
        data = data or self.getData()
        return data['text']

    def getBotId(self):
        global _botID
        return _botID

    def setData(self, data):
        global _data
        _data = data

    def getData(self):
        global _data
        return _data
