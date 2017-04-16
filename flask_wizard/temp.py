from __future__ import absolute_import
from __future__ import print_function

import json
import requests
import os

import parser

from flask import request

class Wizard(object):
    def __init__(self, app=None):
        self.app = app
        self.config = os.path.join(os.getcwd(),'config.json')
        if app is not None:
            self.init_app(app)

    def init_app(self,app):
        ''' Initializes the application with the extension.

        :param app: The Flask application object.
        '''
        self.verify_token = app.config.get('VERIFY_TOKEN')
        self.pat = app.config.get('PAT')
        app.add_url_rule('/api/messages',view_func=self._verify
        ,methods=['GET'])
        app.add_url_rule('/api/messages',view_func=self._respond
        ,methods=['POST'])

        with open(self.config,"r") as jsonFile:
            data = json.load(jsonFile)
            self.model = os.path.join(os.getcwd(),data["active_model"]).replace('./','')
            print(self.model)

    def _verify(self,*args,**kwargs):
        if request.args.get('hub.verify_token','') == self.verify_token:
            return request.args.get('hub.challenge','')
        else:
            return "Error, wrong validation token"
    
    def _respond(self,*args,**kwargs):
        payload = request.get_data()
        print(payload)
        for sender, message in self._messaging_events(payload):
            print("Incoming from %s: %s" % (sender, message))
            self._send_message(self.pat,sender,message)
        return "responded"

    def _messaging_events(self, payload):
        data = json.loads(payload)
        messaging_events = data["entry"][0]["messaging"]
        for event in messaging_events:
            if "message" in event and "text" in event["message"]:
                yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
            else:
                yield event["sender"]["id"], "I can't echo this"

    def _send_message(self, token, recipient, text):
        """Send the message text to recipient with id recipient.
        """
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": token},
            data=json.dumps({
            "recipient": {"id": recipient},
            "message": {"text": text.decode('unicode_escape')}
            }),
            headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print(r.text)
