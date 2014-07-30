import Tkinter as tk
import urllib2, json
from http_dict import http_status_dict

class Application(tk.Frame): 
    def __init__(self, master=None):
        tk.Frame.__init__(self, master) 
        self.grid() 
        self.createWidgets()
    def createWidgets(self):
        self.EntryText = tk.Entry(self, bg='red') 
        self.GetButton = tk.Button(self, text='Print',
                                command=self.GetURL) 
        self.GetButton.grid(row=0, column=1)
        self.EntryText.grid(row=0, column=0)

#-----Open connection with the target URL (got from the Entry widget)-----#
    def GetURL(self):
         url_target = ("http://www." + self.EntryText.get())
         self.req = urllib2.urlopen(url_target)
         self.get_http_status()
         self.get_host_headers()
         self.descr_http_status()

#-----Get the HTTP status code from the target URL-----#
    def get_http_status(self):
        self.req_stat = self.req.getcode()
        print self.req_stat
        
#-----Get the headers from the target URL-----#
    def get_host_headers(self):
        headers = self.req.info()
        self.json_headers = json.dumps(dict(headers))
        print self.json_headers
        
#-----Describe status code by getting description from http_dict module-----#
    def descr_http_status(self):
        http_status = http_status_dict[str(self.req_stat)]
        print http_status


app = Application()   
app.master.title('App') 
app.mainloop()




