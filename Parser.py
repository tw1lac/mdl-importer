class Parser(object):
	def __init__(self, file):
		self.file = file

	def parse(self, context):
		pass

	def check_pars(self, pars, line):
		line.strip('\n')
		if line.endswith("{"):
			pars += 1
		elif line.endswith("}"):
			pars -= 1
		return pars

	def read(self, pars):
		line = self.file.readline().replace(",", "").strip()
		pars = self.check_pars(pars, line)
		return line, pars

	def check_pars2(self, pars, line):
		line.strip('\n')
		if line.find("{") > -1 and line.find("}") > -1:
			#ignore such { }
			return pars
		if line.endswith("{"):
			pars += 1
		elif line.endswith("}"):
			pars -= 1
		return pars

	def read2(self, pars):
		line = self.file.readline().replace(",", "").strip()
		pars = self.check_pars2(pars, line)
		return line, pars