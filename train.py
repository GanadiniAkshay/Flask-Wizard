from __future__ import absolute_import
from __future__ import print_function

import os
import json
import sys
import urllib
import tarfile
import wget
import shutil

from subprocess import call

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

def learn(arguments):
    path = os.path.join(os.getcwd(), 'train')
    if (os.path.isdir(path)):
        ac_path = os.path.join(os.getcwd(),'actions')
        files = os.listdir(ac_path)
        imps = []

        for i in range(len(files)):
            name = files[i].split('.')
            if len(name) > 1:
                if name[1] == 'py' and name[0] != '__init__':
                    name = name[0]
                    imps.append(name)
        init_path = os.path.join(ac_path,'__init__.py')
        file = open(init_path,'w')
        toWrite = '__all__ = ' + str(imps)

        file.write(toWrite)
        file.close()

        files = os.listdir(path)

        
        common_examples = []

        none_example_1 = {'text':'jshfjdhsfj','intent':'None','entities':[]}
        none_example_2 = {'text':'dfjkhjkfds','intent':'None','entities':[]}
        common_examples.append(none_example_1)
        common_examples.append(none_example_2)

        
        for file in files:
            file_data = file.split('.')
            intent_name = file_data[0]
            file_type = file_data[1]
            if file_type != 'txt':
                continue
            else:
                with open(path + '/' + file,'r') as intentFile:
                    responses = []
                    examples = intentFile.readlines()
                    examples = [*map(lambda s: s.strip(), examples)]
                    if "<-responses->" in examples:
                        pos = examples.index("<-responses->")
                        responses = examples[pos+1:]
                        examples = examples[:pos]
                    for sample in examples:
                        example = {}
                        sample_split = sample.split('<=>')
                        sample_text = sample_split[0]

                        if len(sample_split) == 1:
                            example['text'] = sample
                            example['intent'] = intent_name
                            example['entities'] = []
                        else:
                            #get list of entities in the sample
                            sample_entities = sample_split[1:]

                            #check if paranthesis match
                            open_paran_count = sample_text.count('(')
                            close_paran_count = sample_text.count(')')

                            if open_paran_count != close_paran_count:
                                raise ValueError("Paranthesis don't match for " + sample_text)
                                

                            #check if paranthesis and provided entites match
                            if open_paran_count != len(sample_entities):
                                raise ValueError("The entities provided and words marked in entities don't match for " + sample_text)
                                
                            
                            start_pos = 0
                            entities_count = 0
                            no_of_entities = len(sample_entities)
                            entities = []

                            while entities_count < no_of_entities:
                                start_pos = sample_text.find('(', start_pos, len(sample_text)) + 1
                                end_pos   = sample_text.find(')', start_pos, len(sample_text))
                                
                                entityLabel = {}

                                entityLabel['start'] = start_pos - 1
                                entityLabel['end'] = end_pos - 1
                                entityLabel['value'] = sample_text[start_pos:end_pos]
                                entityLabel['entity'] = sample_entities[entities_count].strip()
                                
                                entities.append(entityLabel)
                                entities_count += 1

                            example['text'] = sample_text.replace('(','').replace(')','')
                            example['intent'] = intent_name
                            example['entities'] = entities

                        common_examples.append(example)
                    if len(responses) > 0:
                           with open(os.path.join(os.getcwd(),"actions.json"),"r+") as jsonFile:
                               data = json.load(jsonFile)
                               data[intent_name] = responses
                               jsonFile.seek(0)
                               jsonFile.truncate()
                               json.dump(data, jsonFile)
        
        nlp_json = {"rasa_nlu_data":{"common_examples":common_examples}}

        with open(os.path.join(path, 'train.json'),"w") as trainFile:
            json.dump(nlp_json, trainFile)

        with open(os.path.join(os.getcwd(), 'config.json'),"r") as jsonFile:
            data = json.load(jsonFile)

        jsonFile.close()

        training_data = load_data(os.path.join(path, 'train.json'))
        trainer = Trainer(RasaNLUConfig(os.path.join(os.getcwd(), 'config.json')))
        trainer.train(training_data)
        model_directory = trainer.persist('models')

        print(model_directory)
        data["active_model"] = str(model_directory)

        with open(os.path.join(os.getcwd(), 'config.json'),"w") as jsonFile:
            json.dump(data, jsonFile)
    else:
        raise FileNotFoundError("No train folder found. Please setup a wizard bot first by running wiz create <bot_name>")


learn("")



