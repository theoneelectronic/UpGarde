
http_status_dict = {"100": "100 Continue : Server has received the request headers and client should proceed to send the request body",
                    "101": "101 Switching Protocols : The requester has asked the server to switch protocols and the server is acknowledging that it will do so",
                    "102": "102 Processing : Server has received and is processing the request, but no response is available yet",
                    "200": "200 OK : Standard response for successful HTTP requests.",
                    "201": "201 Created : The request has been fulfilled and resulted in a new resource being created.",
                    "202": "202 Accepted : The request has been accepted for processing, but the processing has not been completed.",
                    "203": "203 Non-Authoritative Information : The server successfully processed the request, but is returning information that may be from another source.",
                    "204": "204 No Content : The server successfully processed the request, but is not returning any content. Usually used as a response to a successful delete request.",
                    "205": "205 Reset Content : The server successfully processed the request, but is not returning any content.",
                    "206": "206 Partial Content : The server is delivering only part of the resource due to a range header sent by the client.",
                    "207": "207 Multi-Status (WebDAV; RFC 4918) : The message body that follows is an XML message and can contain a number of separate response codes, depending on how many sub-requests were made.",
                    "208": "208 Already Reported (WebDAV; RFC 5842) : The members of a DAV binding have already been enumerated in a previous reply to this request, and are not being included again.",
                    "226": "226 IM Used (RFC 3229) : The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance.",
                    "300": "300 Multiple Choices : Indicates multiple options for the resource that the client may follow (i.e. different format options for video, list files with different extensions, or word sense disambiguation).",
                    "301": "301 Moved Permanently : This and all future requests should be directed to the given URI.",
                    "302": "302 Found : The client is required to perform a temporary redirect. However industry practice implemented 302 with the functionality of a 303 See Other.",
                    "303": "303 See Other : The response to the request can be found under another URI using a GET method.",
                    "304": "304 Not Modified : Indicates that the resource has not been modified since the version specified by the request headers If-Modified-Since or If-Match.",
                    "305": "305 Use Proxy : The requested resource is only available through a proxy, whose address is provided in the response.",
                    "306": "306 Switch Proxy : No longer used. Originally meant: Subsequent requests should use the specified proxy.",
                    "307": "307 Temporary Redirect : In this case, the request should be repeated with another URI; however, future requests should still use the original URI.",
                    "308": "308 Permanent Redirect : The request, and all future requests should be repeated using another URI.",
                    
                    
                    
                    }
