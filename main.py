import requests
import json
import threading
from http_dict import http_status_dict
import pymongo
from pymongo import MongoClient
from url_parser import *

global req
req = requests.get('https://www.python.org/')

def get_http_status():
    #threading.Timer(20, get_http_status).start()
    global req_stat
    req_stat = req.status_code
          
def get_host_headers():
    #threading.Timer(30, get_host_headers).start()
    global headers
    headers = req.headers
    print json.dumps(dict(headers))
    print "\n"

get_http_status()
get_host_headers()

print http_status_dict[str(req_stat)]
print html_source

"""
client1 = MongoClient()
db = client1.test_database1

post = dict(headers)

posts = db.posts
post_id = posts.insert(post)
"""



