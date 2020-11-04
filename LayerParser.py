from .Layer import Layer
from .MaterialAlpha import MaterialAlpha
from .Parser import Parser


class LayerParser(Parser):
	def __init__(self, file):
		self.tokens = [
			"FilterMode", "Unshaded", "SphereEnvironmentMap",
			"TwoSided", "Unfogged", "NoDepthTest", "NoDepthSet",
			"TextureID", "Alpha", "Linear"
		]
		super(LayerParser, self).__init__(file)

	def parse(self, context):
		layer = Layer()
		pars = 1

		line, pars = self.read(pars)

		while pars > 0:
			label, *data = line.split(" ")

			if label == "static":
				label = data[0]
				data = data[1:]

			if label in self.tokens:
				if label in Layer.SHADING_FLAGS:
					layer.shading_flags |= Layer.SHADING_FLAGS[label]

				elif label == "FilterMode":
					if data[0] in Layer.FILTER_MODES:
						layer.filter_mode = data[0]
					else:
						raise Exception("Unknown FilterMode: '%s'" % data[0])

				elif label == "Alpha":
					if len(data) > 1:
						layer.material_alpha = MaterialAlpha()

						line, pars = self.read(pars)

						while pars > 1:
							label, *data = line.replace(":", "").strip().split(" ")

							if label in ["Linear", "Hermite", "Bezier", "DontInterp"]:
								layer.material_alpha.interpolation_type = label
							else:
								layer.material_alpha.tracks[label] = data[0]

							line, pars = self.read(pars)
					else:
						layer.alpha = data[0]

				elif label == "TextureID":
					layer.texture_id = int(data[0])
			else:
				raise Exception("Unknown data in layer: %s %s" % (label, data))

			line, pars = self.read(pars)

		return layer