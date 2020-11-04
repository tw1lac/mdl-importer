from .Anim import Anim
from .Parser import Parser


class SequencesParser(Parser):
	def __init__(self, file):
		super(SequencesParser, self).__init__(file)

	def parse(self, context, count):
		anims = []
		pars = 1
		line, pars = self.read2(pars)
		#print("1 line=%s pars=%d " % (line, pars))
		while(pars > 0):
			if(line.find("Anim") >= 0):
				anim = Anim()
				anim.name = line.replace("Anim", "").replace("{", "").replace("}", "").replace(",", "").strip()
				line, pars = self.read2(pars)
				#print("2 line=%s pars=%d " % (line, pars))
				while(pars > 1):
					if(line.find("Interval") >= 0):
						frames = line.replace("Interval", "").replace("{", "").replace("}", "").replace(",", "").strip().split(" ")
						anim.start = frames[0]
						anim.end = frames[1]
					elif line.find("NonLooping") >= 0 :
						anim.loop = False
					elif line.find("MinimumExtent") >= 0 :
						[anim.min.append(float(v)) for v in line.replace("MinimumExtent", "").replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]
					elif line.find("MaximumExtent") >= 0 :
						[anim.max.append(float(v)) for v in line.replace("MaximumExtent", "").replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]
					elif line.find("BoundsRadius") >= 0 :
						anim.radius = float(line.replace("BoundsRadius", "").replace("{", "").replace("}", "").replace(",", "").strip())
					line, pars = self.read2(pars)
				#Add it!!!
				anims.append(anim)

			line, pars = self.read2(pars)

		#prn_list(anims)

		return anims