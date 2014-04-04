import math

class Delivery:
    bags = 0
    street = ""
    address = ""
    latitude = 0
    longitude = 0
    # distance in miles per degree latitude
    miles = 69

    def distance(self, otherDelivery):
        dx = otherDelivery.latitude - self.latitude
        dy = otherDelivery.longitude - self.longitude
        distance = self.miles * math.sqrt( math.pow( dx, 2 ) + math.pow( dy, 2 ) )
        if( self.street != otherDelivery.street ):
            distance = distance + 0.5
        return distance

first = Delivery()
first.latitude = 38.9266409
first.longitude = -77.403143

second = Delivery()
second.latitude = 38.9266409
second.longitude = -77.403143

print first.distance(second)

second.latitude = 38.926848
second.longitude = -77.40389

print first.distance(second)

second.street = "other street"

print first.distance(second)


