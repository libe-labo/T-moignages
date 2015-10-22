#!/usr/bin/env python

from __future__ import print_function  # In case we're running with python2

import sys
import json
import argparse
import subprocess
import pyinotify
import requests
import pystache
import tweepy


twitter_api = None


def getTweet(url):
    global twitter_api
    if twitter_api is None:
        with open('.twitter.json', 'r') as f:
            twitter_api = json.loads(f.read())
    api = tweepy.API(tweepy.AppAuthHandler(twitter_api['api_key'], twitter_api['api_secret']))
    return api.get_status(url.split('/')[-1])


def canBuildLess(f):
    try:
        subprocess.Popen(['lessc', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print('Il semblerait qu\'il soit impossible de compiler le style, \
               demande à ce cher Paulloz de le faire pour toi.', file=sys.stderr)
        return lambda: None
    return f


@canBuildLess
def buildLessFiles():
    p = subprocess.Popen(['lessc', 'less/main.less', '--include-path=less/'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode > 0:
        print(stderr.decode('utf-8'), file=sys.stderr)
    else:
        print("Built style.css")
        with open('style.css', mode='w') as f:
            f.write(stdout.decode('utf-8'))


class Sheet():
    def __init__(self, key):
        self.__endpoint = 'https://spreadsheets.google.com'
        self.__key = key

        self.__data = list()

        try:
            path = '/feeds/worksheets/{key}/public/basic?alt=json'.format(
                key=key)
            for entry in self.__requestData(path)['feed']['entry']:
                path = '/feeds/list/{key}/{sheetId}/public/values?alt=json'\
                    .format(key=key,
                            sheetId=entry['link'][len(entry['link']) - 1]
                                         ['href'].split('/').pop())

                self.__setData(self.__formatData([
                    {key[4:]: value['$t']
                        for key, value in entry.items()
                        if key[:4] == 'gsx$'}
                    for entry in self.__requestData(path)['feed']['entry']]))

        except requests.exceptions.RequestException as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    def __requestData(self, path):
        r = requests.get(self.__endpoint + path)
        if r.status_code == 200:
            return r.json()
        raise requests.exceptions.RequestException(
            "Seems we can't find {0}".format(self.__key))

    def __setData(self, data):
        self.__data = data

    def __formatData(self, data):
        def getOrFalse(d, k):
            return len(d[k]) > 0 and dict(value=d[k].encode('utf-8')) or False

        def addNBSPs(s):
            for char in ['?', ':', '!']:
                s = s.replace(' {0}'.format(char), '&nbsp;{0}'.format(char))
            return s

        _data = dict(items=[])
        for d in data:
            if d['type'] in ['titre', 'sous-titre', 'chapo']:
                _data[d['type']] = addNBSPs(d['texteext.']).encode('utf-8')
            elif d['type'] in ['lire-aussi']:
                _data[d['type']] = dict(
                    textext=addNBSPs(d['texteext.']).encode('utf-8'),
                    textint=addNBSPs(d['texteint.']).encode('utf-8')
                )
            elif d['type'] in ['tweet']:
                tweet = getTweet(d['texteext.'])
                _d = dict()
                _d[d['type']] = dict(
                    id=tweet.id,
                    fromname=tweet.author.name,
                    fromscreenname=tweet.author.screen_name,
                    text=tweet.text,
                    date=tweet.created_at.strftime('%d/%m/%Y, %H:%M'),
                    picture=tweet.author.profile_image_url
                )
                _data['items'].append(_d)
            else:
                _d = dict()
                _d[d['type']] = dict(
                    textext=addNBSPs(d['texteext.']).encode('utf-8'),
                    textint=addNBSPs(d['texteint.']).encode('utf-8'),
                    image=addNBSPs(d['image']).encode('utf-8')
                )
                _data['items'].append(_d)
        return _data

    def getData(self):
        return self.__data


def watchFiles():
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY

    class EventHandler(pyinotify.ProcessEvent):
        def __process_change(self, event):
            print("{0} has been modified".format(event.pathname))
            buildLessFiles()

        def process_IN_DELETE(self, event):
            self.__process_change(event)

        def process_IN_CREATE(self, event):
            self.__process_change(event)

        def process_IN_MODIFY(self, event):
            self.__process_change(event)

    notifier = pyinotify.Notifier(wm, EventHandler())
    wm.add_watch('less/', mask, rec=True)

    notifier.loop()


def buildIndex(sheet_id):
    with open('index.html', 'w') as index:
        with open('templates/base.mustache', 'r') as template:
            index.write(pystache.render(template.read(), Sheet(sheet_id).getData()))
    print("Built index.html")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['watch', 'build'], default='build', nargs='?')
    parser.add_argument('sheet-id')
    args = parser.parse_args()

    if args.action == 'watch':
        buildLessFiles()
        buildIndex(vars(args)['sheet-id'])
        watchFiles()
    elif args.action == 'build':
        buildLessFiles()
        buildIndex(vars(args)['sheet-id'])
