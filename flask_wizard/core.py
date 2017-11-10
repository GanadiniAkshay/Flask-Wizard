from __future__ import absolute_import
from __future__ import print_function

import json
import requests
import os
import redis

from flask_pymongo import PyMongo

from .facebook import FacebookHandler
from .web import HttpHandler
from .slack import SlackHandler
from .telegram import TelegramHandler

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
            self.redis_db = ""
            self.mongo = ""
            data = json.load(jsonFile)
            if "active_model" in data.keys():
                print("Using the data model at " + data["active_model"])
                self.model = data["active_model"]
            else:
                self.model = ""

            if "redis" in data.keys():
                if data['redis']['host'] and data['redis']['host'] != "":
                    host = data['redis']['host']
                    if data['redis']['port'] and data['redis']['port'] != "":
                        port = data['redis']['port']
                    else:
                        port = 6379
                    
                    if data['redis']['password']:
                        password = data['redis']['password']
                    else:
                        password = ""

                    self.redis_db = redis.StrictRedis(host=host,port=int(port),password=password)
            
            if "mongo" in data.keys():
                if data['mongo']['mongo_uri'] and data['mongo']['mongo_uri'] != "":
                    app.config['MONGO_URI'] = data['mongo']['mongo_uri']
                    self.mongo = PyMongo(app)
            if "ozz_guid" in data.keys():
                self.ozz_guid = data['ozz_guid']
            else:
                self.ozz_guid = ""
            self.channels = data["channels"].keys()
            if "facebook" in self.channels:
                self.facebook = True
                self.facebook_verify_token = data["channels"]["facebook"]["verify_token"]
                self.facebook_pat = data["channels"]["facebook"]["pat"]
                self.facebook_pid = data["channels"]["facebook"]["pid"]
            if "slack" in self.channels:
                self.slack = True
                self.slack_pid = data["channels"]["slack"]["cid"]
                self.slack_pad = data["channels"]["slack"]["cs"]
                self.slack_verify_token = data["channels"]["slack"]["verify_token"]
                self.slack_bot_token = data["channels"]["slack"]["bot_token"]
            if "telegram" in self.channels:
                self.telegram = True
                self.token = data["channels"]["telegram"]["bot_token"]

        # web initializaion
        web = HttpHandler(self.model, self.config, self.actions, self.ozz_guid, self.redis_db, self.mongo)
        app.add_url_rule('/api/messages/http',view_func=web.response,methods=["POST"])

        #facebook initialization
        if "facebook" in self.channels:
            self.verify_token = self.facebook_verify_token
            self.pat = self.facebook_pat
            self.pid = self.facebook_pid
            fb = FacebookHandler(self.pid, self.pat, self.verify_token, self.ozz_guid, self.actions, self.redis_db, self.mongo)
            app.add_url_rule('/api/messages/facebook',view_func=fb.verify
            ,methods=['GET'])
            app.add_url_rule('/api/messages/facebook',view_func=fb.respond
            ,methods=['POST'])
        if "slack" in self.channels:
            self.pid = self.slack_pid
            self.pad = self.slack_pad
            self.verify_token = self.slack_verify_token
            self.bot_token = self.slack_bot_token
            slack  = SlackHandler(self.pid,self.pad,self.verify_token,self.bot_token,self.ozz_guid,self.actions, self.redis_db, self.mongo)
            #app.add_url_rule('/api/messages/slack',view_func=slack.verify,methods=['GET'])
            app.add_url_rule('/api/messages/slack',view_func=slack.respond,methods=['POST'])
        
        if "telegram" in self.channels:
            self.bot_token = self.token
            telegram  = TelegramHandler(self.bot_token,self.ozz_guid,self.actions,self.redis_db, self.mongo)
            app.add_url_rule('/api/messages/telegram',view_func=telegram.responds,methods = ['POST'])
    