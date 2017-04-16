import json
import os

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

with open("config.json","r") as jsonFile:
    data = json.load(jsonFile)

jsonFile.close()

training_data = load_data('./train/train.json', 'en')
trainer = Trainer(RasaNLUConfig("config.json"))
trainer.train(training_data)
model_directory = trainer.persist('./models/')

data["active_model"] = str(model_directory)

with open("config.json","w") as jsonFile:
    json.dump(data, jsonFile)
