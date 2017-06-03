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
from . import __skype__

from .nlu import NLUParser

class SkypeHandler(__skype__.SkypeBot):
    """
        The skype handler acts as the interface to handle all requests coming 
        from messenger.

        It parses the payload and responds
        The SkypeBot class will handle tokens on its own(refresh of 60 seconds)
    """
    def __init__(self, cid, cs, model, config, actions):
        self.cid = cid
        self.cs = cs
        self.bot = __skype__.SkypeBot(cid, cs)
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        if model == "":
            self.nlu = None
        else:
            self.nlu = NLUParser(model, config)
        super().__init__(client_id = cid, client_secret = cs)


    def skyperespond(self,*args,**kwargs):
        data = request.get_data()
        #data may be read as binary
        if(type(data) == type(b"")):
            data = json.loads(data.decode())
        self.setData(data)
        messageType = self.getType(data)
        print(messageType)
        if messageType == "ping":
            #TODO add ping message set by user
            pass
        elif messageType == "typing":
            #TODO add ping message set by user
            pass
        elif messageType == "contactRelationUpdate":
            if self.getAction(data):
                if "add":
                    #TODO add relation
                    pass
                if "remove":
                    #TODO remove relation
                    pass
        elif messageType == "conversationUpdate":
            #TODO hello messagee
            pass
        elif messageType == "message":
            message = self.getText(data)
            if self.nlu:
              message = self.getText(data)
              intent, entities = self.nlu.parse(message)
              if type(self.actions[intent]) == list:
                self.sendTextMessage(random.choice(self.actions[intent]), data)
              else:
                func = eval(self.actions[intent])
                session = {}
                session['user'] = {
                        'id':self.getUserId(),
                        'name':self.getUserName(),
                        'uid':self.getUserStore()
                }
                session['intent'] = intent
                session['entities'] = entities
                session['message'] = message
                session['channel'] = 'skype'
                self.sendTextMessage(eval(self.actions[intent])(session), data)
            else:
              print("NLU Error")
        return "responded"
