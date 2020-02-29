import wget
import requests

api = "https://ws-public.interpol.int/notices/v1/yellow?resultPerPage=100&page="

dictionary = requests.get(api + "1").json()
#num_items = dictionary["total"]
num_items = 25
for i in dictionary["_embedded"]["notices"][:num_items]:
	try:
		name = i["name"]
		img = i["_links"]["thumbnail"]["href"]
		wget.download(img, "images/{}.png".format(name))
	except KeyError:
		pass

for i in range(2, num_items // 100 + 1):
	dictionary = requests.get(api + str(i)).json()
	for i in dictionary["_embedded"]["notices"]:
		try:
			name = i["name"]
			img = i["_links"]["thumbnail"]["href"]
			wget.download(img, "images/{}.png".format(name))
		except:
			pass
