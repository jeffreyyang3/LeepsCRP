import random

data = [
	[
		{"priceBase": 200, "end": 400, "variance": 50, "qualityBase": 100, "noise": 10}


	]




]

def shuffle(data):
	return [random.sample(data[0], k=len(data[0]))]

def export_data():
	return shuffle(data)