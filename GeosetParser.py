from Geoset import Geoset
from Parser import Parser


class GeosetParser(Parser):
	def __init__(self, file):
		self.tokens = ["Vertices", "Normals", "TVertices", "Faces", "MaterialID", "Groups", "VertexGroup"]
		super(GeosetParser, self).__init__(file)

	def parse(self, context):
		geoset = Geoset()
		pars = 1

		line = self.file.readline().strip()
		pars = self.check_pars(pars, line)

		while pars > 0:
			label, *data = line.split(" ")

			if label in self.tokens:
				if label == "MaterialID":
					geoset.material_id = int(data[0].replace(",", ""))
				#=============================BEGIN=====================================
				elif label == "VertexGroup":
					line, pars = self.read(pars)
					while pars > 1:
						line = line.replace(",", "").strip()
						geoset.vertexGroup.append(line)
						#print("geoset.vertexGroup.append %s \n" % line)
						line, pars = self.read(pars)
				elif label == "Groups":
					#read next
					line, pars = self.read2(pars)
					#Matrices { 3 4 }
					line = line.replace("{", "").replace("}", "").strip()
					#Matrices  3 4
					#label2, *data = line.split(" ")
					while line.find("Matrices") >= 0:
						data2 = line.replace("Matrices", "").strip().split(" ")
						gps = []
						[gps.append(int(v)) for v in data2]
						geoset.groups.append(gps)
						line, pars = self.read2(pars)
						line = line.replace("{", "").replace("}", "").strip()
					#prn_list2(geoset.groups)
				#=============================E N D=====================================
				elif label in ["Vertices", "Normals", "Faces", "TVertices"]:

					if label == "Vertices":
						for _ in range(int(data[0])):
							[geoset.vertices.append(float(v) / 20.0)  for v in self.file.readline().replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]

					elif label == "Normals":
						for _ in range(int(data[0])):
							[geoset.normals.append(float(v)) for v in self.file.readline().replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]

					elif label == "Faces":
						line, pars = self.read(pars)
						[geoset.faces.append(int(v)) for v in self.file.readline().replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]
						line, pars = self.read(pars)

					elif label == "TVertices":
						for _ in range(int(data[0])):
							geoset.uvs.append([float(v) for v in self.file.readline().replace("{", "").replace("}", "").replace(",", "").strip().split(" ")])

			line = self.file.readline().strip()
			pars = self.check_pars(pars, line)

		return geoset