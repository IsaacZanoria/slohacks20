import wget
import requests

api = "https://ws-public.interpol.int/notices/v1/yellow?resultPerPage=100&page="

dictionary = requests.get(api + "1").json()
#num_items = dictionary["total"]
num_items = 25
for i in dictionary["_embedded"]["notices"][:num_items]:
	name = i["name"]
	images = i["_links"]["images"]["href"]
	dictionary = requests.get(images).json()
	if len(dictionary["_embedded"]["images"]) > 0:
		img = dictionary["_embedded"]["images"][0]["_links"]["self"]["href"]
		wget.download(img, "images/{}.png".format(name))

for i in range(2, num_items // 100 + 1):
	dictionary = requests.get(api + str(i)).json()
	for i in dictionary["_embedded"]["notices"]:
		name = i["name"]
		images = i["_links"]["images"]["href"]
		dictionary = requests.get(images).json()
		img = dictionary["_embedded"]["images"][0]["_links"]["self"]["href"]
		wget.download(img, "images/{}.png".format(name))
