from __future__ import absolute_import
from __future__ import print_function

import os
import json
import requests


class OzzParser(object):
    def __init__(self, ozz_guid):
        self.ozz_guid = ozz_guid

    def parse(self, message):
        url = "https://ozz.ai/api/parse/" + self.ozz_guid
        querystring = {"q":message}
        headers = {
                    'cache-control': "no-cache"
                  }
        response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
        data = json.loads(response.text)
        return (data['intent'],data['entities'],data['response'])