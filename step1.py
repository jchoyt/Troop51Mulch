#!/usr/bin/python

import mulchLibrary
import string
import time
import json
import sys

# write out the cache
def saveFile(fileloc, struct):
    f=open(fileloc, "w")
    json.dump(struct, f, indent=4, separators=(',', ': '))
    f.close()

# read in raw spreadsheet dump and return an ordered list of all Orders
def readOrders(fileloc, cache):
    ret = []
    for line in open(fileloc).readlines():
        if not line.strip(): continue
        line.strip()
        o = mulchLibrary.Order()
        #o.deposit, o.order, o.firstname, o.lastname, o.orderdate, o.bags, o.donation, o.paid, o.checknum, o.subdivision, o.streetnum, o.streetname, o.city, o.state, o.zipcode, o.phone, o.email, o.comments , o.toss1, o.toss2, o.toss3, o.toss4, o.toss5 = line.rstrip().split('\t')
        # 2016 o.deposit, o.order, o.firstname, o.lastname, o.orderdate, o.bags, o.donation, o.paid, o.checknum, o.subdivision, o.streetnum, o.streetname, o.city, o.state, o.zipcode, o.phone, o.email, o.comments, o.toss1 = line.rstrip().split('\t')
        # new for 2017 below
        toss1, o.order, toss2, o.firstname, o.lastname, o.streetnum, o.streetname, toss3, o.city, o.state, o.zipcode, o.subdivision, o.bags, o.phone, o.email, o.comments, toss4  = line.rstrip().split('\t')
        o.setLocation(cache)
        ret.append(o)

    import operator
    ret.sort(key=operator.attrgetter('streetname'))
    return ret

def randomColor():
    # from random import randrange
    # ret = "%s" % "".join([hex(randrange(0, 255))[2:] for i in range(3)])
    import random
    ret = '#%06X' % random.randint(0,256**3-1)
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
    print("\nPrinting out clumps")

    clumps = dict()
    for o in orderList:
        if(o.streetname in clumpconfig):
            clumpname = clumpconfig[o.streetname]
            if(clumpname in clumps):
                clumpbags = int(clumps[clumpname].bags)
                clumps[clumpname].bags = clumpbags + int(o.bags)
            else:
                clumps[clumpname] = mulchLibrary.Clump()
                clumps[clumpname].bags = o.bags
            clumps[clumpname].orders.append(o)
        else:
            print("Missing " + o.streetname + " in clumps config file")
    for key in list(clumps.keys()):
        for o in clumps[key].orders:
            print (str(o.order) + "\t" + o.lastname + "\t" + o.firstname + "\t" + o.phone + "\t" + key + "\t" + o.street + "\t" + o.city + "\t" + o.state + "\t" + o.zipcode + "\tComments: " + o.comments + "\t" + str(o.bags))


###############################################################
if __name__ == "__main__":
    cache = mulchLibrary.loadFile("latlong.cache")
    orderList = readOrders(sys.argv[1], cache)
    clumpconfig = mulchLibrary.loadFile("clumps.json")
    setOrderColors(clumpconfig, orderList)
    saveFile("latlong.cache", cache)
    # Create map of all orders using the pre-defined clumps.  This helps find streets that should be grouped.
    mulchLibrary.createDeliveryMap( orderList, './allDeliveries.html')

    printClumps( orderList, clumpconfig )  #dump this to a csv file for input into a spreadsheet and manual route creation
