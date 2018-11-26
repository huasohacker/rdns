import json
import requests
import sys
import socket
import re

host = sys.argv[1]

# key from bing  need to set sucriptionKey set
subscriptionKey = ""
customConfigId = ""
###

def get_host(host):
    
    try:
        return str(socket.gethostbyname(host))
    except socket.error:
        return 1

def bing(host):

    searchTerm = "ip:" + host

    url = 'https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/search?q=' + searchTerm + '&customconfig=' + customConfigId
    r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': subscriptionKey})
    j = r.json()
    data = []

    for i in j['webPages']['value']:
         data.append(i['url'])

    return data

def robtex(host):
    url = 'https://freeapi.robtex.com/ipquery/' + host
    r = requests.get(url)
    j = r.json()
    data = []
    
    for i in j['act']:
        data.append(i['o'])

    for i in j['pas']:
        data.append(i['o'])

    return data

ip = get_host(host)
print ('[*] Triying ... %s <-> %s' % (host, ip))

bing=bing(ip)
robtex=robtex(ip)

data = []

for host in bing:
    try:
        a=re.search('//(.*?)/(.*?)',host)
        data.append(a.group(1))
    except:
        data.append(host)

for host in robtex:
    try:
        a=re.search('//(.*?)/(.*?)',host)
        data.append(a.group(1))
    except:
        data.append(host)

data = list(set(data))
data.sort()

for url in data:
    surl = get_host(url)
    if ip == surl:
        print ('[+] ' + url)

