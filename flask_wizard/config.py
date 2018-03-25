from __future__ import absolute_import
from __future__ import print_function

import json
import requests
import random
import apiai
import sys
import uuid
import os

from flask import request,jsonify, render_template

class ConfigHandler(object):
    def __init__(self, route):
        self.route = route
        print("Config page setup at - " + route)

    def render(self):
        """
            Render the configuration UI
        """
        return render_template('_do_not_modify_config.html')

    def modconfig(self,*args,**kwargs):
        if request.method == 'GET':
            config = os.path.join(os.getcwd(),'config.json')
            with open(config,"r") as jsonFile:
                 data = json.load(jsonFile)
            return jsonify(data)
        else:
            payload = request.get_json()
            config = os.path.join(os.getcwd(),'config.json')
            with open(config,"w") as jsonFile:
                json.dump(payload, jsonFile, indent=2)
            return jsonify(payload)
