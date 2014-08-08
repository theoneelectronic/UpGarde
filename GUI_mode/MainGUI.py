#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk
import json, htmllib, formatter, urllib2
from http_dict import http_status_dict
from urllib2 import *
from contextlib import closing


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master) 
        self.grid() 
        self.createWidgets()
        self.master.resizable(False, False) #make the window not resizable
        self.master.wm_iconbitmap("favicon_trex.ico") #set the favicon
        
    def createWidgets(self):
        #widgets creation
        self.StatusTextVar = tk.StringVar() #set a string variable
        self.EntryText = tk.Entry(self, width=23)#creating the entry widget
        self.GetButton = tk.Button(self, height=1, width=9, text='Kumo it!', #creating the action button
                                  command=self.GetURL) #the command executes a custom function
        self.TxtButton = tk.Button(self, height=1, width=9, text='Print to Txt',
                                  command=self.PrintTxt)
        self.QuitButton = tk.Button(self, height=1, width=9, text="Quit",
                                    command=self.QuitApp) 
        self.StatusLabel0 = tk.Label(self, height=1, width=20, text="Status:",
                                  anchor=tk.W)
        self.StatusLabel = tk.Label(self, height=1, width=20, relief="sunken",
                                    anchor=tk.W, textvariable=self.StatusTextVar) #create a label to print the status of the operation
        self.ResultsLabel = tk.Label(self, height=1, width=20, text="Results", anchor=tk.W)
        self.ResultsText = tk.Text(self, height=20, width=100) #create results text widget
        self.ResultsScrollbar = tk.Scrollbar(self, orient=tk.VERTICAL) #create scrollbar connected to the text widget
        self.ResultsScrollbar.config(command=self.ResultsText.yview)
        self.ResultsText.configure(yscrollcommand=self.ResultsScrollbar.set)

        #widgets positioning
        self.GetButton.grid(row=0, column=1, sticky=tk.E) #placing the button in the grid
        self.EntryText.grid(row=0, column=0, sticky=tk.W) #placing the entry widget in the grid
        self.TxtButton.grid(row=1, column=1, sticky=tk.E)
        self.StatusLabel0.grid(row=2, column=0, sticky=tk.W)
        self.StatusLabel.grid(row=3, column=0, sticky=tk.W)
        self.ResultsLabel.grid(row=4, column=0, sticky=tk.W)
        self.ResultsText.grid(row=5, column=0)
        self.ResultsScrollbar.grid(row=5, column=1, sticky=tk.NS)
        self.QuitButton.grid(row=6, column=1, sticky=tk.E)

#-----Open connection with the target URL (got from the Entry widget)-----#
    def GetURL(self):
        try: #try to open the URL
            self.url_target = ("http://www." + self.EntryText.get()) 
            self.req = urllib2.urlopen(self.url_target)
            self.get_http_status()
            self.get_host_headers()
            self.descr_http_status()
            self.url_list()
            self.robot_parser()
            self.StatusTextVar.set("Success!")
            #begin to insert text in the text widget
            self.ResultsText.insert('end', ("Results for " "%s" % self.url_target)+ "\n" + "\n")
            self.ResultsText.insert('end', "--HTTP status:--" + "\n")
            self.ResultsText.insert('end', (str(self.http_status) + "\n"+ "\n"))
            self.ResultsText.insert('end', "--HTTP Headers:--" + "\n")
            self.ResultsText.insert('end', (str(self.headers)+ "\n "+ "\n"))
            self.ResultsText.insert('end', "--Robots.txt:--" + "\n")
            self.ResultsText.insert('end', (str(self.robot_parsed)+ "\n "+ "\n"))
            self.ResultsText.insert('end', "--Sitemap:--" + "\n")
            self.ResultsText.insert('end', (str(self.parsed_url_list)+ "\n "+ "\n"))
        except: #behaviour in case of insuccess
            self.StatusTextVar.set("Wrong input. Please retry")
            pass       

#-----Get the HTTP status code from the target URL-----#
    def get_http_status(self):
        self.req_stat = self.req.getcode()     
       
#-----Get the headers from the target URL-----#
    def get_host_headers(self):
        self.headers = self.req.info()
        self.json_headers = json.dumps(dict(self.headers))
            
#-----Describe status code by getting description from http_dict module-----#
    def descr_http_status(self):
        self.http_status = http_status_dict[str(self.req_stat)]    
        
#------Generation of URL list from parsers-------#
    def url_list(self):
        html_source = htmllib.HTMLParser(formatter.NullFormatter())
        html_source.feed(urllib2.urlopen(self.url_target).read())
        html_source.close()
        #create default formatter. Each parser is associated with a Formatter object used to output parsed
        #data. Since we don't need to do any output, it is sufficient to use the default 'do-nothing' NullFormatter() defined in the formatter package.
        #Biblio:
        #Python programming — text and web mining - Finn ˚Arup Nielsen
        #http://cis.poly.edu/cs912/parsing.txt
        html_source_list = []
        for url in html_source.anchorlist:
            html_source_list.append(url)
            self.parsed_url_list = ("\n".join(str(url) for url in html_source_list))
        
#------parsing robot.txt file from host-------#
    def robot_parser(self):
        with closing(urlopen(self.url_target + "/robots.txt")) as stream:
            self.robot_parsed = stream.read()

#------printing the results to txt file-------#
    def PrintTxt(self):
        output_txt = open("results for " "%s" % self.url_target.lstrip("http://") + ".txt", "w")
        #method .lstrip is used to remove the leading part of text,
        #including "//" that/ mess with directories and breaks the program
        output_txt.write("Kumo test results as follows" + "\n" + "\n")
        output_txt.write("---Target host:--- " + "\n" + self.url_target + "\n" + "\n")
        output_txt.write("--HTTP status:--" + "\n")
        output_txt.write(self.http_status + "\n" + "\n")
        output_txt.write("--HTTP Headers:--" + "\n")
        output_txt.write(str(self.headers) + "\n")
        output_txt.write("--Robots.txt:--" + "\n")
        output_txt.write(str(self.robot_parsed) + "\n")
        output_txt.write("--Sitemap:--" + "\n")
        output_txt.write(self.parsed_url_list)
        output_txt.close()

#------quitting the application-------#
    def QuitApp (self):
        self.master.destroy()


app = Application()   
app.master.title('Kumo') 
app.mainloop()




