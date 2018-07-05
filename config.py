import random

data = [
	[
		{"priceBase": 200, "end": 4000, "variance": [1,3,8,12], "qualityBase": 100, "noise": 10, "allowedMarkup": 1.4}


	]




]

def shuffle(data):
	return [random.sample(data[0], k=len(data[0]))]

def export_data():
	return shuffle(data)