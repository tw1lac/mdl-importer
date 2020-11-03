class Material(object):
	FLAGS = {"ConstantColor": 2**0, "SortPrimitivesNearZ": 2**3, "SortPrimitivesFarZ": 2**4, "FullResolution": 2**5}
	def __init__(self):
		self.layers = []
		self.flags = 0