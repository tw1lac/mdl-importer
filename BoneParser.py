from Bone import Bone
from BoneData import BoneData
from BoneDataData import BoneDataData
from Parser import Parser


class BoneParser(Parser):
	def __init__(self, file):
		super(BoneParser, self).__init__(file)

	def parse(self, context, name):
		#line.replace(":", "").strip().split(" ")
		bone = Bone()

		bone.name = name.replace('"', "").strip()

		#print("Begin parse for %s \n" % (bone.name))

		pars = 1

		line, pars = self.read2(pars)

		while(pars > 0):
			label, *data = line.split(" ")
			if label == "ObjectId":
				bone.objectId = int(data[0])
			if label == "Parent":
				bone.parent = int(data[0])
			#if label == "GeosetId":
			#	print("GeosetId=%s " % data[0])
			if label == "Scaling" or label == "Rotation" or label == "Translation":
				bdata = BoneData(label)
				bdata.size = int(data[0])
				#get type Scaling first!!!
				line, pars = self.read2(pars)
				bdata.type = line;#Linear or
				#record it
				scalpars = pars
				line, pars = self.read2(pars)

				dataindex = 0
				while(pars >= scalpars):
					if line.find(":") > -1:
						label, data = line.split(":")
						bonedata = BoneDataData()
						bonedata.time = int(label)
						if bdata.name == "Translation":
							#print("Find Translation!!!!!!!!!")
							[bonedata.val.append(float(v) / 20.0) for v in data.replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]
						else:
							[bonedata.val.append(float(v)) for v in data.replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]
						if(bdata.type.find('Linear') == -1):# not Linear
							[bonedata.inTan.append(float(v)) for v in self.file.readline().replace("{", "").replace("}", "").replace(",", "").replace("InTan", "").strip().split(" ")]
							[bonedata.outTan.append(float(v)) for v in self.file.readline().replace("{", "").replace("}", "").replace(",", "").replace("OutTan", "").strip().split(" ")]

						bdata.data.append(bonedata)
					else:
						label, *data = line.split(" ")
						if label == "GlobalSeqId":
							bdata.globalSeqId = int(data[0])

					line, pars = self.read2(pars)
				bone.boneData.append(bdata)

			line, pars = self.read2(pars)
		#print("===================================>")
		#prn_obj(bone)
		#prn_list(bone.boneData[0].data)
		#prn_list(bone.boneData[1].data)
		#print("<===================================")
		'''for _ in range(count):
			label, *data = line.split(" ")
			
			if label == "ObjectId":
				bone.ObjectId = (int)data[0]
			if label == "Scaling":
				material = Material()
				materials.append(material)
				
				line, pars = self.read(pars)
				
				while pars > 1:
					label, *data = line.split(" ")
					
					if label == "Layer":
						material.layers.append(self.layer_parser.parse(context))
						pars -= 1
					elif label in Material.FLAGS:
						material.flags |= Material.FLAGS[label]
					else:
						raise Exception("Unknown data in material: %s %s" % (label, data))
						
					line, pars = self.read(pars)
				
			line, pars = self.read(pars)'''
		#print("End parse for Bone_%s  \n" % (name))
		return bone