import random

# Mode Keys
	#   1: Auction 1 Price Cap 1
	#   2: Auction 1.1 Price Cap with Participation
	# 	3: Auction 2 Price Cap 2
	#   4: Auction 3 Reference Price 1
	# 	5: Auction 4 Reference Price 2



"""
data = [
	[
		{"priceBase": 200, "end": 200, "variance": [1, 3, 5, 8, 12, 15], "mode": 4, "buy15pts": 2},
		{"priceBase": 200, "end": 200, "variance": [1, 3, 5, 8, 12, 15], "mode": 3, "buy15pts": 4},
		{"priceBase": 200, "end": 200, "variance": [1, 3, 5, 8, 12, 15], "mode": 1, "buy15pts": 2},
		{"priceBase": 200, "end": 200, "variance": [1, 3, 5, 8, 12, 15], "mode": 5, "buy15pts": 4},

	]
]
"""




data = [
	[
		{"priceBase": 200, "end": 200, "variance": [1, 3, 5, 8, 12, 15], "mode": 4, "buy15pts": 2},
	]
]




def shuffle(data):
	return [random.sample(data[0], k=len(data[0]))]

def export_data():
	return shuffle(data)
