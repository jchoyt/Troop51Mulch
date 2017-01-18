#!/usr/bin/python
"""
Assumptions:
    -   All orders have at least one bag
"""
from random import sample
from math import radians, cos, sin, asin, sqrt
import sys

from mulchLibrary import loadFile, Order, Route
from step1 import readOrders

truck_sizes = [331, 331, 331, 331, 331]
drive_speed = 10 # miles per hour


def gen_depot():
    """
    creates the start/end place for each route, duck typing to look like an order for the purposes
    of route creation
    """
    depot = Order()
    depot.streetname = 'hidden meadow drive'
    depot.streetnum = 3301
    depot.lat = 38.906372
    depot.lon = -77.407503
    depot.bags = 0
    return depot

def gen_individual(orderList):
    """
    takes a list of Orders, shuffles them, and returns a new list of Orders
    """
    return sample(orderList, k=len(orderList))

def gen_population(orderList, pop_size):
    pass


def define_routes(orderList):
    """
    breaks an ordered list of orders into routes
    """
    truck_num = 0
    truck_size = truck_sizes[truck_num]
    routes = []
    bag_total = 0
    route_num = 1
    current_route = Route(route_num)
    current_route.truck_num = truck_num
    current_route.orders.append(gen_depot())
    # break into routes
    for x in orderList:
        bag_total += int(x.bags)
        if truck_size >= bag_total:
            # add to current route
            current_route.orders.append(x)
            current_route.bags = bag_total
        else:
            # finish off route with the depot at the end
            current_route.orders.append(gen_depot())
            routes.append(current_route)
            # start a new route
            bag_total = int(x.bags)
            route_num += 1
            current_route = Route(route_num)
            current_route.orders.append(gen_depot())
            current_route.orders.append(x)
            current_route.bags = bag_total
            # increment the truck number
            truck_num+= 1
            if truck_num >= len(truck_sizes):
                truck_num = 0
            current_route.truck_num = truck_num
    # add the last route
    current_route.orders.append(gen_depot())
    routes.append(current_route)
    return routes

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).  Answer in miles.
    Swiped from http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    miles = 3959 * c
    # print(miles)
    return miles

def calculate_time(route):
    """
    Estimates the delivery time for a route.
    It updates the route with the total and returns the total time
    """
    total_bags, total_distance, street_changes = 0, 0, -1  # -1 to account for change from None to the depot
    last_street, last_lat, last_lon = None, None, None
    for order in route.orders:
        total_bags += int(order.bags)
        # print(order.streetname, last_street)
        if order.streetname != last_street:
            street_changes+= 1
            last_street = order.streetname
        if last_lat != None:
            total_distance += haversine (float(last_lon), float(last_lat), float(order.lon), float(order.lat))
        last_lat = order.lat
        last_lon = order.lon
    # 6 bags per minute + 5 minutes per street change + distance driven at 20 mph
    # print(street_changes)
    total_time = total_bags / 6 + street_changes * 4 + total_distance / drive_speed
    route.time = total_time
    return total_time

def fitness(individual):
    """
    Takes an individual (i.e., an ordered list of orders), breaks them up into routes, calculates the
    time for each route.  Adds up all the times and returns that as the score
    """
    routes = define_routes(individual)
    print(len(routes))
    total_time = 0
    total_bags = 0
    for route in routes:
        total_time += calculate_time(route)
        total_bags += route.bags
        print(str(route.num) + " " + str(route.bags) + " " + str(route.time))
    print("Total bags: " + str(total_bags))
    return total_time


def grade(pop, target):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, target) for x in pop))
    return summed / (len(pop) * 1.0)

if __name__ == "__main__":
    order_2016 = [239,241,240,238,253,202,76,187,256,151,147,167,182,46,178,184,142,125,70,185,227,61,249,254,33,247,16,105,114,174,19,244,243,152,81,84,234,72,170,245,169,55,67,201,160,120,23,80,162,45,78,108,116,208,155,127,79,248,130,131,26,219,94,118,42,231,232,126,136,246,75,62,166,15,57,6,205,82,222,95,180,195,214,146,89,34,1,59,134,39,3,66,236,21,220,128,47,196,124,50,251,226,200,90,85,109,10,194,192,133,60,158,99,63,230,135,88,154,11,100,35,175,179,132,91,157,189,250,233,28,163,216,77,242,14,141,7,110,206,176,54,225,188,68,73,255,224,153,56,32,9,211,217,30,93,203,209,237,204,123,97,83,164,58,215,107,140,171,213,139,138,104,168,212,69,40,103,186,150,96,111,8,102,29,53,48,210,87,207,5,37,144,22,98,159,137,86,18,2,38,24,172,156,52,51,113,20,258,165,49,17,115,43,228,161,44,191,145,71,64,190,223,193,149,218,4,12,183,41,121,257,199,112,173,106,65,197,36,101,143,92,25,235,177,181,31,148,117,13,122,129,221,229]


    cache = loadFile("latlong.cache")
    orderList = readOrders(sys.argv[1], cache)
    # i = gen_individual(orderList)
    # i = orderList
    i = []
    for ordernum in order_2016:
        for order in orderList:
            # print(str(order.order) + ":" + str(ordernum))
            if int(order.order) == ordernum:
                i.append(order)
                continue
    print(fitness(i))

    # Pull out just the order numbers
    # orderNums = [o.order for o in orderList]
    # printOrder(orderNums)



    # Generate random Order list
    # for i in range(10):
    #     newOrderList = sample(orderList, k=len(orderList))
    #     orderNums = [o.order for o in newOrderList]
    #     printOrder(orderNums)
