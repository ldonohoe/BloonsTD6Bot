


class MapResult():
	
	def __init__(self, mapName, difficulty):
		self.mapName = mapName
		self.difficulty = difficulty
		self.result = ''
		self.cause = None
		self.time = 0

	def reportResults(self):
		outStr = f'{self.result} {self.difficulty} on map: {self.mapName} in'
		minutes = int(self.time // 60)
		seconds = int(self.time % 60)
		outStr = f'{outStr} {minutes}:{seconds}'
		if self.cause is not None:
			outStr = f'{outStr} due to {self.cause}'

		return outStr