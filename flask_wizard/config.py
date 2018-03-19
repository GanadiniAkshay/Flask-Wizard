from __future__ import absolute_import
from __future__ import print_function

import json
import requests
import random
import apiai
import sys
import uuid

from flask import request,jsonify, render_template

class ConfigHandler(object):
    def __init__(self, route):
        self.route = route
        print("Config page setup at - " + route)

    def render(self):
        return render_template('index.html')