#!/usr/bin/python3.5

# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import socket
import argparse
from colored import fg, bg, attr
from threading import Thread
from queue import Queue
from multiprocessing.dummy import Pool


parser = argparse.ArgumentParser()
parser.add_argument( "-o","--host",help="set hosts file list" )
parser.add_argument( "-t","--threads",help="threads, default 10" )
parser.parse_args()
args = parser.parse_args()

if args.threads:
    _threads = int(args.threads)
else:
    _threads = 10

t_hosts = []
if args.host:
    if os.path.isfile(args.host):
        fp = open( args.host, 'r' )
        t_hosts = fp.read().split("\n")
        fp.close()

n_host = len(t_hosts)

if not n_host:
    parser.error( 'hosts list missing' )

sys.stdout.write( '%s[+] %d hosts found: %s%s\n' % (fg('green'),n_host,args.host,attr(0)) )

def resolve( host ):
    if t_multiproc['n_current']%5000 == 0:
        save()
    
    sys.stdout.write( 'progress: %d/%d\r' %  (t_multiproc['n_current'],t_multiproc['n_total']) )
    t_multiproc['n_current'] = t_multiproc['n_current'] + 1

    try:
        ip = socket.gethostbyname( host )
        t_alive[host] = ip
        # print(ip)
    except Exception as e:
        t_dead.append( host )
        # sys.stdout.write( "%s[-] error occurred: %s (%s)%s\n" % (fg('red'),e,host,attr(0)) )

t_alive = {}
t_dead = []

t_multiproc = {
    'n_current': 0,
    'n_total': n_host
}

# pool = Pool( _threads )
# pool.map( resolve, t_hosts )
# pool.close()
# pool.join()

def save():
    fp = open( 'h_alive', 'w' )
    for h in sorted(t_alive.keys()):
        fp.write( "%s:%s\n" % (h,t_alive[h]) )
    fp.close()

    fp = open( 'h_dead', 'w' )
    for h in t_dead:
        fp.write( "%s\n" % h )
    fp.close()


def doWork():
    while True:
        host = q.get()
        resolve( host )
        q.task_done()


q = Queue( _threads*2 )

for i in range(_threads):
    t = Thread( target=doWork )
    t.daemon = True
    t.start()

try:
    for host in t_hosts:
        q.put( host )
    q.join()
except KeyboardInterrupt:
    sys.exit(1)


# print( t_alive)
# print( t_dead)
sys.stdout.write( '%s[+] %d hosts alive, %d dead hosts%s\n' % (fg('green'),len(t_alive),len(t_dead),attr(0)) )

save()


exit()
