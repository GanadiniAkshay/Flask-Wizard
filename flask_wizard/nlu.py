from __future__ import absolute_import
from __future__ import print_function

import os
import json

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter

class NLUParser(object):
    def __init__(self, model, config):
        self.model = model
        self.metadata = Metadata.load(self.model)
        self.config = config
        self.interpreter = Interpreter.load(self.metadata, RasaNLUConfig(config))

    def parse(self, message):
        parsed_data = self.interpreter.parse(message)
        #print(parsed_data)
        if parsed_data['intent']['confidence'] < 0.30:
            intent = 'None'
        else:
            intent = parsed_data['intent']['name']
        entities = parsed_data['entities']
        print(intent,entities)
        return intent,entities
    