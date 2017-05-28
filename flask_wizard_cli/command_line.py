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

def main():
    arguments = sys.argv
    if len(arguments) < 2:
        show_hint(arguments)
    else:
        method = arguments[1]
        if method == 'train':
            learn(arguments)
        elif method == 'init':
            init(arguments)
        elif method == 'hint':
            show_hint(arguments)
        elif method == 'run':
            run(arguments)
        elif method == 'build':
            build(arguments)
        elif method == "download":
            download(arguments)
        else:
            show_hint(arguments)

def build(arguments):
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

def init(arguments):
    #Setup bot name
    main_name = os.getcwd().split(os.sep)[-1]
    if len(arguments) < 3:
        prompt = "What is the name of the bot? (default: " + main_name + "):"
        bot_name = str(input(prompt))
        if len(bot_name) == 0:
            bot_name = main_name
    else:
        bot_name = ' '.join(arguments[2:])
    print("Creating bot: " + bot_name)

    #Setup actions folder
    print("Creating actions folder....")
    directory = os.path.join(os.getcwd(),'actions')
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Configure actions folder
    print("Configuring actions folder....")
    directory = os.path.join(os.getcwd(),'actions')
    with open(os.path.join(directory,'__init__.py'), "w") as initFile:
        initFile.write("#It will be initialized at runtime")

    #Setup train folder
    print("Creating train folder....")
    directory = os.path.join(os.getcwd(),'train')
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Setup config.json file
    print("Creating config.json...")
    file_path = os.path.join(os.getcwd(),'config.json')
    with open(file_path, "w") as jsonFile:
        data = {}
        data["name"] = bot_name
        data["pipeline"] = "mitie_sklearn"
        data["mitie_file"] = "./train/total_word_feature_extractor.dat"
        data["channels"] = {}
        json.dump(data, jsonFile)

    #Setup actions.json file
    print("Creating actions.json...")
    file_path = os.path.join(os.getcwd(),'actions.json')
    with open(file_path, "w") as jsonFile:
        data = {}
        json.dump(data,jsonFile)

    #Setup main.py file
    print("Creating main.py...")
    file_path = os.path.join(os.getcwd(),'main.py')
    with open(file_path, "w") as mainFile:
        mainFile.write("from flask import Flask\n")
        mainFile.write("from flask_wizard import Wizard\n")
        mainFile.write("\n")
        mainFile.write("app = Flask(__name__)\n")
        mainFile.write("wizard = Wizard(app)\n")
        mainFile.write("\n")
        mainFile.write("if __name__ == '__main__':\n")
        mainFile.write("\tapp.run()")

    #Download mitie file
    print("Setting up Mitie model file...")
    print("Installing Mitie")

    if os.name == 'nt':
        #windows operating system
        call(["pip","install","git+https://github.com/mit-nlp/MITIE.git#egg=mitie"])
    else:
        #linux, unix or macos
        if sys.version_info >= (3,0):
            call(["pip3","install","git+https://github.com/mit-nlp/MITIE.git#egg=mitie"])
        else:
            call(["pip","install","git+https://github.com/mit-nlp/MITIE.git#egg=mitie"])
    print("Choose one of the options below")
    print("1. Download Mitie models (size>400MB, so if you already have the total_word_feature_extractor.dat file use it. You can find it in the train folder if you already set up wiz before")
    print("2. Copy from existing path")
    choice = str(input("Choice (1 default): "))
    if len(choice)==0 or choice == "1":
        directory_path = os.path.join(os.getcwd(),'train')
        file_path = os.path.join(directory_path,'mitie.tar.bz2')
        wget.download("https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2",'mitie.tar.bz2')

        #Extracting mitie file
        print("")
        print("Extracting Mitie model (this might take a couple of minutes)")
        tar = tarfile.open('mitie.tar.bz2',"r:bz2")
        tar.extractall()
        tar.close()

        #Move files around and only keep total_word_feature_extractor.dat
        current_path = os.path.join(os.getcwd(),'MITIE-models','english','total_word_feature_extractor.dat')
        new_path = os.path.join(os.getcwd(),'train','total_word_feature_extractor.dat')
        os.rename(current_path, new_path)
        os.remove('mitie.tar.bz2')
        shutil.rmtree(os.path.join(os.getcwd(), 'MITIE-models'))
    else:
        path = str(input("Enter path of existing total_word_feature_extractor.dat file: "))
        if path[0] == '~':
            home = os.path.expanduser('~')
            path = path.replace('~',home)
        if os.path.exists(path):
            shutil.copyfile(path,os.path.join(os.getcwd(),'train','total_word_feature_extractor.dat'))
    
    #Download en model for spacy
    print("Setting up spacy")
    if os.name == 'nt':
        #windows operating system
        call(["python","-m","spacy","download","en"])
    else:
        #linux, unix, macos
        if sys.version_info >= (3,0):
            call(["python3","-m","spacy","download","en"])
        else:
            call(["python","-m","spacy","download","en"])

def run(arguments):
    main_path = os.path.join(os.getcwd(),'main.py')
    if os.name == 'nt':
        #windows operating system
        call(["python","main.py"])
    else:
        #linux, unix, macos operating system
        if sys.version_info >= (3,0):
            call(["python3","main.py"])
        else:
            call(["python","main.py"])

def download(arguments):
    directory_path = os.path.join(os.getcwd(),'train')
    file_path = os.path.join(directory_path,'mitie.tar.bz2')
    wget.download("https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2",'mitie.tar.bz2')

    #Extracting mitie file
    print("")
    print("Extracting Mitie model (this might take a couple of minutes)")
    tar = tarfile.open('mitie.tar.bz2',"r:bz2")
    tar.extractall()
    tar.close()

    #Move files around and only keep total_word_feature_extractor.dat
    current_path = os.path.join(os.getcwd(),'MITIE-models','english','total_word_feature_extractor.dat')
    new_path = os.path.join(os.getcwd(),'train','total_word_feature_extractor.dat')
    os.rename(current_path, new_path)
    os.remove('mitie.tar.bz2')
    shutil.rmtree(os.path.join(os.getcwd(), 'MITIE-models'))

def show_hint(arguments):
    print("Please provide the right option or command you want to run")
    print("Accepted commands: ")
    print("-------------------------------------------")
    print("wiz hint #to see list of commands")
    print("wiz train #to train the nlp model")
    print("wiz create <bot name> #to create a new bot")
