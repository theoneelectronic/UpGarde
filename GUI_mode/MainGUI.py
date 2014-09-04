#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk
import json, htmllib, formatter, urllib2
from http_dict import http_status_dict
from ua_dict import ua_dict, ua_list
from urllib2 import *
from contextlib import closing
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master) 
        self.grid() 
        self.createWidgets()
        self.master.resizable(False, False) #make the window not resizable
        #self.master.iconbitmap("Kumo.ico")
    
        try:
            self.master.wm_iconbitmap("Kumo.ico") #set the favicon
        except:
            self.master.wm_iconbitmap("favicon_trex.xbm")
            pass
  
    def createWidgets(self):
        #----defining variables----#
        self.StatusTextVar = tk.StringVar() #set a string variable
        self.RBVar = tk.StringVar() #set a string variable
        self.OMVar = tk.StringVar()
        self.OMVar.set(ua_list[0])

        #----create widgets----#
        self.ButtonFrame = tk.Frame(self)#create the frame for the command button row
        self.EntryLabel = tk.Label(self, width=36, anchor=tk.W,
                                   text="Digit your URL (Hostname only)")
        self.EntryText = tk.Entry(self, width=32, textvariable=self.RBVar)#creating the entry widget
        self.GetButton = tk.Button(self, height=1, width=9, text='Kumo it!', bg="PaleGreen1",#creating the action button
                                  command=self.GetURL) #the command executes a custom function
        self.TxtButton = tk.Button(self.ButtonFrame, height=2, width=9, text='Print to Txt',
                                  bg="White", command=self.PrintTxt) #note that the widget has parent another widget (ButtonFrame)
        self.QuitButton = tk.Button(self, height=1, width=9, text="Quit",
                                    command=self.QuitApp) 
        self.StatusLabel0 = tk.Label(self, height=1, width=20, text="Status:",
                                  anchor=tk.W)
        self.StatusLabel = tk.Label(self, height=1, width=24, relief="sunken",
                                    anchor=tk.W, textvariable=self.StatusTextVar) #create a label to print the status of the operation
        self.ResultsLabel = tk.Label(self, height=1, width=20, text="Results", anchor=tk.W)
        self.ResultsText = tk.Text(self, height=20, width=100) #create results text widget
        self.ResultsScrollbar = tk.Scrollbar(self, orient=tk.VERTICAL) #create scrollbar connected to the text widget
        self.ResultsScrollbar.config(command=self.ResultsText.yview)
        self.ResultsText.configure(yscrollcommand=self.ResultsScrollbar.set)
        #sets the two radiobutton to choose the beginning of the entry widget text 
        self.RadioButton2 = tk.Radiobutton(self, padx=67, text="https://", variable=self.RBVar, value="https://www.")
        self.RadioButton1 = tk.Radiobutton(self, text="http://", variable=self.RBVar, value="http://www.")
        self.Save2Json = tk.Button(self.ButtonFrame, height=2, width=12, text="Save headers \n to JSON",
                                   bg="White", command=self.JsonOut) #note that the widget has parent another widget (ButtonFrame)
        self.ua_listbox = tk.OptionMenu(self.ButtonFrame, self.OMVar, *ua_list) #create a list of user agents
        self.ua_listbox.config(width=35, anchor=tk.W, bg="White")
        self.ua_Label = tk.Label(self.ButtonFrame, width=36, anchor=tk.SW,
                                   text="Please select your User-Agent")
        self.TracerouteButton = tk.Button(self.ButtonFrame, width=15, text="Traceroute",
                                          bg="White", command=self.traceroute)
            
        #----place widgets with the grid method----#
        self.ButtonFrame.grid(row=2, column=0, sticky=tk.SW) #placing the button frame
        self.GetButton.grid(row=0, column=0) #placing the button in the grid
        self.EntryText.grid(row=0, column=0, sticky=tk.W) #placing the entry widget in the grid
        self.ua_Label.grid(row=0, column=2, sticky=tk.NE) #position is relative to the ButtonFrame widget
        self.EntryLabel.grid(row=2, column=0, sticky=tk.NW) #position is relative to the ButtonFrame widget
        self.TxtButton.grid(row=1, column=0) #position is relative to the ButtonFrame widget
        self.Save2Json.grid(row=1, column=1) #position is relative to the ButtonFrame widget
        self.ua_listbox.grid(row=1, column=2, sticky=tk.S) #position is relative to the ButtonFrame widget
        self.TracerouteButton.grid(row=1, column=3, sticky=tk.S) #position is relative to the ButtonFrame widget
        self.StatusLabel0.grid(row=4, column=0, sticky=tk.W)
        self.RadioButton1.grid(row=3, column=0, sticky=tk.W)
        self.RadioButton2.grid(row=3, column=0, sticky=tk.W)
        self.StatusLabel.grid(row=6, column=0, sticky=tk.W)
        self.ResultsLabel.grid(row=7, column=0, sticky=tk.W)
        self.ResultsText.grid(row=8, column=0, columnspan=3)
        self.ResultsScrollbar.grid(row=8, column=3, sticky=tk.NS)
        self.QuitButton.grid(row=9, column=4, sticky=tk.E)
        

#-----Open connection with the target URL (got from the Entry widget)-----#
    def GetURL(self):
        try: #try to open the URL
            ual = str(self.OMVar.get()) #define user agent variable according to what selected on the ua list
            uad = ua_dict[str(ual)] #get the user agent from the ua dictionary with the key same as the ua selected by the user from the ua list
            self.url_target = (self.EntryText.get()) #gets the URL from the entry widget
            self.request = urllib2.Request(self.url_target, headers={'User-agent': '%s' % uad } ) #create the request with the user agent selected by the user from the list
            self.req = urllib2.urlopen(self.request)
            
            #----begins calling the functions----#
            self.get_http_status() #calls the_http status function
            self.get_host_headers() #calls the host_headers function
            self.descr_http_status() #calls the descr_http_status function
            self.url_list() #calls the url_list function
            self.robot_parser() #calls the robot_parser function
            self.StatusTextVar.set("Success!") #sets the status bar text if success
            
            
            #----begin to insert text in the text widget----#
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

#------creating the json file------#
    def JsonOut(self):
        json_headers = json.dumps(dict(self.headers))
        JSON_output = open("JSON headers for " "%s" % self.url_target.lstrip("http://") + ".txt", "w")
        JSON_output.write(json_headers)
        JSON_output.close()

#-----traceroute function-------#
    def traceroute(self):
        host = str(self.EntryText.get().lstrip("http://"))
        p = subprocess.Popen(["tracert", '-d', '-w', '100', host], 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.ResultsText.insert('end', "--Traceroute:--")
        while True:
            line = p.stdout.readline()
            if not line: break
            print '-->',line,
            self.ResultsText.insert('end', (str(line)))
            
        p.wait()

#------quitting the application-------#
    def QuitApp(self):
        self.master.destroy()

app = Application()   
app.master.title('Kumo') 
app.mainloop()
