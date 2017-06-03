"Definition for the skype API object"
import requests, json, traceback, sys, time

"Time handling imports"
from datetime import *
from time import *

"OS handling"
import os, re, base64, importlib, string
from sys import version_info

def CreateBasicPayload(ourid, text, sender):
    payload = {
                "type":"message",
                "text":text,
                "from": {
                    "id":ourid,
                    "name":"OzzBotSystem"
                 },
                 "conversation": {
                     "id":sender
                 }
              }
    return payload    

def Send(token, service, sender, ourid, payload):
        url = service + '/v3/conversations/' + sender + '/activities/'
        headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
        payload["locale"] = "en-US"
        r = requests.post(url, data=json.dumps(payload), headers=headers)


def SendTextMessage(token, service, sender, ourid, text):
        Send(token, service, sender, ourid, payload = CreateBasicPayload(ourid, text, sender))


def AddButton(payload, btype, title, value):
    button = {"type":btype, "title":title, "value":value}
    if "attachments" not in payload:
        payload["attachments"] = [
            {
                "contentType": "application/vnd.microsoft.card.hero",
                "content": {
                    "buttons":[]
                }
            }
        ]
    if "buttons" not in payload['attachments'][0]['content']:
        payload['attachments'][0]['content']["buttons"] = []
    print(payload)
    payload['attachments'][0]['content']['buttons'].append(button)
    return

def AddImage(payload, url):
    img = {"url": url}
    if "attachments" not in payload:
        payload["attachments"] = [
            {
                "contentType": "application/vnd.microsoft.card.hero",
                "content": {
                    "images": []
                }
            }
        ]
    if "images" not in payload['attachments'][0]['content']:
        payload['attachments'][0]['content']["images"] = []
    print(payload)
    payload['attachments'][0]['content']['images'].append(img)
    return

def AddCardDetails(payload, title, subtitle, text):
    if "attachments" not in payload:
        payload["attachments"] = [
            {
                "contentType": "application/vnd.microsoft.card.hero",
                "content": {
                    "title": "",
                    "subtitle": "",
                    "text": ""
                }
            }
        ]
    if "title" not in payload['attachments'][0]['content']:
        payload['attachments'][0]['content']["title"] = []
    if "subtitle" not in payload['attachments'][0]['content']:
        payload['attachments'][0]['content']["subtitle"] = []
    if "subtitle" not in payload['attachments'][0]['content']:
        payload['attachments'][0]['content']["buttons"] = []
    payload['attachments'][0]['content']['title'] = title;
    payload['attachments'][0]['content']['subtitle'] = subtitle;
    payload['attachments'][0]['content']['text'] = text;
    return

def AddMedia(payload, imageurl, mediaurl):
    if "attachments" not in payload:
        payload["attachments"] = [
            {
                "contentType": "application/vnd.microsoft.card.video",
                "content": {
                    "image": {
                        "url": ""
                    },
                    "media": [
                        {
                            "url":""
                        }
                    ]
                }
            }
        ]
    if "image" not in payload['attachments'][0]['content']:
        payload['attachments'][0]['content']["image"] = {}
        payload['attachments'][0]['content']["image"]["url"] = ""
        payload['attachments'][0]['content']["media"] = []
        payload['attachments'][0]['content']["media"][0]["url"] = ""
    payload['attachments'][0]['contentType'] = "application/vnd.microsoft.card.video"
    payload['attachments'][0]['content']["image"]["url"] = imageurl
    payload['attachments'][0]['content']["media"][0]["url"] = mediaurl
    return
