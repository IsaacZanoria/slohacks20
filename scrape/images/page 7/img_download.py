# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 19:49:40 2020

@author: rjsta
"""

#url = "https://www.namus.gov/api/CaseSets/NamUs/MissingPersons/Cases/10044/Images/22606/Thumbnail"

import wget
import csv

results = []
with open("img_links_0_500.csv") as csvfile:
    reader = csv.reader(csvfile) # change contents to floats
    for row in reader: # each row is a list
        results.append(row[1])
        
        
for res in results:
    
    if res != "0":
        print("result %s" % res)
        #url = "https://www.namus.gov/api/CaseSets/NamUs/MissingPersons/Cases/10044/Images/22606/Thumbnail"
        url = r"https://www.namus.gov" + res[:-9] + "Original/"
        print(url.split(r"/"))
        output_filepath = url[ (url.find("/Cases/") + 7):url.find("/Images/") ] + ".png"
#        print(output_filepath)
        wget.download(url, output_filepath)