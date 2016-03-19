#!/usr/bin/python

import string
import httplib
import time
import json
import sys

class Order():

    def __init__(self):
        self.order=0
        self.color = "#00FF00"

    def setLocation(self, cache):
        """ Check the lat/long cache, check new addresses with googleapi.  Set lat/long for the order appropriately.
            After this method is run, the Order will have lat/long set or have its lat set to 'Address is suspect' """

        # create qr codes - requires qrencode to be installed in the os.  Do this every time in case the order numbers change
        #import os
        #os.system("qrencode -o qrcodes/" + str(self.order) + ".png 'MECARD:N:" + self.lastname + ", " + self.firstname + ";ADR:" + self.street + ", " + self.city + ", " + self.state + " " + str(self.zipcode) + ";NOTE:Order " + str(self.order) + ": " + str(self.bags) + " bags;'")

        # 2014, street number and name were in the same column - he changed it for 2015
        #self.streetname = self.street.lower().split(' ',1)[1]

        #2015 - ensure lower case streetname
        self.streetname = self.streetname.lower()
        #2015 - create "street" from number and name
        self.street = self.streetnum + ' ' + self.streetname
        # print self.street

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

class Clump():
    def __init__(self):
        self.bags = 0
        self.orders = []

# write out the cache
def saveFile(fileloc, struct):
    f=open(fileloc, "w")
    json.dump(struct, f, indent=4, separators=(',', ': '))
    f.close()

# read in json file
def loadFile(fileloc):
    f=open(fileloc, "r")
    ret = json.load(f)
    f.close()
    return ret

# read in raw spreadsheet dump and return an ordered list of all Orders
def readOrders(fileloc, cache):
    ret = []
    for line in open(fileloc).readlines():
        if not line.strip(): continue
        line.strip()
        o = Order()
        #o.deposit, o.order, o.firstname, o.lastname, o.orderdate, o.bags, o.donation, o.paid, o.checknum, o.subdivision, o.streetnum, o.streetname, o.city, o.state, o.zipcode, o.phone, o.email, o.comments , o.toss1, o.toss2, o.toss3, o.toss4, o.toss5 = line.rstrip().split('\t')
        o.deposit, o.order, o.firstname, o.lastname, o.orderdate, o.bags, o.donation, o.paid, o.checknum, o.subdivision, o.streetnum, o.streetname, o.city, o.state, o.zipcode, o.phone, o.email, o.comments, o.toss1 = line.rstrip().split('\t')
        o.setLocation(cache)
        ret.append(o)

    import operator
    ret.sort(key=operator.attrgetter('streetname'))
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
        if (o.lat[:7]=='Address'):
            print o.street + " is being ignored due to bad address"
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

def printClumps( clumps, clumpconfig):
    from collections import OrderedDict
    # print out clumps
    print "\nPrinting out clumps"

    clumps = dict()
    for o in orderList:
        if(o.streetname in clumpconfig):
            clumpname = clumpconfig[o.streetname]
            if(clumpname in clumps):
                clumpbags = int(clumps[clumpname].bags)
                clumps[clumpname].bags = clumpbags + int(o.bags)
            else:
                clumps[clumpname] = Clump()
                clumps[clumpname].bags = o.bags
            clumps[clumpname].orders.append(o)
        else:
            print "Missing " + o.streetname + " in clumps config file"
    for key in clumps.keys():
        for o in clumps[key].orders:
            print str(o.order) +"\t" + o.lastname + "\t" + o.firstname + "\t" + o.phone + "\t" + key + "\t" + o.street + "\t" + o.city + "\t" + o.state + "\t" + o.zipcode + "\tComments: " + o.comments + "\t" + str(o.bags)

def createRouteArtifacts( fileloc ):
    routedOrders = readRoutes(fileloc, cache)
    for i in range(1,50):
        r=[]
        for o in routedOrders:
            color = "FF0000"
            if(int(o.route) == i):
                o.color=color
                r.append(o)
        createDeliveryMap( r, "maps/route" + str(i) + ".html" )
        createRouteList( i, r, "routes/route" + str(i) + ".html" )

def createRouteList( routeNum, orders, outputfile ):
    f=open(outputfile, "w")
    f.write('<html><head><style type="text/css">.panel{ padding:6px; border:solid 1px #E4E4E4; background-color:#EEEEEE; margin:8px 0px; width:98% ; min-height:80px; }.bodytext { font: Tahoma, sans-serif; color: #666666;  }.qrcode { float:left; }h1 { margin-bottom:5px; }</style></head><body>')
    f.write('<h1>Route ' + str(routeNum) + '</h1>')
    #f.write('<br/>\nComments: Estimated time XX min, YYY bags.  \n')
    gmapsUrl = "https://maps.google.com/maps?saddr=3301+Hidden+Meadow+Drive+Herndon,+VA+20171&daddr="
    bags=0
    import urllib
    for o in orders:
        bags += int(o.bags)
        address = o.street + " " + o.city + " " + o.state + " " + o.zipcode
        gmapsUrl += address + "+to:"
        f.write('<div class="panel" align="justify"><span class="qrcode">')
        #f.write('<img src="../qrcodes/' + str(o.order) + '.png" height="80px"/></span>')
        f.write('<span class="orangetitle"><a href="https://maps.google.com/maps?q=' + urllib.quote_plus(address) + '" target="_blank">' + address + '</a></span><span class="bodytext">')
        f.write('<br/><b>' + str(o.bags) + ' bags</b> - Order ' + str(o.order) + ' <!-- - <span style="float:right"><a href="">Mark Done</a></span> -->')
        f.write('<br/>Name: ' + o.firstname + ' ' + o.lastname + ' Tel: ' + o.phone)
        f.write('<br><b>' + o.comments + '</b></span></div>')

    gmapsUrl += "3301+Hidden+Meadow+Drive+Herndon,+VA+20171"
    adjustment = ''
    if(bags > 315):
        adjustment = 'Add ' + str(bags - 315) + ' bags'
    elif(bags < 315):
        adjustment = 'Bring back ' + str(315 - bags) + ' bags'

    f.write('<div style="position:absolute;left:150px;top:0px;"><span style="font:1.5em bold italic;">\n' + str(bags) + ' bags.  ' + adjustment + '\n</span><br>')
    f.write('<a href="' + gmapsUrl + '" target="_blank">Google maps directions for entire route</a></body>')
    f.write('</div>')
    f.close()


cache = loadFile("latlong.cache")

######### Step 1 ###############
#orderList = readOrders(sys.argv[1], cache)
#clumpconfig = loadFile("clumps.json")
#setOrderColors(clumpconfig, orderList)
#saveFile("latlong.cache", cache)
## Create map of all orders using the pre-defined clumps.  This helps find streets that should be grouped.
#createDeliveryMap( orderList, './allDeliveries.html')
#
#printClumps( orderList, clumpconfig )  #dump this to a csv file for input into a spreadsheet and manual route creation

########## Step 2 #################
createRouteArtifacts( sys.argv[1] )







