import requests, json, pymongo, var
from http_dict import http_status_dict
from pymongo import MongoClient
from url_parser import *

#-----Open connection with the target URL (specified in var module)-----#
req = requests.get(var.url_target)

#-----Get the HTTP status code from the target URL-----#
def get_http_status():
    global req_stat
    req_stat = req.status_code
get_http_status()

#-----Get the headers from the target URL-----#          
def get_host_headers():
    global headers
    headers = req.headers
    print json.dumps(dict(headers))
    print "\n"
get_host_headers()

#-----Describe status code by getting description from http_dict module-----#
http_status = http_status_dict[str(req_stat)]

#------Generation of URL list from parsers-------#
html_source_list = []
for url in html_source.anchorlist:
    html_source_list.append(url)

#------Writing results in the text file-------#
output_txt = open("UpGarde-Result.txt", "w")
output_txt.write("UpGarde test results as follows" + "\n" + "\n")
output_txt.write("---Target host:--- " + var.url_target + "\n" + "\n")
output_txt.write("--HTTP status:--" + "\n")
output_txt.write(http_status + "\n" + "\n")
output_txt.write("--URL structure:--" + "\n")
output_txt.write("\n".join(str(url) for url in html_source_list))
output_txt.close()




"""
client1 = MongoClient()
db = client1.test_database1

post = dict(headers)

posts = db.posts
post_id = posts.insert(post)
"""



