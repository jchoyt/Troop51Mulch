#!/usr/bin/python

import string
import httplib
import time
import simplejson
import sys

def checkvalid( address ):
    # check the address with googleapi
    conn = httplib.HTTPConnection("maps.googleapis.com")
    conn.request("GET", "/maps/api/geocode/json?address=" + address.replace(" ", "%20") + "&sensor=true")
    r1 = conn.getresponse()
    time.sleep(0.5)
    # parse out the type, lat and long
    jsonData = simplejson.loads( r1.read() )
    # print jsonData
    if ('ROOFTOP' == jsonData['results'][0]['geometry']['location_type']):
        return str(jsonData ['results'][0]['geometry']['location']['lat']) +  ", " + str(jsonData ['results'][0]['geometry']['location']['lng'])
    else:
        return "Address is suspect"

def printhead():
    print "<html><body><table><tbody>"
    sys.stdout.flush()

def printfoot():
    print "</tbody></table></body></html>"

printhead()
for line in open(sys.argv[1]).readlines():
    if not line.strip(): continue
    line.strip();
    bags, street, city, state, zipcode = line.rstrip().split('\t')
    print "<tr><td>" + street, city, state, zipcode + "</td><td>" + checkvalid( street + " " +  city + " " +  state + " " +  zipcode) + "</td></tr>"
    sys.stdout.flush()
printfoot()
