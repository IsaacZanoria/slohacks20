import wget
import requests
import os
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver

#api = "https://ws-public.interpol.int/notices/v1/yellow?resultPerPage=100&page="
#api = "https://www.namus.gov//MissingPersons/Case#/" #add index at the of link
api = r"https://public.opendatasoft.com/api/records/1.0/search/?dataset=namus-missings&rows=50&facet=cityoflastcontact&facet=countydisplaynameoflastcontact&facet=raceethnicity&facet=statedisplaynameoflastcontact&facet=gender"

#dictionary = requests.get(api + "1").json()
#print(dictionary)
#num_items = dictionary["total"]
#num_items = 100
#for i in dictionary["_embedded"]["notices"][:num_items]:
#	name = i["name"]
#	images = i["_links"]["images"]["href"]
#	dictionary = requests.get(images).json()
#	if len(dictionary["_embedded"]["images"]) > 0:
#		img = dictionary["_embedded"]["images"][0]["_links"]["self"]["href"]
#		wget.download(img, "images/{}.png".format(name))

os.mkdir("images/page %i" % j)
ictionary = requests.get(api).json()
    for i in dictionary["_embedded"]["notices"]:
        name = i["entity_id"].replace("/", "-")
        images = i["_links"]["images"]["href"]
        dictionary = requests.get(images).json()
        if len(dictionary["_embedded"]["images"]) > 0:
            img = dictionary["_embedded"]["images"][0]["_links"]["self"]["href"]
            print(img)
            wget.download(img, "images/page %i/%s.png" % (j, name))


#for i in range(1, 10045):
#    api_request_format = r"https://public.opendatasoft.com/api/records/1.0/search/?dataset=namus-missings&namus2number=%i&rows=1"
#attachments_page_format = r"https://www.namus.gov//MissingPersons/Case#/%i/attachments"

id = 10044
req = requests.get(r"https://www.namus.gov/MissingPersons/Case#/10044/attachments")
soup = BeautifulSoup(req.content, features="lxml")
#returns = soup.find("div", attrs={'href': requests.compile("^http://")})["href"]
returns = soup.find("a", {"target": "_blank"})
#for ret in returns:
#    print(ret["src"])
print(returns)


#driver = webdriver.PhantomJS()
#driver.get(r"https://www.namus.gov//MissingPersons/Case#/%i/attachments" % id)
#p_element = driver.find_element_by_id(id_='a')
#print(p_element.text)