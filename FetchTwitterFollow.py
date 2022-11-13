#!/usr/bin/python3

# WolfwithSword 2022


import sys
import twitter
import argparse, configparser
import time, datetime
import traceback
import unicodecsv as csv

import requests
import re


SLEEP_ON_ERROR_MINS=5


def toStr(key, val, urlExpand):
    if val is None:
        return 'null'
    if isinstance(val, bool) or isinstance(val, int):
        return str(val)
    if urlExpand and str(val).startswith('https://t.co/'):
        regex = r"(?i)\b((?:https?://t.co/.+))"
        url = re.findall(regex,str(val))
        return get_original_twitter_url(url, str(val))
    if "color" in key:
        return "#" + str(val)
    return val


def get_original_twitter_url(twitter_urls, val):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    for twitter_url in twitter_urls:
        r = requests.get(url = twitter_url,headers=headers)
        data = r.text
        url = re.search("(?P<url>https?://[^\s]+)\"", data).group("url")
        val = val.replace(twitter_url, url)
    return val


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-auth', '--authfile', help="config file for API auth")
    parser.add_argument('-u', '--user', help="Username to fetch from. No @ symbol.")
    parser.add_argument('-m', '--mode', choices=['following', 'followers'],
                        help="Which mode to fetch. [followers, following] Default: following")
    parser.add_argument('--urlexpand', action='store_true',
                        help = 'If included, expand https://t.co/ url to full url from user website link. Warning - this makes this tool MUCH slower.')
    parser.set_defaults(mode='following', authfile='./auth.ini', urlexpand=False)
    args = parser.parse_args()
    
    authPath = args.authfile
    username = args.user
    mode = args.mode
    urlExpand = args.urlexpand;
    
    if mode not in ['following', 'followers']:
        print("Invalid mode set. Cannot continue.")
        return
    
    if username is None:
        print("Must have a username.")
        return

    if authPath is None:
        print("No auth file found")
        return

    print("Fetching [%s] from user: %s" % (mode, username))
    
    config = configparser.ConfigParser()
    config.read(authPath)
    
    api_key = config['Twitter']['api_key']
    api_key_secret = config['Twitter']['api_key_secret']
    access_token = config['Twitter']['access_token']
    access_token_secret = config['Twitter']['access_token_secret']

    if None in [api_key, api_key_secret, access_token, access_token_secret] or\
            "" in [api_key, api_key_secret, access_token, access_token_secret]:
        print("Auth values not set. Please configure and try again")
        return

    try:
        api = twitter.Api(consumer_key=api_key, consumer_secret=api_key_secret,
                          access_token_key=access_token, access_token_secret=access_token_secret,
                          sleep_on_rate_limit=True, input_encoding=None)
    except:
        print("Could not connect or authenticate to Twitter API")
        return

    if api is None:
        print("Could not connect to Twitter API")
        return
    
    print("Connected to Twitter API and Authorized")
    
    csv_filename = "%s-%s-%s.csv" % (username, mode, datetime.datetime.now().strftime("%Y%m%d"))
    nextCursor = -1
    
    fieldNames = None
    try:
        with open("USER_FIELDS") as fieldsFile:
            fieldNames = [field.strip(' \n') for field in fieldsFile.readlines()]
    except:
        print("Could not read USER_FIELDS file.")
        return
    
    with open(csv_filename, 'wb') as csvFile:
        startTime = time.time()
        csvFile.write(u'\ufeff'.encode('utf8'))

        writer = csv.DictWriter(csvFile, fieldNames, encoding='utf-8', delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writeheader()

        numInCollection = 0;
        while nextCursor != 0:
            try:
                collection = None
                if mode == 'followers':
                    nextCursor, prevCursor, collection = api.GetFollowersPaged(screen_name=username, cursor=nextCursor)
                elif mode == 'following':
                    nextCursor, prevCursor, collection = api.GetFriendsPaged(screen_name=username, cursor=nextCursor)
            except:
                print("Error obtaining next page of %s (w/ nextCursor=%d). Waiting for 5m before retrying \n" % (
                      mode, nextCursor))
                traceback.print_exc(file=sys.stderr)
                time.sleep(SLEEP_ON_ERROR_MINS * 60)    
            else:
                for u in collection:
                    row = {fld: toStr(fld, getattr(u,fld), urlExpand) for fld in fieldNames}
                    writer.writerow(row)
                    numInCollection += 1
                    print("Progress: %d users" % numInCollection, end="\r")
            endTime = time.time()
        print("\n")
        print("%d %s of %s dumped to %s in %f seconds" % (numInCollection, mode, username, csv_filename, endTime - startTime))
        
if __name__=="__main__":
    main()
