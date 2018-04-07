from flask_wizard import response
from urllib.parse import quote

import json
import math
import operator
import os

def link_account(session):
    config_path = os.path.join(os.getcwd(),'config.json')
    with open(config_path,"r") as jsonFile:
        config = json.load(jsonFile)
        frontend = config["frontend"]
    url = frontend + "/login?uid="+ str(session['user']['id'])
    course_obj = [response.template_element(
                                                title="Login",
                                                action=response.actions(type="web_url",url=url),
                                                buttons=[response.button(type="web_url",url=url,title="Authenticate")]
                                            )]
    response.send(session,"linking it up")
    template = response.template(type="generic",elements=course_obj)
    response.send(session,template)