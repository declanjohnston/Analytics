# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 10:45:32 2020

Is called by the game importer to have the shift information for the game

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

def import_shifts(game_id):
    #do stuff
    path = "C:/Users/decla/Documents/Analytics/data/raw/docs/2019/json_shifts/" + str(game_id) + ".txt"
    with open(path) as json_file:
        data = json.load(json_file)
        for shift in data['data']:
            print(shift['lastName'])


import_shifts(2019020001)