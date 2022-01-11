


class MapResult():
	
	def __init__(self, mapName, result, difficulty, cause=None):
		self.mapName = mapName
		self.result = result
		self.cause = cause
		self.difficulty = difficulty

	def reportResults(self):
		outStr = f''