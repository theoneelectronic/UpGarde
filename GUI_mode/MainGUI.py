# -*- coding: utf-8 -*-
import Tkinter as tk
import urllib2, json, htmllib, formatter, urllib2
from http_dict import http_status_dict
from urllib2 import urlopen
from contextlib import closing

class Application(tk.Frame): 
    def __init__(self, master=None):
        tk.Frame.__init__(self, master) 
        self.grid() 
        self.createWidgets()
    def createWidgets(self):
        self.EntryText = tk.Entry(self, bg='red')#creating the entry widget
        self.GetButton = tk.Button(self, text='Print', #creating the action button
                                command=self.GetURL) #the command executes a custom function
        self.GetButton.grid(row=0, column=1) #placing the button in the grid
        self.EntryText.grid(row=0, column=0) #placing the entry widget in the grid

#-----Open connection with the target URL (got from the Entry widget)-----#
    def GetURL(self):
         self.url_target = ("http://www." + self.EntryText.get())
         self.req = urllib2.urlopen(self.url_target)
         self.get_http_status()
         self.get_host_headers()
         self.descr_http_status()
         self.url_list()
         self.robot_parser()

#-----Get the HTTP status code from the target URL-----#
    def get_http_status(self):
        self.req_stat = self.req.getcode()
        print self.req_stat
       
#-----Get the headers from the target URL-----#
    def get_host_headers(self):
        headers = self.req.info()
        self.json_headers = json.dumps(dict(headers))
            
#-----Describe status code by getting description from http_dict module-----#
    def descr_http_status(self):
        http_status = http_status_dict[str(self.req_stat)]
        
#------Generation of URL list from parsers-------#
    def url_list(self):
        html_source = htmllib.HTMLParser(formatter.NullFormatter())
        html_source.feed(urllib2.urlopen(self.url_target).read())
        html_source.close()
        #create default formatter. Each parser is associated with a Formatter object used to output parsed
        #data. Since we don't need to do any output, it is sufficient to use the default 'do-nothing' NullFormatter() defined in the formatter package.
        """
        Biblio:
        Python programming — text and web mining - Finn ˚Arup Nielsen
        http://cis.poly.edu/cs912/parsing.txt
        """
        html_source_list = []
        for url in html_source.anchorlist:
            html_source_list.append(url)
           
#------parsing robot.txt file from host-------#
    def robot_parser(self):
        with closing(urlopen(self.url_target + "/robots.txt")) as stream:
            self.robot_parsed = stream.read()
            print self.robot_parsed

app = Application()   
app.master.title('App') 
app.mainloop()




