#!/usr/bin/python

import mulchLibrary
import sys


def createRouteArtifacts( fileloc ):
    routedOrders = mulchLibrary.readRoutes(fileloc, cache)
    for i in range(1,50):
        r=[]
        for o in routedOrders:
            color = "FF0000"
            if(int(o.route) == i):
                o.color=color
                r.append(o)
        # mulchLibrary.createDeliveryMap( r, "maps/route" + str(i) + ".html" )
        createRouteList( i, r, "routes/route" + str(i) + ".html" )

def createRouteList( routeNum, orders, outputfile ):
    f=open(outputfile, "w")
    f.write('<html><head><style type="text/css">.panel{ padding:6px; border:solid 1px #E4E4E4; background-color:#EEEEEE; margin:8px 0px; width:98% ; min-height:80px; }.bodytext { font: Tahoma, sans-serif; color: #666666;  }h1 { margin-bottom:5px; }</style></head><body>')
    f.write('<h1>Route ' + str(routeNum) + '</h1>')
    #f.write('<br/>\nComments: Estimated time XX min, YYY bags.  \n')
    gmapsUrl = "https://maps.google.com/maps?saddr=3301+Hidden+Meadow+Drive+Herndon,+VA+20171&daddr="
    bags=0
    import urllib
    for o in orders:
        bags += int(o.bags)
        address = o.street + " " + o.city + " " + o.state + " " + o.zipcode
        gmapsUrl += address + "+to:"
        f.write('<div class="panel" align="justify">')
        f.write('<span class="orangetitle"><a href="https://maps.google.com/maps?q=' + urllib.parse.quote_plus(address) + '" target="_blank">' + address + '</a></span><span class="bodytext">')
        f.write('<br/><b>' + str(o.bags) + ' bags</b> - Order ' + str(o.order) + ' <!-- - <span style="float:right"><a href="">Mark Done</a></span> -->')
        f.write('<br/>Name: ' + o.firstname + ' ' + o.lastname + ' Tel: ' + o.phone)
        f.write('<br><b>' + o.comments + '</b></span></div>')

    gmapsUrl += "3301+Hidden+Meadow+Drive+Herndon,+VA+20171"
    adjustment = ''
    if(bags > 315):
        adjustment = 'Add ' + str(bags - 315) + ' bags'
    elif(bags < 315):
        adjustment = 'Bring back ' + str(315 - bags) + ' bags'

    f.write('<div style="position:absolute;left:250px;top:0px;"><span style="font:1.5em bold italic;">\n' + str(bags) + ' bags.  ' + adjustment + '\n</span><br>')
    f.write('<a href="' + gmapsUrl + '" target="_blank">Google maps directions for entire route</a></body>')
    f.write('</div>')
    f.close()

##########################################################################

if __name__ == "__main__":
    cache = mulchLibrary.loadFile("latlong.cache")
    createRouteArtifacts( sys.argv[1] )
