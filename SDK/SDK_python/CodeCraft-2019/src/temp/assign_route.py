#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:50:40 2019

@author: zlchen
"""

from generate_graph import D,nx
from load_data import car_data

print(car_data.head())

route = []
for i in range(car_data.shape[0]):
    route_i = [car_data.iloc[i,0]]
    route_i.append(nx.shortest_path(D,car_data.iloc[i,1],car_data.iloc[i,2]))
    route.append(route_i)
    
print(route)