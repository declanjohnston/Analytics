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
import gzip

def import_shifts(game_id, year):
    #do stuff
    path = "./data/raw/docs/" + str(year) + "/json_shifts/" + str(year*10) + str(game_id) + ".txt.gz"
    with gzip.open(path) as json_file:
        data = json.load(json_file)
        data = data['data']
        temp = []
        first_shift = data.pop(0)
        while(first_shift['detailCode'] != 0):
            first_shift = data.pop(0)
        player_id = first_shift['playerId']
        temp.append(first_shift)
        for shift in data:
            #print(shift['lastName'])
            if shift['detailCode'] == 0:
                new_player_id = shift['playerId']
                if new_player_id != player_id:
                    player_id_path = "./data/players/shifts/" + str(player_id) + ".json"
                    if os.path.exists(player_id_path):
                        with open(player_id_path, mode='r') as file:
                            data = json.load(file)
                        data.append(temp)    
                    else:
                        data = temp
                    with open(player_id_path, mode='w') as file:
                       json.dump(data, file)
                    temp = []
                    player_id = new_player_id
                temp.append(shift)

