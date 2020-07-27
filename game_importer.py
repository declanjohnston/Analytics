# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 17:40:29 2020

@author: decla
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import hockey_scraper
from datetime import date, timedelta
import csv

#Generate date and create path if necessary
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")
path = "C:/Users/decla/Documents/Analytics/data/processed_games/" + yesterday
if not os.path.exists(path):
    os.makedirs(path)

#Scrape data
scraped_data = hockey_scraper.scrape_date_range(yesterday,yesterday, True, docs_dir="C:/Users/decla/Documents/Analytics/data/raw")

#Read and process data
raw_path = "C:/Users/decla/Documents/Analytics/data/raw/csvs/" + "nhl_pbp_" + yesterday + "--" + yesterday + ".csv"
data = []
with open(raw_path) as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    line_count = 0
    for row in csv_reader:
        data.append(row)
        
#Remove description since it contains commas
for event in data:
    event[5] = event[5].replace(',', '')
    
games = []
temp = []
game = int(data[1][1])
for row in data[1:-1]:
    if int(row[1]) != game:
        game = int(row[1])
        games.append(temp)
        temp = []
        temp.append(row)        
    else:
        temp.append(row)
games.append(temp)

for game in games:
    write_path = path + "/" + game[0][1] + ".csv"
    with open(write_path, mode='w') as file:
        writer = csv.writer(file,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator = '\n')
        writer.writerow(data[0])
        for row in game:
            writer.writerow(row)
            

        
    