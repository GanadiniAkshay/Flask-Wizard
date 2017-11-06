import os
import json
import requests
import base64
import sys


class button(object):
    """
    Used to create buttons of different types
    """
    def __init__(self, type,title="__Nonefined__",url="__Nonefined__",payload="__Nonefined__",webview_height_ratio="full",messenger_extensions=False, fallback_url="__Nonefined__"): 
        self.type = type
        self.url = url
        self.title = title
        self.payload = payload


class actions(object):
    """
    Used to create actions for template elements
    """
    def __init__(self, type,url="__Nonefined__",messenger_extensions=False,webview_height_ratio="full"):
        self.type = type
        if url != "_Nonefined__":
            self.url = url

        self.messenger_extensions = messenger_extensions
        self.webview_height_ratio = webview_height_ratio



class template_element(object):
    """
        Used to create elements inside templates
    """
    def __init__(self,title="__Nonefined__",image_url="__Nonefined__",subtitle="__Nonefined__",action="__Nonefined__",buttons=[]):
        if title != "_Nonefined__":
            self.title = title
        
        if image_url != "_Nonefined__":
            self.image_url = image_url

        if subtitle != "_Nonefined__":
            self.subtitle = subtitle

        if action != "_Nonefined__":
            self.action = action

        self.buttons = buttons

class template(object):
    """
     Used to create templates
    """
    def __init__(self, type, text="", buttons=[], elements=[]):
        self.template_type = type
        self.text = text
        self.buttons = []


        self.elements = []

        for element in elements:
            new_element = {}
            if element.title != "__Nonefined__":
                new_element["title"] = element.title
            if element.image_url != "__Nonefined__":
                new_element["image_url"] = element.image_url
            if element.subtitle != "__Nonefined__":
                new_element["subtitle"] = element.subtitle
            if element.action != "__Nonefined__":
                new_element["default_action"] = {
                                    "type":element.action.type
                                 }
                if element.action.url != "_Nonefined__":
                    new_element["default_action"]["url"] = element.action.url 
                new_element["default_action"]["webview_height_ratio"] = element.action.webview_height_ratio 
            new_element["buttons"]=[]
            for button in element.buttons:
                new_button = {}
                new_button["type"] = button.type
                if button.title != "__Nonefined__":
                    new_button["title"] = button.title
                if button.url != "__Nonefined__":
                    new_button["url"]  = button.url
                if button.payload != "__Nonefined__":
                    new_button["payload"] = button.payload
                new_element["buttons"].append(new_button)
            self.elements.append(new_element)
            

        if self.template_type == "generic":
            self.response = {
                                    "attachment":{
                                        "type":"template",
                                        "payload":{
                                            "template_type":"generic",
                                            "elements":self.elements
                                        }
                                    }
                                 }
        else:
            for button in buttons:
                new_button = {}
                new_button["type"] = button.type
                if button.title != "__Nonefined__":
                    new_button["title"] = button.title
                if button.url != "__Nonefined__":
                    new_button["url"]  = button.url
                if button.payload != "__Nonefined__":
                    new_button["payload"] = button.payload
                self.buttons.append(new_button)


            self.response = {
                                "attachment":{
                                    "type":"template",
                                    "payload":{
                                        "template_type":self.template_type,
                                        "text":self.text,
                                        "buttons":self.buttons
                                    }
                                }
                            }

class attachement(object):
    """
    Used to send voice, video or image attachements
    """
    def __init__(self, type, url):
        self.type = type
        self.payload = {"url":url}

        self.response = {
                            "attachment":{
                                    "type":self.type,
                                    "payload":self.payload
                            }
                        }

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
            if type(response) == type("str"):
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


def sendTyping(session,action="on"):
    channel = session["channel"]
    if channel == 'web':
        return "hey"
    if channel == 'facebook':
        if action == "on":
            action = "typing_on"
        else:
            action = "typing_off"
        config = os.path.join(os.getcwd(),'config.json')
        with open(config,"r") as jsonFile:
            data = json.load(jsonFile)
            facebook_pat = data["channels"]["facebook"]["pat"]
            recipient = session["user"]["id"]
            r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                params={"access_token": facebook_pat},
                data=json.dumps({
                "recipient": {"id": recipient},
                "sender_action": action
                }),
                headers={'Content-type': 'application/json'})
            if r.status_code != requests.codes.ok:
                print(r.text)


def sendSeen(session):
    channel = session["channel"]
    if channel == 'web':
        return "hey"
    if channel == 'facebook':
        config = os.path.join(os.getcwd(),'config.json')
        with open(config,"r") as jsonFile:
            data = json.load(jsonFile)
            facebook_pat = data["channels"]["facebook"]["pat"]
            recipient = session["user"]["id"]
            r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                params={"access_token": facebook_pat},
                data=json.dumps({
                "recipient": {"id": recipient},
                "sender_action": "mark_seen"
                }),
                headers={'Content-type': 'application/json'})
            if r.status_code != requests.codes.ok:
                print(r.text)
    
