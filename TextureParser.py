from .Parser import Parser
from .Texture import Texture


class TextureParser(Parser):
	def parse(self, context, count):
		textures = []
		bracket_count = 1

		line, bracket_count = self.read(bracket_count)

		for _ in range(count):
			label, *data = line.split(" ")

			if label == "Bitmap":
				texture = Texture()
				textures.append(texture)

				line, bracket_count = self.read(bracket_count)
				while bracket_count > 1:
					try:
						label, data = line.split(" ")
					except:
						label = line
						data = ""

					if label == "Image" and data:
						texture.filepath = data.replace('"', "").replace("blp", "png")

					elif label == "ReplaceableId":
						texture.replaceable_id = int(data)

					else:
						print("Unknown data in texture: %s %s" % (label, data))
						# raise Exception("Unknown data in texture: %s %s" % (label, data))

					line, bracket_count = self.read(bracket_count)

				if texture.replaceable_id == 2:
					texture.filepath = "ReplaceableTextures/TeamGlow/TeamGlow00.png"

			line, bracket_count = self.read(bracket_count)

		return textures
