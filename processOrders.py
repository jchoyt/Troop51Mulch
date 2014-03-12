#!/usr/bin/python

import string
import httplib
import time
import json
import sys

class Order():
    color = "#00FF00"
    def __init__(self):
        self.order=0

    def setlocation(self, cache):
        """ Check the lat/long cache, check new addresses with googleapi.  Set lat/long for the order appropriately.
            After this method is run, the Order will have lat/long set or have its lat set to 'Address is suspect' """
        self.streetname = self.street.lower().split(' ',1)[1]
        # print self.streetname
        if(self.street in cache):
            self.lat = cache[self.street][0]
            self.lon = cache[self.street][1]
        else:
            print "Looking up lat/long for " + self.street
            conn = httplib.HTTPConnection("maps.googleapis.com")
            self.address = self.street + " " +  self.city + " " +  self.state + " " +  self.zipcode
            conn.request("GET", "/maps/api/geocode/json?address=" + self.address.replace(" ", "%20") + "&sensor=true")
            r1 = conn.getresponse()
            time.sleep(0.5)
            # parse out the type, lat and long
            jsonData = json.loads(r1.read())
            # print jsonData
            if ('ROOFTOP' == jsonData['results'][0]['geometry']['location_type']):
                self.lat = str(jsonData ['results'][0]['geometry']['location']['lat'])
                self.lon = str(jsonData ['results'][0]['geometry']['location']['lng'])
            else:
                self.lat = "Address is suspect"
                self.lon = ""
            cache[self.street] = (self.lat, self.lon)

# read in lat/long cachce and return it
def loadLatLongCache(fileloc):
    print "\nReading in lat/long cache"
    import json
    f=open(fileloc, "r")
    ret = json.load(f)
    f.close()
    return ret

# write out the cache
def saveLatLongCache(fileloc):
    print "\nWriting out the lat/long cache"
    f=open(fileloc, "w")
    json.dump(cache, f, indent=4, separators=(',', ': '))
    f.close()

# read in clump configs
def loadClumpConfig(fileloc):
    f=open(fileloc, "r")
    ret = json.load(f)
    f.close()
    return ret

# read in raw spreadsheet dump and return an ordered list of all Orders
def readOrders(fileloc, cache):
    print "\nReading in spreadsheet dump"
    ret = []
    for line in open(fileloc).readlines():
        if not line.strip(): continue
        line.strip()
        o = Order()
        o.deposit, o.order, o.firstname, o.lastname, o.orderdate, o.bags, o.donation, o.paid, o.checknum, o.subdivision, o.street, o.city, o.state, o.zipcode, o.phone, o.email, o.comments, o.toss1, o.toss2, o.toss3, o.toss4, o.toss5 = line.rstrip().split('\t')
        o.setlocation(cache)
        ret.append(o)

    import operator
    ret.sort(key=operator.attrgetter('streetname'))
    return ret

# make an HTML map of deliveries
def createDeliveryMap(orders, outputfile):
    zoomlevel = 13  # bigger is closer
    print "Creating overview map of " + str(len(orders)) + " deliveries"
    import pygmaps
    # Church of the Epiphany - 38.906814,-77.40729
    # centered at rough central order  38.927115,-77.384287
    mymap = pygmaps.maps(38.927115,-77.384287, zoomlevel)
    for o in orders:
        if (o.lat[:7]=='Address'):
            print o.street + " is being ignored due to bad address"
            continue
        mymap.addpoint(float(o.lat), float(o.lon), o.color, o.street + " - " + o.bags + " bags")

    mymap.draw(outputfile)



def randomColor():
    from random import randrange
    ret = "%s" % "".join([hex(randrange(0, 255))[2:] for i in range(3)])
    return ret

def setOrderColors(clumpconfig, orderList):
    for clumpname in clumpconfig.values():
        c = randomColor()
        for o in orderList:
            if (o.streetname in clumpconfig and clumpconfig[o.streetname] == clumpname ):
                o.color = c;

cache = loadLatLongCache("latlong.cache")
orderList = readOrders(sys.argv[1], cache)
clumpconfig = loadClumpConfig("clumps.json")
setOrderColors(clumpconfig, orderList)
saveLatLongCache("latlong.cache")
createDeliveryMap( orderList, './allDeliveries.html')

# print out clumps
print "\nPrinting out clump names and bag total for large clumps (100+ bags)"

clumps = dict()
for o in orderList:
    if(o.streetname in clumpconfig):
        clumpname = clumpconfig[o.streetname]
        if(clumpname in clumps):
            clumpbags = int(clumps[clumpname])
            clumps[clumpname] = clumpbags + int(o.bags)
        else:
            clumps[clumpname] = o.bags

    else:
        print "Missing " + o.streetname + " in clumps config file"


for key in clumps.keys():
    if int(clumps[key]) > 99:
        print key + ":" + str(clumps[key])
