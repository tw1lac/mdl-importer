class Parser(object):
	def __init__(self, file):
		self.file = file

	def parse(self, context):
		pass

	def count_brackets(self, bracket_count, line):
		# line.strip('\n')
		# if line.endswith("{"):
		# 	bracket_count += 1
		# elif line.endswith("}"):
		# 	bracket_count -= 1
		start_brackets = line.count('{')
		end_brackets = line.count('}')
		bracket_count += start_brackets
		bracket_count -= end_brackets
		return bracket_count

	def read(self, bracket_count):
		line = self.file.readline().replace(",", "").strip()
		bracket_count = self.count_brackets(bracket_count, line)
		return line, bracket_count

	def count_brackets2(self, bracket_count, line):
		line.strip('\n')
		if line.find("{") > -1 and line.find("}") > -1:
			#ignore such { }
			return bracket_count
		if line.endswith("{"):
			bracket_count += 1
		elif line.endswith("}"):
			bracket_count -= 1
		return bracket_count

	def read2(self, bracket_count):
		line = self.file.readline().replace(",", "").strip()
		bracket_count = self.count_brackets2(bracket_count, line)
		return line, bracket_count