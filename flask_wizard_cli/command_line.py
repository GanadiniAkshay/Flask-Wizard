from __future__ import absolute_import
from __future__ import print_function

import os
import json
import sys
import urllib
import tarfile
import wget
import shutil
import getpass
import requests
import time
import jwt

from subprocess import call


def main():
    arguments = sys.argv
    if len(arguments) < 2:
        show_hint(arguments)
    else:
        method = arguments[1]
        if method == "build":
            build(arguments)
        elif method == 'init':
            init(arguments)
        elif method == 'hint':
            show_hint(arguments)
        elif method == 'run':
            run(arguments)
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

def init(arguments):
    #Setup bot name
    main_name = os.getcwd().split(os.sep)[-1]
    if len(arguments) < 3:
        prompt = "Name of the bot (default: " + main_name + "):"
        bot_name = str(input(prompt))
        if len(bot_name) == 0:
            bot_name = main_name
    else:
        bot_name = ' '.join(arguments[2:])

    #Setup Author Name
    prompt = "Name of the author:"
    user_name = str(input(prompt))
    if len(user_name) == 0:
        user_name = "wizard_user"

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

    #Setup actions.json file
    print("Creating actions.json...")
    file_path = os.path.join(os.getcwd(),'actions.json')
    with open(file_path, "w") as jsonFile:
        data = {}
        json.dump(data,jsonFile,indent=2)

    #Setup main.py file
    print("Creating application.py...")
    file_path = os.path.join(os.getcwd(),'application.py')
    with open(file_path, "w") as mainFile:
        mainFile.write("from flask import Flask\n")
        mainFile.write("from flask_wizard import Wizard\n")
        mainFile.write("\n")
        mainFile.write("application = Flask(__name__)\n")
        mainFile.write("wizard = Wizard(application)\n")
        mainFile.write("\n")
        mainFile.write("if __name__ == '__main__':\n")
        mainFile.write("\tapplication.run()")

    #Setup config.json file
    print("Creating config.json....")
    file_path = os.path.join(os.getcwd(),'config.json')
    with open(file_path, "w") as jsonFile:
        data = {}
        data["name"] = bot_name
        data["channels"] = {}
        data["ozz_guid"] = ""
        data["redis"] = {"host":"","port":"","password":""}
        data["mongo"] = {"mongo_uri":""}
        json.dump(data, jsonFile, indent=2)

def run(arguments):
    main_path = os.path.join(os.getcwd(),'application.py')
    if os.name == 'nt':
        #windows operating system
        call(["python","application.py"])
    else:
        #linux, unix, macos operating system
        if sys.version_info >= (3,0):
            call(["python3","application.py"])
        else:
            call(["python","application.py"])


def show_hint(arguments):
    print("Please provide the right option or command you want to run")
    print("Accepted commands: ")
    print("-------------------------------------------")
    print("wiz hint #to see list of commands")
    print("wiz train #to train the nlp model")
    print("wiz create <bot name> #to create a new bot")

