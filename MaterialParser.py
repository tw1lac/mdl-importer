from .LayerParser import LayerParser
from .Material import Material
from .Parser import Parser


class MaterialParser(Parser):
	def __init__(self, file):
		self.layer_parser = LayerParser(file)
		super(MaterialParser, self).__init__(file)

	def parse(self, context, count):
		materials = []
		bracket_count = 1

		line, bracket_count = self.read(bracket_count)

		for _ in range(count):
			label, *data = line.split(" ")

			if label == "Material":
				material = Material()
				materials.append(material)

				line, bracket_count = self.read(bracket_count)

				while bracket_count > 1:
					label, *data = line.split(" ")

					if label == "Layer":
						material.layers.append(self.layer_parser.parse(context))
						bracket_count -= 1
					elif label in Material.FLAGS:
						material.flags |= Material.FLAGS[label]
					else:
						raise Exception("Unknown data in material: %s %s" % (label, data))

					line, bracket_count = self.read(bracket_count)

			line, bracket_count = self.read(bracket_count)

		return materials
