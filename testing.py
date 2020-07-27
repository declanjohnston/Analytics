# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 18:25:18 2020

@author: decla
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import hockey_scraper
from datetime import date, timedelta
import csv
import logging
READ_MODE = 'r'

my_list = [12, 65, 54, 39, 102, 339, 221, 50, 70, ] 
my_list2 = [[1,2,3],[1,1,1],[1,2,4]]
# use anonymous function to filter and comparing  
# if divisible or not 
result = list(filter(lambda x: (x[0] == x[2]), my_list2))  
  
# printing the result 
print(result)  