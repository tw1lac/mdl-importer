from .utils import bracket_remover
from .Geoset import Geoset
from .Parser import Parser


class GeosetParser(Parser):
	def __init__(self, file):
		self.tokens = ["Vertices", "Normals", "TVertices", "Faces", "MaterialID", "Groups", "VertexGroup"]
		super(GeosetParser, self).__init__(file)

	def parse(self, context):
		geoset = Geoset()
		bracket_count = 1

		line = self.file.readline().strip()
		bracket_count = self.count_brackets(bracket_count, line)

		while bracket_count > 0:
			label, *data = line.split(" ")

			if label in self.tokens:
				if label == "MaterialID":
					geoset.material_id = int(data[0].replace(",", ""))

				elif label == "VertexGroup":
					line, bracket_count = self.read(bracket_count)

					while bracket_count > 1:
						line = line.replace(",", "").strip()
						geoset.vertexGroup.append(line)
						line, bracket_count = self.read(bracket_count)

				elif label == "Groups":
					line, bracket_count = self.read(bracket_count)

					while "Matrices" in line:
						line = bracket_remover(line)
						data2 = line.replace("Matrices", "").strip().split(" ")
						group_points = []
						[group_points.append(int(v)) for v in data2]
						geoset.groups.append(group_points)
						line, bracket_count = self.read(bracket_count)

				elif label == "Vertices":
					line, bracket_count = self.read(bracket_count)

					while bracket_count > 1:
						line = bracket_remover(line)
						data2 = line.strip().split(" ")
						vert_points = []
						[vert_points.append(float(v) / 20.0) for v in data2]
						geoset.vertices.append(vert_points)
						line, bracket_count = self.read(bracket_count)

				elif label == "Normals":
					line, bracket_count = self.read(bracket_count)

					while bracket_count > 1:
						line = bracket_remover(line)
						data2 = line.strip().split(" ")
						normal_points = []
						[normal_points.append(float(v)) for v in data2]
						geoset.normals.append(normal_points)
						line, bracket_count = self.read(bracket_count)

				elif label == "Faces":
					line, bracket_count = self.read(bracket_count)
					label, *data = line.split(" ")

					if label == "Triangles":
						line, bracket_count = self.read(bracket_count)

						while bracket_count > 2:
							line = bracket_remover(line)
							data2 = line.strip().split(" ")

							if data2[0] != '':
								if len(data2) > 3:
									for i in range(len(data2)//3):
										face_points = []
										[face_points.append(int(v)) for v in data2[i*3:i*3+3]]
										geoset.faces.append(face_points)
								else:
									face_points = []
									[face_points.append(int(v)) for v in data2]
									geoset.faces.append(face_points)
							line, bracket_count = self.read(bracket_count)

				elif label == "TVertices":
					line, bracket_count = self.read(bracket_count)

					while bracket_count > 1:
						line = bracket_remover(line)
						data2 = line.strip().split(" ")
						t_vert_points = []
						[t_vert_points.append(float(v) / 20.0) for v in data2]
						geoset.uvs.append(t_vert_points)
						line, bracket_count = self.read(bracket_count)

			line = self.file.readline().strip()
			bracket_count = self.count_brackets(bracket_count, line)

		return geoset
