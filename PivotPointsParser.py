from .Parser import Parser
from .PivotPoint import PivotPoint


class PivotPointsParser(Parser):
	def __init__(self, file):
		super(PivotPointsParser, self).__init__(file)

	def parse(self, context, count):
		pps = []
		pars = 1
		#index = 0
		line, pars = self.read2(pars)
		print("count = %d \n" % int(count) )
		while(pars > 0):
			pp = PivotPoint()
			#print("line=%s" % line)
			[pp.pos.append(float(v) / 20.0) for v in line.replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]
			#print("PivotPointsParser %f %f %f\n" % (float(pp.pos[1]), float(pp.pos[2]), float(pp.pos[3])))
			pps.append(pp)
			#index = index + 1
			#print("================")
			line, pars = self.read2(pars)

		#print(pps[0].pos[1])
		return pps