# inpired from bobrov script
# http://offsecbyautomation.com/Open-Redirection-Bobrov/

import os.path
import sys
import argparse
import requests
from termcolor import colored

parser = argparse.ArgumentParser()
parser.add_argument("-d","--domain",help="domains file or single domain")
parser.add_argument("-p","--payload",help="payloads file or single payload")
parser.add_argument("-s","--nossl",help="disable ssl", action="store_true")
parser.parse_args()
args = parser.parse_args()

if args.nossl:
    ssl = ''
else:
    ssl = 's'

if args.domain:
    f_domain = args.domain
    if os.path.isfile(f_domain):
        f = open( f_domain, 'r')
        t_domain = f.readlines()
        f.close()
    else:
        t_domain = [f_domain]
else:
    parser.print_help()
    sys.exit(2)

if args.payload:
    f_payload = args.payload
    if os.path.isfile(f_payload):
        f = open( f_payload, 'r')
        t_payload = f.readlines()
        f.close()
    else:
        t_payload = [f_payload]
else:
    t_payload = ["//www.google.com/%2e%2e"]

for domain in t_domain:
    domain = domain.strip()
    for payload in t_payload:
        url = 'http' + ssl + '://' + domain + payload
        #sys.stdout.write( domain )
        sys.stdout.write(url)
        try:
            r = requests.get( url, allow_redirects=False, timeout=10 )
        except requests.exceptions.RequestException as e:
            #print e
            sys.stdout.write( "\n" )
            continue
        if "Location" in r.headers and r.headers["Location"] == payload:
            sys.stdout.write( colored(" VULNERABLE!","red") )
        sys.stdout.write( "\n" )
