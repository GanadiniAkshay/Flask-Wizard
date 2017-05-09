from __future__ import absolute_import
from __future__ import print_function

import json
import requests
import os

from .facebook import FacebookHandler
from .web import HttpHandler


class Wizard(object):
    """
        The wizard object is the central interface for interacting with the bot.

        It sets up the model to be used for NLP. It sets us the different webhooks for different channels and
        calls a function from the channels object to process it.
    """
    def __init__(self, app=None):
        self.app = app
        self.config = os.path.join(os.getcwd(),'config.json')
        self.actions = os.path.join(os.getcwd(),'actions.json')

        path = os.path.join(os.getcwd(),'actions')
        files = os.listdir(path)
        imps = []

        for i in range(len(files)):
            name = files[i].split('.')
            if len(name) > 1:
                if name[1] == 'py' and name[0] != '__init__':
                    name = name[0]
                    imps.append(name)
        init_path = os.path.join(path,'__init__.py')
        file = open(init_path,'w')
        toWrite = '__all__ = ' + str(imps)

        file.write(toWrite)
        file.close()

        if app is not None:
            self.init_app(app)

    def init_app(self,app):
        ''' Initializes the application with the extension.

        :param app: The Flask application object.
        '''
        with open(self.config,"r") as jsonFile:
            data = json.load(jsonFile)
            if "active_model" in data.keys():
                print("Using data model " + data["active_model"])
                self.model = data["active_model"]
            else:
                self.model = ""
            self.channels = data["channels"].keys()
            if "facebook" in self.channels:
                self.facebook = True
                self.facebook_verify_token = data["channels"]["facebook"]["verify_token"]
                self.facebook_pat = data["channels"]["facebook"]["pat"]
                self.facebook_pid = data["channels"]["facebook"]["pid"]

        # web initializaion
        web = HttpHandler(self.model, self.config, self.actions)
        app.add_url_rule('/api/messages/http',view_func=web.response,methods=["POST"])

        #facebook initialization
        if "facebook" in self.channels:
            self.verify_token = self.facebook_verify_token
            self.pat = self.facebook_pat
            self.pid = self.facebook_pid
            fb = FacebookHandler(self.pid, self.pat, self.verify_token, self.model, self.config, self.actions)
            app.add_url_rule('/api/messages/facebook',view_func=fb.verify
            ,methods=['GET'])
            app.add_url_rule('/api/messages/facebook',view_func=fb.respond
            ,methods=['POST'])