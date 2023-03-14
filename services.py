import json
import requests

REV_KEY = "f89b79f27498db5318b92735944f75cff59904fe"
REV_URL = "https://revapi.reverieinc.com/"


def lang_detect(text: str):
    payload = json.dumps({"text": text})
    headers = {
        "Content-Type": "application/json",
        "Postman-Token": "60e488ea-1077-41f5-b47f-ad0e157a4705",
        "REV-API-KEY": REV_KEY,
        "REV-APP-ID": "com.ashis",
        "REV-APPNAME": "lang_id_text",
        "cache-control": "no-cache",
    }

    response = requests.request("POST", REV_URL, headers=headers, data=payload)
    return json.loads(response.text)['lang']


def sentiment_detect(text):
    payload = json.dumps({
    "data": text,
    "mode": "ne"
    })
    headers = {
    'Content-Type': 'application/json',
    'REV-API-KEY': '5e617b4bd897b44f5af9960b418c9e825ea25b51',
    'REV-APP-ID': 'com.revnlu',
    'REV-APPNAME': 'sentiment',
    'src_lang': 'hi-rom'
    }

    response = requests.request("POST", REV_URL, headers=headers, data=payload)

    return json.loads(response.text)['sentiments']