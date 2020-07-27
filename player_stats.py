# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:34:34 2020

@author: decla
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import csv
import event_info
import custom_stats
READ_MODE = 'r'

def team(player_id,event):
    if event[30] == player_id+".0" or event[22] == player_id+".0" or event[24] == player_id+".0" or event[26] == player_id+".0" or event[28] == player_id+".0" or event[32] == player_id+".0":
        players_team = event[13]
    else:
        players_team = event[14]
    return players_team


def goals(player_id,events):
    goals = 0
    for event in events:
        if event[4] == "GOAL" and event[16] == player_id+".0" and event[3] != str(5):
            goals = goals+1
    return goals
    
def assists(player_id,events):
    assists = 0
    for event in events:
        if event[4] == "GOAL" and (event[18]== player_id+".0" or event[20]== player_id+".0" ):
            assists = assists+1
    return assists

def cf(player_id,events):

    filtered_events = list(filter(lambda x: (((x[4] == "SHOT") or (x[4] == "MISS") or (x[4] =="BLOCK") or (x[4] =="GOAL")) and x[11] == team(player_id,x) and x[3] != str(5) and event_info.is_5v5(x)), events))
    cf = len(filtered_events)
    return cf

def ca(player_id,events):

    filtered_events = list(filter(lambda x: (((x[4] == "SHOT") or (x[4] == "MISS") or (x[4] =="BLOCK") or (x[4] =="GOAL")) and x[11] != team(player_id,x) and x[3] != str(5) and event_info.is_5v5(x)), events))
    cf = len(filtered_events)
    return cf

def cfp(player_id,events):
    CF = cf(player_id, events)
    CA = ca(player_id, events)
    return CF/(CF+CA)

def gf(player_id, events):
        
    filtered_events = list(filter(lambda x: (x[4] == "GOAL" and x[11] == team(player_id,x) and x[3] != str(5) ), events))
    return GF

def ga(player_id, events):

    filtered_events = list(filter(lambda x: (x[4] == "GOAL" and x[11] != team(player_id,x) and x[3] != str(5) ), events))
    return len(filtered_events)

def pm(player_id, events):
    return gf(player_id, events) - ga(player_id, events) ## not working, need to handle PP and EN situations


def points(player_id,events):
    return goals(player_id, events) +assists(player_id, events)

def lookup_id(player_id, stats_request):
    switcher = {"GOALS" : goals,
                "ASSISTS" : assists,
                "POINTS" : points,
                "CF" : cf,
                "CA" : ca,
                "CF%" : cfp,
                "GF" : gf,
                "GA" : ga,
                "PM" : pm,
                "JOHNSTON NUMBER" : custom_stats.johnston_number}
    events = []
    with open("C:/Users/decla/Documents/Analytics/data/players/" + player_id +".csv") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            events.append(row)
    events.pop(0)
    stats = []
    for stat in stats_request:
        stat = stat.upper()
        stats.append(switcher.get(stat)(player_id,events))
    print(stats)    
      
        
def lookup_name(name, stats):
    #lookup player id in player_lookup.csv
    with open("C:/Users/decla/Documents/Analytics/data/players/player_lookup.csv") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        name  = name.upper()
        for row in csv_reader:
            if row[1] == name:
                print(row[0])
                lookup_id(row[0],stats)
                return
    print("Player not found")