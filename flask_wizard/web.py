from __future__ import absolute_import
from __future__ import print_function

import json
import requests
import random

from flask import request
from actions import *

from .ozz import OzzParser

class HttpHandler(object):
    """
        HttpHandler acts as the interface to provide the Http
        channel for your bot. 
        It accepts the incoming message as a post request and then sends the 
        response as a Http response
    """
    def __init__(self,model,config, actions, ozz_guid, redis_db, mongo):
        self.redis_db = redis_db
        self.mongo = mongo
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        if ozz_guid != "":
            self.nlu = OzzParser(ozz_guid)
        else:
            self.nlu = None
        print("HTTP endpoint - /api/messages/http")

    def response(self, *args, **kwargs):
        """
          Take the message, parse it and respond
        """
        payload = request.get_data()
        payload = payload.decode('utf-8')
        data = json.loads(payload)
        message = data["message"]
        if self.nlu:
            intent, entities, response = self.nlu.parse(message)
            if intent in self.actions:
                if type(self.actions[intent]) == list:
                    response = random.choice(self.actions[intent])
                else:
                    session = {}
                    session['user'] = {
                                'id':request.remote_addr,
                                'name':'User',
                                'profile_pic':'None',
                                'locale':'en-US',
                                'timezone':'0',
                                'gender':'None'
                            }
                    session['intent'] = intent
                    session['entities'] = entities
                    session['message'] = message
                    session['channel'] = 'web'
                    func = eval(self.actions[intent])
                    response = func(session)
                return response
            elif response != "":
                return response
            else:
                return "Sorry, I couldn't understand that"
        else:
            return str(message)