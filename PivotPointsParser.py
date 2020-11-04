from .utils import bracket_remover
from .Parser import Parser
from .PivotPoint import PivotPoint


class PivotPointsParser(Parser):
	def __init__(self, file):
		super(PivotPointsParser, self).__init__(file)

	def parse(self, context, count):
		pivot_points = []
		bracket_count = 1

		line, bracket_count = self.read(bracket_count)
		while bracket_count > 0:
			pivot_point = PivotPoint()
			[pivot_point.pos.append(float(v) / 20.0) for v in bracket_remover(line).split(" ")]
			pivot_points.append(pivot_point)
			line, bracket_count = self.read(bracket_count)

		return pivot_points
