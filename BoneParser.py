from .utils import bracket_remover
from .Bone import Bone
from .BoneData import BoneData
from .BoneDataData import BoneDataData
from .Parser import Parser


class BoneParser(Parser):
	def __init__(self, file):
		super(BoneParser, self).__init__(file)

	def parse(self, context, name):
		bone = Bone()
		bone.name = name.replace('"', "").strip()

		bracket_count = 1

		line, bracket_count = self.read(bracket_count)

		while bracket_count > 0:
			label, *data = line.split(" ")
			if label == "ObjectId":
				bone.objectId = int(data[0])
			if label == "Parent":
				bone.parent = int(data[0])
			# if label == "GeosetId":
				# print("GeosetId=%s " % data[0])
			if label in ["Scaling", "Rotation", "Translation"]:
				bdata = BoneData(label)
				bdata.size = int(data[0])

				line, bracket_count = self.read(bracket_count)
				bracket_count_start = bracket_count
				bdata.type = line  # Linear or Hermite

				line, bracket_count = self.read(bracket_count)

				while bracket_count >= bracket_count_start:
					if line.find(":") > -1:
						label, data = line.split(":")
						bonedata = BoneDataData()
						bonedata.time = int(label)

						if bdata.name == "Translation":
							self.data_appender(bonedata.val, data, 20)
						else:
							self.data_appender(bonedata.val, data)

						if bdata.type.find('Linear') == -1:  # not Linear
							self.data_appender(bonedata.inTan, self.file.readline().replace("InTan", ""))
							self.data_appender(bonedata.outTan, self.file.readline().replace("OutTan", ""))

						bdata.data.append(bonedata)
					else:
						label, *data = line.split(" ")
						if label == "GlobalSeqId":
							bdata.globalSeqId = int(data[0])

					line, bracket_count = self.read(bracket_count)
				bone.boneData.append(bdata)

			line, bracket_count = self.read(bracket_count)

		return bone

	def data_appender(self, data_receiver, data_string, div=1):
		[data_receiver.append(float(v)/div) for v in bracket_remover(data_string).split(" ")]
