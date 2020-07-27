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


# Shot for: +1
# Shot against -1
# Shot by: +3
# Goal for: +5
# Goal against -5
# Goal bu: +10
# Penalty taken: -5
# Penalty drawn: +5

def johnston_number(player_id,events):
    num = 0
    for event in events:
        #if GOAL
        if event[4] == "GOAL" and event[3] != str(5):
            #if goal scored by
            if event[16] == player_id+".0":
                num = num + 10
            
        
    return num
