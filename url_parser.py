import htmllib, formatter, urllib
html_source = htmllib.HTMLParser(formatter.NullFormatter())
html_source.feed(urllib.urlopen("http://www.engeene.it").read())
html_source.close()
for url in html_source.anchorlist:
	print url

