import var
from urllib import urlopen
from contextlib import closing

with closing(urlopen(var.url_target + "/robots.txt")) as stream:
    global robot_parsed
    robot_parsed = stream.read()

