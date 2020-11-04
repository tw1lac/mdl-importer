from .utils import bracket_remover
from .Anim import Anim
from .Parser import Parser


class SequencesParser(Parser):
	def __init__(self, file):
		super(SequencesParser, self).__init__(file)

	def parse(self, context, count):
		anims = []
		bracket_count = 1

		line, bracket_count = self.read(bracket_count)
		while bracket_count > 0:
			if line.find("Anim") >= 0:
				anim = Anim()
				anim.name = bracket_remover(line.replace("Anim", ""))

				line, bracket_count = self.read(bracket_count)
				while bracket_count > 1:
					line = bracket_remover(line)
					if line.find("Interval") >= 0:
						frames = line.replace("Interval", "").strip().split(" ")
						anim.start = frames[0]
						anim.end = frames[1]

					elif line.find("NonLooping") >= 0:
						anim.loop = False

					elif line.find("MinimumExtent") >= 0:
						[anim.min.append(float(v)) for v in line.replace("MinimumExtent", "").strip().split(" ")]

					elif line.find("MaximumExtent") >= 0:
						[anim.max.append(float(v)) for v in line.replace("MaximumExtent", "").strip().split(" ")]

					elif line.find("BoundsRadius") >= 0:
						anim.radius = float(line.replace("BoundsRadius", "").strip())

					line, bracket_count = self.read(bracket_count)

				anims.append(anim)

			line, bracket_count = self.read(bracket_count)

		#prn_list(anims)

		return anims