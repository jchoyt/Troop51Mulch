#! /bin/python
from numpy import *
 
pop_size = 2000
l = 200
z = zeros((pop_size,l))
 
def mutate () :
        for i in xrange(pop_size):
                for j in xrange(l) :
                        if random.random()<0.5 :
                                z[i,j] = random.random()
 
import cProfile
cProfile.run('mutate()')
 
def mutate_matrix () :
        r = random.random(size=(pop_size,l))<0.5
        v = random.random(size=(pop_size,l))
        k = r*v + logical_not(r)*z
 
cProfile.run('mutate_matrix()')
