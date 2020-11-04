from .BoneParser import BoneParser
from .GeosetParser import GeosetParser
from .Model import Model
from .MaterialParser import MaterialParser
from .Parser import Parser
from .PivotPointsParser import PivotPointsParser
from .SequencesParser import SequencesParser
from .TextureParser import TextureParser
from .VersionParser import VersionParser


class MDLParser(Parser):
	def __init__(self, file):
		self.tokens = {
			"Version": VersionParser(file),
			"Model": None,  # We only care about the model's name right now
			"Geoset": GeosetParser(file),
			"Textures": TextureParser(file),
			"Materials": MaterialParser(file),
			"Sequences": SequencesParser(file),
			#"GlobalSequences",
			#"GeosetAnim",
			"Bone": BoneParser(file),
			#"Helper",
			#"Attachment",
			"PivotPoints" : PivotPointsParser(file)
		}
		super(MDLParser, self).__init__(file)

	def parse(self, context):
		model = Model()
		line = self.file.readline()
		while(line):
			label, *data = line.split(" ")

			if label not in self.tokens:
				line = self.file.readline()
				continue

			if label == "Model":
				model.name = data[0].replace('"', "")
			elif label == "Geoset":
				model.geosets.append(self.tokens[label].parse(context))
			elif label == "Version":
				self.tokens["Version"].parse(context)
			elif label == "Textures":
				model.textures = self.tokens[label].parse(context, int(data[0]))
			elif label == "Materials":
				model.materials = self.tokens[label].parse(context, int(data[0]))
			elif label == "Bone":
				model.bones.append(self.tokens[label].parse(context, data[0]))
			elif label == "Sequences":
				model.anims = self.tokens[label].parse(context, data[0])
			elif label == "PivotPoints":
				model.pivots = self.tokens[label].parse(context, data[0])

			line = self.file.readline()

		return model
