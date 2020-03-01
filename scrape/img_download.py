# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 19:49:40 2020

@author: rjsta
"""

import wget
import csv

results = []
with open("img_links_0_500.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # each row is a list
        results.append(row)