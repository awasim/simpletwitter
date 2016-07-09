def getlongurl2.x(url):
    import urllib
    resp = urllib.open(url)
    return resp.url

def getlongurl3.x(url):
    import urllib.request
    resp = urllib.request.urlopen(url)
    return resp.url
