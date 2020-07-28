# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:41:25 2020

@author: decla
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import csv
import GLOBAL

def is_5v5(event):
    if event[GLOBAL.STRENGTH_INDEX] == "5x5" and event[49] != "" and event[51] != "":
        return True
    if event[GLOBAL.STRENGTH_INDEX] == "4x5" and event[49] == "":
        return True
    if event[GLOBAL.STRENGTH_INDEX] == "5x4" and event[51] == "":
        return True
    return False