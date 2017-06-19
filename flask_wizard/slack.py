from __future__ import absolute_import
from __future__ import print_function

import os
import json
import requests
import base64
import sys
import random
from slackclient import SlackClient

from flask import request
from actions import *

from .nlu import NLUParser

class SlackHandler(object):
    """
        The facebook handler acts as the interface to handle all requests coming 
        from messenger.

        It parses the payload and responds
    """
    def __init__(self, pid, pad , verify_token,bot_token, model, config, actions):
        self.sc = SlackClient(bot_token) 
        self.pid = pid  
        self.pad = pad
        self.verify_token = verify_token
        self.bot_token = bot_token
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        if model == "":
            self.nlu = None
        else:
            self.nlu = NLUParser(model,config)

    def respond(self,*args,**kwargs):
        data = request.get_data()
        print (data)
        if(type(data) == type(b"")):
                data = json.loads(data.decode())
        if self.verify_token  == data['token']:
            if "event" in  data:
                if "message" == data["event"]['type']:
                    message = data["event"]["text"]
                    print (data["event"])
                    if 'subtype' not in data["event"]:
                        id = data["event"]["channel"]
                        if self.nlu:
                            intent, entities = self.nlu.parse(message)
                            if intent in self.actions:   
                                if type(self.actions[intent]) == list:
                                    response = random.choice(self.actions[intent])
                                    self.send_message(id,response)
                                else:
                                    #func = eval(self.actions[intent])
                                    session = {}
                                    session['user']= {
                                        'id':data["event"]["channel"]
                                    }
                                    session['intent'] = intent
                                    session['entities'] = entities
                                    session['message'] = message
                                    session['channel'] = 'slack'
                                    message = eval(self.actions[intent])
                                    self.send_message(id, message)
                                    #func(session)
                        else:
                             self.send_message(id, message)
            return "Responded!"  
        else:
            print ('Error verifying token')

    def send_message(self, id, text):
        """
            Send the message text to recipient with id recipient.
        """ 
        print ('Sending Mssg',text)
        if sys.version_info >= (3, 0):
            message = text
        else:
            message = text.decode('unicode_escape')
        
        r = requests.post('https://slack.com/api/chat.meMessage',
                        headers={'Content-type': 'application/x-www-form-urlencoded'},
                        data={"token":self.bot_token,"text":message,"as_user":True,"channel":id})

        print (r.text)
        """
        n = 2
        while n:
            if self.sc.rtm_connect():
                r = self.sc.api_call("chat.postMessage", channel=id,
                                       text=text, as_user=True)
                #print (r)
                break
            else:
                n-=1
                print ('Error sending message')
        """