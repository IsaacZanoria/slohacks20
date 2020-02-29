import wget
import requests
import os

api = "https://ws-public.interpol.int/notices/v1/yellow?resultPerPage=100&page="

#dictionary = requests.get(api + "1").json()
#print(dictionary)
#num_items = dictionary["total"]
num_items = 1500
#for i in dictionary["_embedded"]["notices"][:num_items]:
#	name = i["name"]
#	images = i["_links"]["images"]["href"]
#	dictionary = requests.get(images).json()
#	if len(dictionary["_embedded"]["images"]) > 0:
#		img = dictionary["_embedded"]["images"][0]["_links"]["self"]["href"]
#		wget.download(img, "images/{}.png".format(name))

for j in range(1, num_items // 100):
    os.mkdir("images/page %i" % j)
    dictionary = requests.get(api + str(j)).json()
    for i in dictionary["_embedded"]["notices"]:
        name = i["entity_id"].replace("/", "-")
        images = i["_links"]["images"]["href"]
        dictionary = requests.get(images).json()
        if len(dictionary["_embedded"]["images"]) > 0:
            img = dictionary["_embedded"]["images"][0]["_links"]["self"]["href"]
            print(img)
            wget.download(img, "images/page %i/%s.png" % (j, name))

