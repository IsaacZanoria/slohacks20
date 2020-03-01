from selenium import webdriver
import time
from bs4 import BeautifulSoup

img_links = []

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome()

end = 1000
start = 500
for i in range(start, end):
    driver.get("https://www.namus.gov/MissingPersons/Case#/{}/attachments".format(i))
    time.sleep(1)
#more_buttons = driver.find_elements_by_class_name("moreLink")
#for x in range(len(more_buttons)):
  #if more_buttons[x].is_displayed():
      #driver.execute_script("arguments[0].click();", more_buttons[x])
      #time.sleep(1)
    page_source = driver.page_source
    time.sleep(1)

#driver.find_element_by_class_name('icon-download').click()

    soup = BeautifulSoup(page_source, 'lxml')
    try:
        s = soup.find('img', alt="Case Photo")['src']
        img_links.append(s)
        print(s)
    except TypeError:
        print("skip")
    
    

#import numpy
#a = numpy.asarray(img_links)
#numpy.savetxt("img_links_0_500.csv", a, fmt = "%.183", delimiter=",")

import pandas as pd 
pd.DataFrame(img_links).to_csv("img_links_500_1000.csv")
