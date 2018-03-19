from __future__ import absolute_import
from __future__ import print_function

import json
import requests
import random
import apiai
import sys
import uuid
import time

from timeit import default_timer as timer

from flask import request,jsonify
from actions import *


class HttpHandler(object):
    """
        HttpHandler acts as the interface to provide the Http
        channel for your bot. 
        It accepts the incoming message as a post request and then sends the 
        response as a Http response
    """
    def __init__(self,config, actions, ozz_guid, redis_db, mongo, log):
        self.redis_db = redis_db
        self.mongo = mongo
        self.log = log
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        if ozz_guid != "":
            if ozz_guid[:4] == 'api_':
                self.api = apiai.ApiAI(ozz_guid[4:])
        print("HTTP endpoint - /api/messages/http")

    def response(self, *args, **kwargs):
        """
          Take the message, parse it and respond
        """
        start = timer()
        payload = request.get_data()
        payload = payload.decode('utf-8')
        data = json.loads(payload)
        message = data["message"]
        if "user_name" in data:
            user_name = data['user_name']
        else:
            user_name = 'User'
        if self.api:
            r = self.api.text_request()
            r.session_id = uuid.uuid4().hex
            r.query = message

            res = r.getresponse()
            res = json.loads(res.read().decode('utf-8'))

            intent = res["result"]["action"]
            if intent == '':
                intent = res["result"]["metadata"]["intentName"]
            response = res["result"]["fulfillment"]["speech"]
            entities = res["result"]['parameters']


            if intent in self.actions:
                if type(self.actions[intent]) == list:
                    response = random.choice(self.actions[intent])
                else:
                    session = {}
                    session['user'] = {
                                'id':request.remote_addr,
                                'name':user_name,
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
                    action = self.actions[intent]
                    response = func(session)
            elif "default_action" in self.actions:
                session = {}
                session['user'] = {
                            'id':request.remote_addr,
                            'name':user_name,
                            'profile_pic':'None',
                            'locale':'en-US',
                            'timezone':'0',
                            'gender':'None'
                        }
                session['intent'] = intent
                session['entities'] = entities
                session['message'] = message
                session['channel'] = 'web'
                func = eval(self.actions["default_action"])
                action = 'None'
                response = func(session)    
            else:
                intent = 'No NLP'
                entities = 'No NLP'
                action = 'No NLP'
                response = {"message":str(message),"type":"text"}
            end = timer()
            runtime = str(end - start)
            log_object = {"message":message,"intent":intent,"entities":entities,"action":action,"response":response,"runtime":runtime,"time":time.time()}
            self.mongo.db.logs.insert_one(log_object)
            return jsonify(response)
            
        else:
            end = timer()
            runtime = str(end - start)
            return str(message)