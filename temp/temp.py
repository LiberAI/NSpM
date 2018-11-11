import urllib2
proxy = urllib2.ProxyHandler({'https': 'http://proxy.iiit.ac.in:8080/'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
result = urllib2.urlopen('https://www.python.org')
print result.read()