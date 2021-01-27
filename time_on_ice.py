# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 22:59:03 2020

@author: decla
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import hockey_scraper
from datetime import date, timedelta
import csv
import GLOBAL
import json

def _ReadCsv(filename):
    """Read CSV file from remote path.

    Args:
      filename(str): filename to read.
    Returns:
      The contents of CSV file.
    Raises:
      ValueError: Unable to read file
    """
    data = []
    try:
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            for row in csv_reader:
                data.append(row)
    except IOError:
        logging.exception('')
    if not data:
        raise ValueError('No data available')
    return data

def total_time_on_ice(player_id):
    #go through every game and add TOI for the player
    toi = 0
    
    return toi
    
def total_time_on_ice_dictionary():
    #copy the player dictionary, then for each player find their TOI
    data = _ReadCsv("C:/Users/decla/Documents/Analytics/data/players/player_lookup.csv")
    data.pop(0)
    for player in data:
        toi = total_time_on_ice(player[0])
        

total_time_on_ice_dictionary()