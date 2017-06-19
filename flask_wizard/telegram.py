from __future__ import absolute_import
from __future__ import print_function

import os
import json
import requests
import base64
import sys
import random
import telepot
import ast
import pprint

from flask import request
from actions import *

from .nlu import NLUParser

class TelegramHandler(object):
    """
        The facebook handler acts as the interface to handle all requests coming 
        from messenger.

        It parses the payload and responds
    """
    def __init__(self,bot_token, model, config, actions):
        self.bot_token = bot_token
        self.update_id = 0 
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        if model == "":
            self.nlu = None
        else:
            self.nlu = NLUParser(model,config)

    def responds(self,*args,**kwargs):
        data = request.get_data()
        if(type(data) == type(b"")):
                data = json.loads(data.decode())
        print (data)
        #print (data)
        if int(data["update_id"]) >= self.update_id:
            self.update_id = int(data["update_id"])
            if "message" in data:
                frm = data["message"]["from"]
                message = data["message"]["text"]
                IdOfSender = frm["id"]
                if self.nlu:
                    intent, entities = self.nlu.parse(message)
                    if intent in self.actions:   
                            if type(self.actions[intent]) == list:
                                    response = random.choice(self.actions[intent])
                                    self.send_message(IdOfSender,response)
                            else:
                                #func = eval(self.actions[intent])
                                session = {}
                                session['user']= {
                                    'id':IdOfSender
                                }
                                session['intent'] = intent
                                session['entities'] = entities
                                session['message'] = message
                                session['channel'] = 'telegram'
                                message = eval(self.actions[intent])
                                self.send_message(IdOfSender, message)                
                else:
                    self.send_message(IdOfSender, message)
        return 'Responded!'
        


    def send_message(self, id, text):
        """
            Send the message text to recipient with id recipient.
        """
        print ('Sending Mssg',text)
        if sys.version_info >= (3, 0):
            message = text
        else:
            message = text.decode('unicode_escape')
        token = self.bot_token
        bot = telepot.Bot(token)
        r = bot.sendMessage(id,text)
        print (r)
        