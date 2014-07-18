import htmllib, formatter, urllib2, var

html_source = htmllib.HTMLParser(formatter.NullFormatter())

#create default formatter. Each parser is associated with a Formatter object used to output parsed
#data. Since we don't need to do any output, it is sufficient to use the default 'do-nothing' NullFormatter() defined in the formatter package.
html_source.feed(urllib2.urlopen(var.url_target).read())
html_source.close()

"""
Biblio:
Python programming — text and web mining - Finn ˚Arup Nielsen
http://cis.poly.edu/cs912/parsing.txt
"""


