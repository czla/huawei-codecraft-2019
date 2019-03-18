#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 15:23:44 2019

@author: zlchen
"""

import pandas as pd
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

car_file = '../../config/car.txt'
cross_file = '../../config/cross.txt'
road_file = '../../config/road.txt'

car_data = pd.read_csv(car_file, sep = ',')
car_data.rename(columns = lambda x:x.replace('#(','').replace(')',''), inplace=True)
car_data['id'] = car_data['id'].str.split('(').str[1]
car_data['planTime'] = car_data['planTime'].str.split(')').str[0]
# print(car_data.head())

cross_data = pd.read_csv(cross_file, sep = ',')
cross_data.columns = ['id','roadIdU','roadIdR','roadIdD','roadIdL']
cross_data['id'] = cross_data['id'].str.split('(').str[1]
cross_data['roadIdL'] = cross_data['roadIdL'].str.split(')').str[0]
#print(cross_data.head())

road_data = pd.read_csv(road_file, sep = ',')
road_data.rename(columns = lambda x:x.replace('#(','').replace(')',''), inplace=True)
road_data['id'] = road_data['id'].str.split('(').str[1]
road_data['isDuplex'] = road_data['isDuplex'].str.split(')').str[0]
# print(road_data.head())
