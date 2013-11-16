import urllib2
url = 'http://api.map.baidu.com/location/ip?ak=E1356a909570fb0e255f1f278dabd11b&ip=76.88.39.95'
request = urllib2.Request(url)
response = urllib2.urlopen(request)
print response.read().decode('raw_unicode_escape').split('|')[2]