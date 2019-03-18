#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 15:27:52 2019

@author: zlchen
"""

import os
import sys
import networkx as nx
import numpy as np

os.chdir(os.path.dirname(sys.argv[0]))

from load_data import cross_data,road_data,car_data


#G = nx.Graph()
D = nx.DiGraph()

# print(list(cross_data['id']))

D.add_nodes_from([int(x) for x in list(cross_data['id'])])

road = []
for i in range(road_data.shape[0]):
    attribute = {}
    attribute['length']=road_data.iloc[i,1]
    attribute['speed']=road_data.iloc[i,2]
    attribute['channel']=road_data.iloc[i,3]
    #road_index = ()
    road.append((road_data.iloc[i,4],road_data.iloc[i,5],attribute))

D.add_edges_from(road)

nx.draw_networkx(D, node_size=30, pos=nx.spring_layout(D), arrows=True, with_labels=True)