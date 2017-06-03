from __future__ import absolute_import
from __future__ import print_function

import os
import json
import requests
import base64
import sys
import random

from flask import request
from actions import *

from .nlu import NLUParser

class FacebookHandler(object):
    """
        The facebook handler acts as the interface to handle all requests coming 
        from messenger.

        It parses the payload and responds
    """
    def __init__(self, pid, pat, verify_token, model, config, actions):
        self.pid = pid
        self.pat = pat
        self.verify_token = verify_token
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        if model == "":
            self.nlu = None
        else:
            self.nlu = NLUParser(model,config)

    def verify(self,*args,**kwargs):
        if request.args.get('hub.verify_token','') == self.verify_token:
            return request.args.get('hub.challenge','')
        else:
            return "Error, wrong validation token"

    def respond(self,*args,**kwargs):
        payload = request.get_data()
        for sender, message in self.messaging_events(payload):
            if sender != self.pid:
                if type(message) != str:
                    message = message.decode('utf-8')
                if self.nlu:
                    intent, entities = self.nlu.parse(message)
                    if intent in self.actions:
                        if type(self.actions[intent]) == list:
                            response = random.choice(self.actions[intent])
                            self.send_message(self.pat,sender,response)
                        else:
                            r = requests.get("https://graph.facebook.com/v2.6/"+ sender + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAAVKqE0ZBVvwBAOPhdm2Prx0EGXEKfdUI24xBcSEOEL4q2iywYYjiBiswZB8yus4VXRwLoFgeUvOZC5ZAhd831eacsozdjBruqiBwGLVcJbNXV005tvFCs3Ay6s7IsmRIgYClHexiCYe8hC23ijV8b1CfsnIWUTapDUKKjpZBMwZDZD")
                            r_data = json.loads(r.text)
                            session = {}
                            session['user'] = {
                                'id':sender,
                                'name':r_data['first_name'] + ' ' + r_data['last_name'],
                                'profile_pic':r_data['profile_pic'],
                                'locale':r_data['locale'],
                                'timezone':r_data['timezone'],
                                'gender':r_data['gender']
                            }
                            session['intent'] = intent
                            session['entities'] = entities
                            session['message'] = message
                            session['channel'] = 'facebook' 
                            func = eval(self.actions[intent])
                            func(session)
                else:
                    self.send_message(self.pat, sender, message)   
        return "responded"

    def messaging_events(self, payload):
        data = json.loads(payload)
        messaging_events = data["entry"][0]["messaging"]
        for event in messaging_events:
            if event["sender"]["id"] == self.pid:
                continue
            elif 'read' in event:
                continue
            elif 'delivery' in event:
                continue
            else:
                if "message" in event and "text" in event["message"]:
                    yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
                else:
                    yield event["sender"]["id"], "I can't echo this"

    def send_message(self, token, recipient, text):
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
