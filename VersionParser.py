from .Parser import Parser


class VersionParser(Parser):
	def parse(self, context):
		label, version = self.file.readline().replace(",", "").split(" ")
		if int(version) != 800:
			raise Exception("MDL file version not supported")
