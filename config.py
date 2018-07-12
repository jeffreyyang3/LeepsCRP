import random


data = [
	# 1 will be auction 1 price cap 1, 2 will be auction 1 participation
	# 3 will be auc 2 price cap 2 and 4 will be auction 3 ref price 1
	# 5 will be auc 4 ref price 2
	[
		{"priceBase": 200, "end": 200, "variance": [1, 3, 5, 8, 12, 15], "qualityBase": 100, "noise": 10, "allowedMarkup": 1.4, "mode": 4},
		{"priceBase": 200, "end": 200, "variance": [1, 3, 5, 8, 12, 15], "qualityBase": 100, "noise": 10, "allowedMarkup": 1.4, "mode": 1},
		{"priceBase": 200, "end": 200, "variance": [1, 3, 5, 8, 12, 15], "qualityBase": 100, "noise": 10, "allowedMarkup": 1.4, "mode": 3},
	]
]


def shuffle(data):
	return [random.sample(data[0], k=len(data[0]))]

def export_data():
	return shuffle(data)
