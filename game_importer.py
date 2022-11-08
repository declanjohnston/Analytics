# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 17:40:29 2020

To be run daily, automatically imports yesterdays pbp data and saves them in a new folder summarized in csvs

@author: decla
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import hockey_scraper
from datetime import date, timedelta
import csv
import GLOBAL


def scrape_day(date):
    # Scrape data
    hockey_scraper.scrape_date_range(date, date, True, docs_dir="./data/raw")


def league_year(date):
    return 2021

# Read and process data


def process_day(date):
    raw_path = "./data/raw/csvs/" + "nhl_pbp_" + date + "--" + date + ".csv"
    path = "./data/processed_games/" + yesterday
    if not os.path.exists(path):
        os.makedirs(path)

    data = []
    with open(raw_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data.append(row)

    # Remove description since it contains commas
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
            writer = csv.writer(file, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_NONE, lineterminator='\n')
            writer.writerow(data[0])
            for row in game:
                writer.writerow(row)
        shift_importer.import_shifts(game[0][1], league_year(date))


# Generate date and create path if necessary
yesterday = date.today() - timedelta(days=10)
yesterday = yesterday.strftime("%Y-%m-%d")

scrape_day(yesterday)
process_day(yesterday)
