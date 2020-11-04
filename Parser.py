class Parser(object):
	def __init__(self, file):
		self.file = file

	def parse(self, context):
		pass

	def count_brackets(self, bracket_count, line):
		start_brackets = line.count('{')
		end_brackets = line.count('}')
		bracket_count += start_brackets
		bracket_count -= end_brackets
		return bracket_count

	def read(self, bracket_count):
		line = self.file.readline().replace(",", "").strip()
		bracket_count = self.count_brackets(bracket_count, line)
		return line, bracket_count
