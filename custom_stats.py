# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 22:09:04 2020

@author: decla
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import csv
import GLOBAL

# Shot for: +1
# Shot against -1
# Shot by: +3
# Goal for: +5
# Goal against -5
# Goal bu: +10
# Penalty taken: -5
# Penalty drawn: +5
# Block: +1 (+2 for block, -1 for shot)


def johnston_number(player_id, events):
    num = 0
    for event in events:
        # if GOAL
        if event[GLOBAL.EVENT_INDEX] == "GOAL" and event[GLOBAL.PERIOD_INDEX] != str(5) and event[GLOBAL.STRENGTH_INDEX] == "5x5":
            # if goal scored by
            if event[GLOBAL.P1_ID_INDEX] == player_id+".0":
                num = num + 100
            elif event[GLOBAL.P2_ID_INDEX] == player_id+".0" or event[GLOBAL.P3_ID_INDEX] == player_id+".0":
                num = num + 40
            elif event[GLOBAL.EVENT_TEAM_INDEX] == player_stats.team(player_id, event):
                num = num + 20
            else:
                num = num - 40

        # if shot
        if (event[GLOBAL.EVENT_INDEX] == "SHOT" or event[GLOBAL.EVENT_INDEX] == "MISS") and event[GLOBAL.PERIOD_INDEX] != str(5) and event[GLOBAL.STRENGTH_INDEX] == "5x5":

            if event[GLOBAL.P1_ID_INDEX] == player_id+".0":
                num = num + 10
            elif event[GLOBAL.EVENT_TEAM_INDEX] == player_stats.team(player_id, event):
                num = num + 2
            else:
                num = num - 4

        # if block
        if event[GLOBAL.EVENT_INDEX] == "BLOCK" and event[GLOBAL.PERIOD_INDEX] != str(5) and event[GLOBAL.STRENGTH_INDEX] == "5x5":
            # blocked by player
            if event[GLOBAL.P1_ID_INDEX] == player_id+".0":
                num = num + 10
            # just a shot
            elif event[GLOBAL.P2_ID_INDEX] == player_id+".0":
                num = num + 10
            elif event[GLOBAL.EVENT_TEAM_INDEX] == player_stats.team(player_id, event):
                num = num + 2
            else:
                num = num - 4

        if event[GLOBAL.EVENT_INDEX] == "PENL" and event[GLOBAL.PERIOD_INDEX] != str(5) and event[GLOBAL.STRENGTH_INDEX] == "5x5":
            if event[GLOBAL.P1_ID_INDEX] == player_id+".0":
                num = num - 20
            elif event[GLOBAL.P2_ID_INDEX] == player_id+".0":
                num = num + 20

    return num


def rank_by_johnston_num():
    path = "C:/Users/decla/Documents/Analytics/data/players/"
    files = os.listdir(path)
    files.pop(-1)
    ranked_list = []
    for player_id in files:
        events = []
        player_id = player_id.replace('.csv', '')
        with open("C:/Users/decla/Documents/Analytics/data/players/" + player_id + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                events.append(row)
        events.pop(0)
        if events[1][GLOBAL.HOME_GOALIE_ID_INDEX] != player_id+".0" and events[1][GLOBAL.AWAY_GOALIE_ID_INDEX] != player_id+".0":
            ranked_list.append([player_stats.name_from_id(str(player_id)),
                               player_id, johnston_number(player_id, events)])

    ranked_list.sort(key=lambda tup: tup[2])
    return ranked_list
