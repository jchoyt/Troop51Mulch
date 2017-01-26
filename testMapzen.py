#!/usr/bin/python

from mulchLibrary import readRoutes, loadFile, Route, Order
from step1 import saveFile
import json
import requests
import time
import sys

key = "mapzen-ukv36Eb"
coee = "{\"lat\":38.904748,\"lon\":-77.397019}"
coee_street = "3301 hidden meadow drive"
routes = {}

def optimize_route(r, route15matrix):
    pass

def process_matrix(order_list, cached_times, new_matrix):
    """adds the new_matrix to the cached_times
    new_matrix is an array of arrays where each sub array is the distances from a single 'from'"""
    for location in new_matrix:
        for cell in location:
            # if cell["time"] > 0:  #weed out the "going to where I started" trips
            start = order_list[cell["from_index"]].street
            end = order_list[cell["to_index"]].street
            if start != end:
                direction = start + " to " + end
                cached_times[direction] = { "dist":cell["distance"], "time":cell["time"]}

def add_coee_to_order_list(order_list):
    coee_order = Order()
    coee_order.street=coee_street
    coee_order.lat=38.904748
    coee_order.lon=-77.397019
    new_list = [coee_order]
    new_list.extend(order_list)
    new_list.append(coee_order)
    return new_list

cache = loadFile("latlong.cache")
orders = readRoutes("2016created_routes.csv", cache)
cached_times = loadFile("drive_cache.json")

""" configure the routes """
for order in orders:
    route = routes.setdefault(int(order.route), Route(int(order.route)))
    route.orders.append(order)

def build_matrix_url(order_list, name):
     matrix_url = "http://matrix.mapzen.com/many_to_many?json={\"costing\":\"auto\",\"locations\":[" + coee
     for order in order_list:
         matrix_url += ",{\"lat\":" + \
             str(order.lat) + ",\"lon\":" + str(order.lon) + "}"
     matrix_url += "," + coee + ''.join(["]}&id=",name,"&api_key=", key])
     return matrix_url

# """Get a matrix for every route and cache it"""
# for route in routes.values():
#     matrix_url =  build_matrix_url(route.orders, "Route"+str(route.num))
#     status_code = 0
#     while status_code != 200:
#         response = requests.get(matrix_url)
#         status_code = response.status_code
#         print(status_code)
#         if status_code == 429:
#             sys.exit()
#     process_matrix(add_coee_to_order_list(route.orders), cached_times, response.json()["many_to_many"])
#     #  print("retrieved from ", matrix_url)
#     time.sleep(15)
# saveFile("drive_cache.json", cached_times)


"""Calculate the drive time for each route"""
for route in routes.values():
    route_time = 0
    last_order = None
    augmented_route_orders = add_coee_to_order_list(route.orders)
    for order in augmented_route_orders:
        if last_order == None:
            pass
        else:
            key = last_order.street + " to " + order.street
            route_time += int(cached_times[key].get("time"))
        last_order = order
    route.time = route_time
    print("Route ",str(route.num)," drive time: ",str(round(route_time/60)), " minutes")
