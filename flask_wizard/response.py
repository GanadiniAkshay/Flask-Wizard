import os
import json
import requests
import base64
import sys

class replies(object):
    """
    The quick reply class for individual
    choice objects inside the bigger full quick reply
    """
    def __init__(self,type='text',title='__Nonefined__',payload='__Nonefined__',img="__Nonefined__"):
        self.type = type
        self.title = title
        self.payload = payload
        self.img   = img

class quick_reply(object):
    """
    Quick Reply class to easily 
    create quick reply objects
    """
    def __init__(self, text, replies):
        self.text = text
        self.replies = []

        for reply in replies:
            new_reply = {}
            new_reply['content_type'] = reply.type
            if reply.title != '__Nonefined__':
                new_reply['title'] = reply.title
            if reply.payload != '__Nonefined__':
                new_reply['payload'] = reply.payload
            if reply.img != '__Nonefined__':
                new_reply['image_url'] = reply.img
            self.replies.append(new_reply)
        
        self.response = {
                            "text":text,
                            "quick_replies": self.replies
                        }

def send(session,response):
    channel = session["channel"]
    if channel == 'web':
        return str(response)
    if channel == 'facebook':
        config = os.path.join(os.getcwd(),'config.json')
        with open(config,"r") as jsonFile:
            data = json.load(jsonFile)
            facebook_pat = data["channels"]["facebook"]["pat"]
            recipient = session["user"]["id"]
            if type(response) == "str":
                if sys.version_info >= (3, 0):
                    message = response
                    message = {"text":message}
                else:
                    message = response.decode('unicode_escape')
                    message = {"text":message}
            else:
                message = response.response
            
            r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                params={"access_token": facebook_pat},
                data=json.dumps({
                "recipient": {"id": recipient},
                "message": message
                }),
                headers={'Content-type': 'application/json'})
            if r.status_code != requests.codes.ok:
                print(r.text)


    
