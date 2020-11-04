from .Parser import Parser
from .Texture import Texture


class TextureParser(Parser):
	def parse(self, context, count):
		textures = []
		pars = 1

		line, pars = self.read(pars)

		for _ in range(count):
			label, *data = line.split(" ")

			if label == "Bitmap":
				texture = Texture()
				textures.append(texture)

				line, pas = self.read(pars)

				while pars > 1:
					label, data = line.split(" ")

					if label == "Image" and data:
						texture.filepath = data.replace('"', "").replace("blp", "png")
					elif label == "ReplaceableId":
						texture.replaceable_id = int(data)
					else:
						raise Exception("Unknown data in texture: %s %s" % (label, data))

					line, pars = self.read(pars)

				if texture.replaceable_id == 2:
					texture.filepath = "ReplaceableTextures/TeamGlow/TeamGlow00.png"

			line, pars = self.read(pars)

		return textures