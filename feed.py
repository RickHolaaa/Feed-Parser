import feedparser
from datetime import datetime
from time import mktime
import urllib.request as request
import json
import pytz
import time
from dotenv import load_dotenv
import os

load_dotenv()

webhook_url=os.getenv('WEBHOOK_URL')
RSS_URL=os.getenv('RSS_URL')
last_seen_path='date.log'

def parseRSS(rss_url):
    return feedparser.parse(rss_url)

def cleanRSS(rss):
    for items in rss['entries']:
        #print(items.keys())
        print(f"{items['title']}")
        print(f"{items['summary']}")
        print(f"[{items['tags'][0]['term']}]")
        print(f"{items['link']}")
        print(f"{datetime.fromtimestamp(mktime(items['published_parsed']))}")
        print()

def actualize(rss):
    data = rss['entries']
    sorted_data = sorted(data, key=lambda x: x['published_parsed'])
    last = sorted_data[-1]

    try:
        with open(last_seen_path, "r") as f:
            res = f.read().split(";")
            date = res[0]
            tit = res[1]
            if (date == str(last['published_parsed']) or tit ==
                str(last['title'])):
                return
            else:
                with open(last_seen_path, "w") as f:
                    f.write(str(last['published_parsed'])+";"+str(last['title']))
    except FileNotFoundError as e:
        with open(last_seen_path, "w") as f:
            f.write(str(last['published_parsed'])+";"+str(last['title']))

    payload=dict()
    embed=dict()

    embed['title']=last['title']
    embed['description']=last['summary']
    embed['timestamp']=str(pytz.timezone("Europe/Paris").localize(datetime.fromtimestamp(mktime(last['published_parsed'])),is_dst=None))
    embed['authors']=last['credit']
    embed['url']=last['link']
    payload['embeds']=[embed]


    return payload

def sendWebhook(payload):
    if (payload==None):
        return
    headers = {'Content-Type': 'application/json','user-agent':'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
    req = request.Request(url=webhook_url,
                          data=json.dumps(payload).encode('utf-8'),
                          headers=headers,
                          method='POST')
    try:
        response = request.urlopen(req)
        #print(response.status,response.reason,response.headers)
    except TabError as e:
        print(f"Error {e.reason}")

if __name__ == '__main__':
    while (True):
        sendWebhook(actualize(parseRSS(RSS_URL)))
        time.sleep(1)
