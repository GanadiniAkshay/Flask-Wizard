from __future__ import absolute_import
from __future__ import print_function

import os
import json
import apiai
import requests
import base64
import sys
import random
import uuid
import time

from timeit import default_timer as timer

from flask import request
from actions import *

class FacebookHandler(object):
    """
        The facebook handler acts as the interface to handle all requests coming 
        from messenger.

        It parses the payload and responds
    """
    def __init__(self, pid, pat, verify_token, ozz_guid, actions, redis_db, mongo, log):
        self.pid = pid
        self.pat = pat
        self.verify_token = verify_token
        self.ozz_guid = ozz_guid
        self.redis_db = redis_db
        self.mongo = mongo
        self.log = log
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        if ozz_guid != "":
            if ozz_guid[:4] == 'api_':
                self.api = apiai.ApiAI(ozz_guid[4:])
        print("Messenger endpoint - /api/messages/facebook")

    def verify(self,*args,**kwargs):
        if request.args.get('hub.verify_token','') == self.verify_token:
            return request.args.get('hub.challenge','')
        else:
            return "Error, wrong validation token"

    def respond(self,*args,**kwargs):
        payload = request.get_json()
        for sender, message in self.messaging_events(payload):
            if sender != self.pid:
                if type(message) != str:
                    start = timer()
                    intent=None
                    entities=None
                    action=None
                    message = message.decode('utf-8')
                    r = requests.get("https://graph.facebook.com/v2.6/"+ sender + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + self.pat)
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
                    session['cache'] = self.redis_db
                    session['mongo'] = self.mongo
                    session['message'] = message
                    session['channel'] = 'facebook' 
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

                    session['intent'] = intent
                    session['entities'] = entities
                    
                    if intent in self.actions:
                        action = self.actions[intent]
                        if type(self.actions[intent]) == list:
                            response = random.choice(self.actions[intent])
                            self.send_message(self.pat,sender,response)
                        else: 
                            func = eval(self.actions[intent])
                            func(session)
                    elif response != "":
                        end = timer()
                        runtime = str(end - start)
                        if self.mongo:
                            log_object = {"message":message,"channel":"facebook","intent":intent,"entities":entities,"action":action,"response":str(response),"runtime":runtime,"time":str(time.time())}
                            self.mongo.db.logs.insert_one(log_object)
                        self.send_message(self.pat, sender, response)
                else:
                    end = timer()
                    runtime = str(end - start)
                    if self.mongo:
                        log_object = {"message":message,"channel":"facebook","intent":intent,"entities":entities,"action":action,"response":str(message),"runtime":runtime,"time":str(time.time())}
                        self.mongo.db.logs.insert_one(log_object)
                    self.send_message(self.pat, sender, message)

        return "responded"

    def messaging_events(self, payload):
        data = payload
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
                elif "postback" in event and "payload" in event["postback"]:
                    yield event["sender"]["id"], event["postback"]["payload"].encode('unicode_escape')

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