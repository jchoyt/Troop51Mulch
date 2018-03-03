#!/usr/bin/python

import string
# from http.client import HTTPConnection
import time
import json
import sys
import requests

class Order:

    address = ""

    def __init__(self):
        self.order=0
        self.color = "#00FF00"

    def setLocation(self, cache):
        """ Check the lat/long cache, check new addresses with googleapi.  Set lat/long for the order appropriately.
            After this method is run, the Order will have lat/long set or have its lat set to 'address is suspect' """

        # create qr codes - requires qrencode to be installed in the os.  Do this every time in case the order numbers change
        #import os
        #os.system("qrencode -o qrcodes/" + str(self.order) + ".png 'MECARD:N:" + self.lastname + ", " + self.firstname + ";ADR:" + self.street + ", " + self.city + ", " + self.state + " " + str(self.zipcode) + ";NOTE:Order " + str(self.order) + ": " + str(self.bags) + " bags;'")

        # 2014, street number and name were in the same column - he changed it for 2015
        #self.streetname = self.street.lower().split(' ',1)[1]

        #2015 - ensure lower case streetname
        self.streetname = self.streetname.lower()
        #2015 - create "street" from number and name
        self.street = self.streetnum + ' ' + self.streetname

        if(self.street in cache):
            self.lat = cache[self.street][0]
            self.lon = cache[self.street][1]
        else:
            print("Looking up lat/long for " + self.street)
            self.address = self.street + " " +  self.city + " " +  self.state + " " +  self.zipcode
            r1 = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + self.address.replace(" ", "%20") + "&sensor=true&key= AIzaSyAU54x8sEfXPLcv3yvaFTX3SISRymn8uaQ")
            time.sleep(0.5)
            # # parse out the type, lat and long
            jsonData = r1.json()
            if ('ROOFTOP' == jsonData['results'][0]['geometry']['location_type']):
                self.lat = str(jsonData ['results'][0]['geometry']['location']['lat'])
                self.lon = str(jsonData ['results'][0]['geometry']['location']['lng'])
            else:
                self.lat = "address is suspect"
                self.lon = ""
            cache[self.street] = (self.lat, self.lon)

    def __str__(self):
        return self.address

class Route:
    def __init__(self, routeNumber):
        self.num = routeNumber
        self.orders = []
        self.time = 0
        self.truck_num = 0

    def finalize(self):
        # get total number of bags
        self.bags = 0
        for o in self.orders:
            self.bags += o.bags;


        # determine time to drive the route


class Clump:
    def __init__(self):
        self.bags = 0
        self.orders = []


# read in json file
def loadFile(fileloc):
    with(open(fileloc, "r")) as f:
        ret = json.load(f)
    return ret

def readRoutes(fileloc, cache):
    ret=[]
    for line in open(fileloc).readlines():
        if not line.strip(): continue
        line.strip()
        o=Order()
        o.order, o.lastname, o.firstname, o.phone, o.streetname, o.street, o.city, o.state, o.zipcode, o.comments, o.bags, o.route = line.rstrip().split('\t')
        #2015 - change for difference in spreadsheet.  Now the street number and name are separate on the main workbook so I emulate that here.  Read Orders will just put it back together again.
        o.streetname = o.street.lower().split(' ',1)[1]
        o.streetnum = o.street.lower().split(' ',1)[0]
        o.setLocation(cache)
        ret.append(o)
    return ret

# make an HTML map of deliveries
def createDeliveryMap(orders, outputfile):
    zoomlevel = 13  # bigger is closer
    #print "Creating overview map of " + str(len(orders)) + " deliveries"
    import pygmaps
    # Church of the Epiphany - 38.906814,-77.40729
    # centered at rough central order  38.927115,-77.384287
    mymap = pygmaps.maps(38.927115,-77.384287, zoomlevel)
    for o in orders:
        if (o.lat[:7]=='address'):
            print(o.street + " is being ignored due to bad address")
            continue
        # The default pygmaps won't work with this.  The following change will rectify.  See http://stackoverflow.com/questions/19142375/how-to-add-a-title-to-each-point-mapped-on-google-maps-using-python-pygmaps
        #This is an issue with pygmaps.py program I downloaded. In the supplied package there is no option to add a 4th column (title).
        #
        #Now I modified pygmaps.py program like below:
        #
        #from
        #
        #def addpoint(self, lat, lng, color = '#FF0000'):
        #    self.points.append((lat,lng,color[1:]))
        #to:
        #
        #def addpoint(self, lat, lng, color = '#FF0000', title = None):
        #    self.points.append((lat,lng,color[1:],title))
        #
        label = o.street + " - Order " + o.order + " - " + o.bags + " bags"
        mymap.addpoint(float(o.lat), float(o.lon), o.color, label)

    mymap.draw(outputfile)

def get_bounding_box():
    """
    Digs through the latlong cache and returns a bounding box around all the deliveries.
    Returned list is [min lat, max lat, min long, max long]. Min/max is by sort order of abs(value).
    """
    with(open("latlong.cache", "r")) as f:
        cache = json.load(f)
    x = cache.values()
    lats = [item[0] for item in x]
    lons = [item[1] for item in x]
    return [float(min(lats)), float(max(lats)),  float(min(lons)), float(max(lons))]
