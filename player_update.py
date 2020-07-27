# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:25:11 2020

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



def update_game(game_id, game_date): 
    player_indeces = [16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,50,52]
    game_path = "C:/Users/decla/Documents/Analytics/data/processed_games/" + game_date + "/"+ game_id 
    game_path.replace(".csv.csv",".csv")
    print(game_path)
    player_path = "C:/Users/decla/Documents/Analytics/data/players/"
    data = _ReadCsv(game_path)
    header = data.pop(0)
    player_ids = []
    event_log = []
    for event in data:
        for id_index in player_indeces:
            if event[id_index] != '':
                player_id = int(float(event[id_index]))
                if player_id in player_ids:
                    index = player_ids.index(player_id)
                    event_log[index].append(event)
                else:
                    player_ids.append(player_id)
                    index = len(player_ids)-1
                    event_log.append([])
                    event_log[index].append(event)
                
                
    for i in range(0,len(player_ids)):
        player = player_ids[i]
        log = event_log[i]
        flags = np.zeros(len(log))
        for j in range(0,len(log)-1):
            for k in range(j+1,len(log)):
                if log[k][0] == log[j][0]:
                    flags[k] = 1
        
        for a in range(len(log)-1,-1,-1):
            if flags[a] ==1:
                log.pop(a)
        
        player_id_path = player_path + str(player) + ".csv"
        if os.path.exists(player_id_path):
            exists = True
        else:
            exists = False
        with open(player_id_path, mode='a') as file:
            writer = csv.writer(file,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator = '\n')
            if exists == False:
                writer.writerow(header)
            for row in log:
                writer.writerow(row)

def update_day(date):
    path = "C:/Users/decla/Documents/Analytics/data/processed_games/" + date
    files = os.listdir(path)
    for game in files:
        update_game(game,date)
                    
def update_bulk():
    path = "C:/Users/decla/Documents/Analytics/data/processed_games/"
    files = os.listdir(path)
    for file in files:
        update_day(file)
        
def player_dictionary_generator():
    path = "C:/Users/decla/Documents/Analytics/data/players/"
    players = os.listdir(path)
    player_dict = {}
    for player in players:
        with open(path+player, mode='r') as file:
            csv_reader = csv.reader(file,delimiter=',')
            csv_reader.__next__()
            data = csv_reader.__next__()
        name = data[data.index(player.replace('.csv','')+".0")-1]
        player_dict[player.replace('.csv','')] = name
    with open(path+"player_lookup.csv",'w') as file:
        writer = csv.writer(file,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator = '\n')
        writer.writerow(["ID","Name"])
        for player in player_dict:
            data = [player,player_dict[player]]
            writer.writerow(data)