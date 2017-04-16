from __future__ import absolute_import
from __future__ import print_function

import json
import requests

from flask import request
from actions import *

from .nlu import NLUParser

class HttpHandler(object):
    """
        HttpHandler acts as the interface to provide the Http
        channel for your bot. 
        It accepts the incoming message as a post request and then sends the 
        response as a Http response
    """
    def __init__(self,model,config, actions):
        with open(actions,"r") as jsonFile:
            self.actions = json.load(jsonFile)
        self.nlu = NLUParser(model,config)

    def response(self, *args, **kwargs):
        """
          Take the message, parse it and respond
        """
        payload = request.get_data()
        data = json.loads(payload)
        intent, entities = self.nlu.parse(data["message"])
        if intent in self.actions:
            func = eval(self.actions[intent])
            response = func()
            return str(response)
        else:
            return ""