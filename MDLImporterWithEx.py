#Copyright 2017 Yellow
#
#Permission is hereby granted, free of charge, to any person obtaining a copy 
#of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
#copies of the Software, and to permit persons to whom the Software is furnished
#to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all 
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
#PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
#OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#DEALINGS IN THE SOFTWARE.

import bpy
import os

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

bl_info = {
	"name": "MDL Importer",
	"description": "Imports Warcraft 3 models",
	"author": "Yellow",
	"version": (0,1,5),
	"blender": (2,7,8),
	"location": "File > Import > WC3 MDL (.mdl)",
	"category": "Import-Export"
}

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

class VersionParser(Parser):
	def parse(self, context):
		label, version = self.file.readline().replace(",", "").split(" ")
		if int(version) != 800:
			raise Exception("MDL file version not supported")

			
class Geoset(object):
	def __init__(self):
		self.vertices = []
		self.normals = []
		self.faces = []
		self.uvs = []
		self.material_id = None
		self.vertexGroup = []
		self.groups = []
		
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

class Texture(object):
	def __init__(self):
		self.filepath = ""
		self.replaceable_id = None
		
class TextureParser(Parser):
	def parse(self, context, count):
		textures = []
		pars = 1
		
		line, pars = self.read(pars)
		
		for _ in range(count):
			label, *data = line.split(" ")
			
			if label == "Bitmap":
				texture = Texture()
				textures.append(texture)
				
				line, pas = self.read(pars)

				while pars > 1:
					label, data = line.split(" ")
					
					if label == "Image" and data:
						texture.filepath = data.replace('"', "").replace("blp", "png")
					elif label == "ReplaceableId":
						texture.replaceable_id = int(data)
					else:
						raise Exception("Unknown data in texture: %s %s" % (label, data))
						
					line, pars = self.read(pars)
				
				if texture.replaceable_id == 2:
					texture.filepath = "ReplaceableTextures/TeamGlow/TeamGlow00.png"
				
			line, pars = self.read(pars)
		
		return textures

class Material(object):
	FLAGS = {"ConstantColor": 2**0, "SortPrimitivesNearZ": 2**3, "SortPrimitivesFarZ": 2**4, "FullResolution": 2**5}
	def __init__(self):
		self.layers = []
		self.flags = 0
		
class MaterialParser(Parser):
	def __init__(self, file):
		self.layer_parser = LayerParser(file)
		super(MaterialParser, self).__init__(file)

	def parse(self, context, count):
		materials = []
		pars = 1

		line, pars = self.read(pars)
		
		for _ in range(count):
			label, *data = line.split(" ")
			
			if label == "Material":	
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
				
			line, pars = self.read(pars)
					
		return materials

class Layer(object):
	SHADING_FLAGS = {"Unshaded": 2**0, "SphereEnvironmentMap": 2**1, "TwoSided": 2**4, "Unfogged": 2**5, "NoDepthTest": 2**6, "NoDepthSet": 2**7}
	FILTER_MODES = ["None", "Transparent", "Blend", "Additive", "AddAlpha", "Modulate", "Modulate2x"]
	def __init__(self):
		self.filter_mode 		 = "None"
		self.shading_flags 		 = 0
		self.texture_id 		 = None
		self.texture_anim_id 	 = None
		self.coord_id 			 = None
		self.alpha 				 = None
		self.material_alpha      = None
		self.material_texture_id = None

class MaterialAlpha(object):
	def __init__(self):
		self.interpolation_type = "None"
		self.tracks				= {}

class LayerParser(Parser):
	def __init__(self, file):
		self.tokens = [
			"FilterMode", "Unshaded", "SphereEnvironmentMap", 
			"TwoSided", "Unfogged", "NoDepthTest", "NoDepthSet",
			"TextureID", "Alpha", "Linear"
		]
		super(LayerParser, self).__init__(file)
		
	def parse(self, context):
		layer = Layer()
		pars = 1
		
		line, pars = self.read(pars)
		
		while pars > 0:
			label, *data = line.split(" ")

			if label == "static":
				label = data[0]
				data = data[1:]
			
			if label in self.tokens:			
				if label in Layer.SHADING_FLAGS:
					layer.shading_flags |= Layer.SHADING_FLAGS[label]
					
				elif label == "FilterMode":
					if data[0] in Layer.FILTER_MODES:
						layer.filter_mode = data[0]
					else:
						raise Exception("Unknown FilterMode: '%s'" % data[0])
					
				elif label == "Alpha":
					if len(data) > 1:
						layer.material_alpha = MaterialAlpha()
						
						line, pars = self.read(pars)
					
						while pars > 1:
							label, *data = line.replace(":", "").strip().split(" ")
							
							if label in ["Linear", "Hermite", "Bezier", "DontInterp"]:
								layer.material_alpha.interpolation_type = label
							else:
								layer.material_alpha.tracks[label] = data[0]
					
							line, pars = self.read(pars)	
					else:
						layer.alpha = data[0]
						
				elif label == "TextureID":
					layer.texture_id = int(data[0])
			else:
				raise Exception("Unknown data in layer: %s %s" % (label, data))
				
			line, pars = self.read(pars)
		
		return layer

#=========================================================> for BEGIN
#=========================================================> for 骨骼
class BoneDataData(object):
	def __init__(self):
		self.time 		 = -1
		self.val	 	 = [3]
		self.inTan	 	 = [3]
		self.outTan 	 	 = [3]

class BoneData(object):
	def __init__(self, name):
		self.name		 = name
		self.type		 = "Hermite"
		self.globalSeqId 	 = -1
		self.data 		 = []
		self.size		 = 0

class Bone(object):
	def __init__(self):
		self.name 		 = "None"
		self.objectId 		 = -1
		self.boneData 		 = []
		#self.geosetId 	 	 = -1
		self.parent		 = -1

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

#=========================================================> for 骨骼位置
class PivotPoint(object):
	def __init__(self):
		self.pos = [3]

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

def prn_obj(obj): 
	 print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

def prn_list(obj):
	for i in range(len(obj)):
		prn_obj(obj[i])

def prn_list2(obj):
	for i in range(len(obj)):
		print("\n")
		for j in range(len(obj[i])):
			print(" " + str(obj[i][j]))

def add_armature(mode):
	armature_name = mode.name
	bpy.ops.object.armature_add() # 创建骨架
	bpy.context.active_object.name = armature_name # 命名骨架
	bpy.data.objects[armature_name].data.name = armature_name # 命名下一层级
	#set location for armature
	bpy.data.objects[armature_name].location = (0.0, 0.0, 0.0)
	bpy.ops.object.editmode_toggle()
	data_basebone = bpy.data.objects[armature_name].data.edit_bones["Bone"]
	bpy.data.objects[armature_name].data.edit_bones.remove(data_basebone) # 删除默认骨头

	for i, bone in enumerate(mode.bones):
		bpy.ops.armature.bone_primitive_add(name = bone.name) # 在编辑模式增加骨头
		data_editbone = bpy.data.armatures[armature_name].edit_bones[bone.name] # 一个bone TYPE
		bpy.data.armatures[armature_name].edit_bones.active=data_editbone # 给骨头命名，超麻烦
		pos = (float(mode.pivots[bone.objectId].pos[1]), float(mode.pivots[bone.objectId].pos[2]), float(mode.pivots[bone.objectId].pos[3]))
		bpy.context.active_bone.head = pos # 骨头根位置
		pos = (float(mode.pivots[bone.objectId].pos[1]), float(mode.pivots[bone.objectId].pos[2]), float(mode.pivots[bone.objectId].pos[3]) + 1 / 20)
		bpy.context.active_bone.tail = pos # 骨头尖位置
		#print("create bone with ID=%s NAME=%s \n" % (bone.objectId, bone.name))

	#Enter object mode first
	#bpy.ops.object.mode_set(mode='OBJECT')

	for i, bone in enumerate(mode.bones):
		#clear select flag
		#See https://blender.stackexchange.com/questions/102983/how-do-i-set-parent-to-armature
		bpy.ops.armature.select_all(action='DESELECT')
		if(bone.parent >= 0):
			data_editbone = bpy.data.armatures[armature_name].edit_bones[bone.name]
			#bpy.data.armatures[armature_name].edit_bones.active=data_editbone # 激活某根骨头
			for j, parent in enumerate(mode.bones):
				#find parent bone!!!
				if(bone.parent == parent.objectId):
					data_editbone.parent = bpy.data.armatures[armature_name].edit_bones[parent.name]
					#data_editbone = bpy.data.armatures[armature_name].edit_bones[parent.name]
					#bpy.data.armatures[armature_name].edit_bones.active=data_editbone # 激活某根骨头
					#bpy.ops.armature.parent_set(type='OFFSET') # 骨头间连接，类型为保持偏移
					#bone.select = True
					#parent.select = True
					#the active object will be the parent of all selected object
					#bpy.data.armatures[armature_name].edit_bones.active = data_editbone
					#bpy.ops.armature.parent_set(type='OFFSET')
					#bpy.ops.object.parent_set(type='BONE', keep_transform=True)
					#print("create parent with C=%s P=%s " % (bone.name, parent.name))
					break

#定点组 VertexGroup -> (Groups) -> (骨骼IDs)
#创建关联并指定权重
def add_VertexGroup(mode, geosets, meshs):

	#print('vertex_groups.keys => ')
	#print(list(meshs[0].values()))
	#print(str(meshs[0].vertices[0].co[0] * 20))
	#print(len(geosets[0].vertex_groups))

	armature = bpy.data.objects[mode.name]
	#针对每个Geoset，创建空的定点组集合（应该通过关联自动创建）
	#link armature
	#bpy.context.scene.objects.link(armature)
	for i in range(len(geosets)):
	#for i,geoset in enumerate(geosets):
		#物体模式创建与骨骼关联
		bpy.ops.object.mode_set(mode='OBJECT')
		geoset = geosets[i]
		bpy.ops.object.select_all(action='DESELECT')
		geoset.select = True
		armature.select = True
		bpy.context.scene.objects.active = armature
		#关联&创建空顶点组
		bpy.ops.object.parent_set(type='ARMATURE_NAME')

		#选择顶点
		bpy.ops.object.select_all(action='DESELECT')
		#geoset.select = True
		bpy.context.scene.objects.active = geoset
		#print(list(geoset.vertex_groups.keys()))
		#编辑模式，指定顶点组
		#bpy.ops.object.mode_set(mode='EDIT')
		mesh = meshs[i]
		#select it!
		#See http://wiki.xentax.com/index.php/Blender_Import_Guide#Bones.2C_weights
		for j in range(len(mode.geosets[i].vertexGroup)):
			vp = mode.geosets[i].vertexGroup[j]
			#Groups
			gps = mode.geosets[i].groups[int(vp)]
			for bid in gps:
				#print("for BOND_ID %s " % bid)
				for bone in mode.bones:
					if(bone.objectId == bid):
						#bpy.ops.object.select_all(action='DESELECT')
						geoset.vertex_groups[bone.name].add([mesh.vertices[j].index], 1, type='ADD')
						#对应顶点
						#print(geoset.vertex_groups[bone.name].index)
						#mesh.vertices.co[i].select = True
						#mesh.vertices.co[i+1].select = True
						#mesh.vertices.co[i+2].select = True
						#mesh.vertices[j].select = True						
						#geoset.vertex_groups.active = geoset.vertex_groups[bone.name]
						#print("add for %s %s " % (bone.name, mesh.vertices[j]))
						#bpy.ops.object.vertex_group_assign()
						#mesh.vertices[j].select = False
						break

#for anim SequencesParser
class Anim(object):
	def __init__(self):
		self.name = ""
		self.start = 0
		self.end = 0
		self.min = []
		self.max = []
		self.radius = 0
		self.loop = True

class SequencesParser(Parser):
	def __init__(self, file):
		super(SequencesParser, self).__init__(file)
		
	def parse(self, context, count):
		anims = []
		pars = 1
		line, pars = self.read2(pars)
		#print("1 line=%s pars=%d " % (line, pars))
		while(pars > 0):
			if(line.find("Anim") >= 0):
				anim = Anim()
				anim.name = line.replace("Anim", "").replace("{", "").replace("}", "").replace(",", "").strip()
				line, pars = self.read2(pars)
				#print("2 line=%s pars=%d " % (line, pars))
				while(pars > 1):
					if(line.find("Interval") >= 0):
						frames = line.replace("Interval", "").replace("{", "").replace("}", "").replace(",", "").strip().split(" ")
						anim.start = frames[0]
						anim.end = frames[1]
					elif line.find("NonLooping") >= 0 :
						anim.loop = False
					elif line.find("MinimumExtent") >= 0 :
						[anim.min.append(float(v)) for v in line.replace("MinimumExtent", "").replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]
					elif line.find("MaximumExtent") >= 0 :
						[anim.max.append(float(v)) for v in line.replace("MaximumExtent", "").replace("{", "").replace("}", "").replace(",", "").strip().split(" ")]
					elif line.find("BoundsRadius") >= 0 :
						anim.radius = float(line.replace("BoundsRadius", "").replace("{", "").replace("}", "").replace(",", "").strip())
					line, pars = self.read2(pars)
				#Add it!!!
				anims.append(anim)

			line, pars = self.read2(pars)
			
		#prn_list(anims)

		return anims


'''
bpy.ops.action.new(
找到匹配bone（如果anim存在gid，则需要跟bone匹配）的 frames 集合（旋转、缩放、位移）
（即bone.xxx.frame在anim的begin、end之间）（按先后排序）

这两个示例都在活动对象的Z轴上插入关键帧。

简单的例子：

obj = bpy.context.object
obj.location[2] = 0.0
obj.keyframe_insert(data_path="location", frame=10.0, index=2)
obj.location[2] = 1.0
obj.keyframe_insert(data_path="location", frame=20.0, index=2)
使用低级功能：

obj = bpy.context.object
obj.animation_data_create()
obj.animation_data.action = bpy.data.actions.new(name="MyAction")
fcu_z = obj.animation_data.action.fcurves.new(data_path="location", index=2)
fcu_z.keyframe_points.add(2)
fcu_z.keyframe_points[0].co = 10.0, 0.0
fcu_z.keyframe_points[1].co = 20.0, 1.0


def createAnim(mode):
	armature = bpy.data.objects[mode.name]
	for anim in model.anims:
		obj = bpy.context.object
		obj.animation_data_create()
		#针对每个anim创建一个action
		obj.animation_data.action = bpy.data.actions.new(name=anim.name)
		#find match bone
		for bone in mode.bones:
			for bdata in bone.boneData:
				for data in bdata.data:
					if data.time >= anim.start and data.time <= anim.end:
						#
						if bdata.name = "Rotation":
							#TODO
						elif bdata.name = "Translation":
							#TODO
							fcu_z = obj.animation_data.action.fcurves.new(data_path="location", index=2)
'''
#=========================================================> for END

class Model(object):
	def __init__(self):
		self.name = ""
		self.geosets = []
		self.textures = []
		self.materials = []
		self.bones = []
		self.pivots = []
		self.anims = []
		
class MDLParser(Parser):
	def __init__(self, file):
		self.tokens = {
			"Version": VersionParser(file),
			"Model": None, # We only care about the model's name right now
			"Geoset": GeosetParser(file),
			"Textures": TextureParser(file),
			"Materials": MaterialParser(file),
			"Sequences": SequencesParser(file), 
			#"GlobalSequences", 
			#"GeosetAnim", 
			"Bone": BoneParser(file), 
			#"Helper", 
			#"Attachment", 
			"PivotPoints" : PivotPointsParser(file)
		}
		super(MDLParser, self).__init__(file)

	def parse(self, context):
		model = Model()
		line = self.file.readline()
		while(line):
			label, *data = line.split(" ")
			
			if label not in self.tokens:
				line = self.file.readline()
				continue
				
			if label == "Model":
				model.name = data[0].replace('"', "")
			elif label == "Geoset":
				model.geosets.append(self.tokens[label].parse(context))
			elif label == "Version":
				self.tokens["Version"].parse(context)
			elif label == "Textures":
				model.textures = self.tokens[label].parse(context, int(data[0]))
			elif label == "Materials":
				model.materials = self.tokens[label].parse(context, int(data[0]))
			elif label == "Bone":
				model.bones.append(self.tokens[label].parse(context, data[0]))
			elif label == "Sequences":
				model.anims = self.tokens[label].parse(context, data[0])
			elif label == "PivotPoints":
				model.pivots = self.tokens[label].parse(context, data[0])
				
			line = self.file.readline()

		return model

class Importer(bpy.types.Operator, ImportHelper):
	bl_idname = "import_mesh.mdl"
	bl_label = "MDL (.mdl)"
	filename_ext = ".mdl"
	filter_glob = StringProperty(default="*.mdl", options={"HIDDEN"})
	
	@classmethod
	def poll(cls, context):
		return True
		
	def execute(self, context):
	
		with open(self.filepath, "r") as file:
			model = MDLParser(file).parse(context)
			
			textures = []
			materials = []
			objs = []
			overtices = []
			meshs = []
			
			# Make blender set the viewport shading to "Material" so we can see something
			bpy.context.scene.render.engine = "CYCLES"
			for area in bpy.context.screen.areas:
				if area.type == "VIEW_3D":
					for space in area.spaces:
						if space.type == "VIEW_3D":
							space.viewport_shade = "MATERIAL"
			
			# Create the materials
			for i, material in enumerate(model.materials):

				mat = bpy.data.materials.new("%s Material %i" % (model.name, i))
				mat.use_nodes = True
				mat.game_settings.alpha_blend = "CLIP"
				
				nodes = mat.node_tree.nodes
				links = mat.node_tree.links
				
				tex_image = nodes.new("ShaderNodeTexImage")

				#print('nodes.keys => ')
				#print(list(nodes.keys()))
				#keytmps = list(nodes.keys())
				#for chinese
				if "材质输出" in nodes.keys():
					output = nodes["材质输出"]
					diffuse = nodes["漫射 BSDF"]
				else:
					output = nodes["Material Output"]
					diffuse = nodes["Diffuse BSDF"]
				#['材质输出', '漫射 BSDF', '图像纹理']
				#output = nodes["Material Output"]
				#output = nodes["材质输出"]
				#diffuse = nodes["Diffuse BSDF"]
				#diffuse = nodes["漫射 BSDF"]
				mix = nodes.new("ShaderNodeMixShader")
				blend_colour = None
				rid = None
				
				# This bit sorts out composing layers. The layer with team colour needs to have the colour mixed in
				# The layer without the team colours need to have transparency mixed in
				# The colour is just set to green by default right now, change it in the "default_value" RGBA tuples
				for layer in material.layers:
					tex = model.textures[layer.texture_id]
					rid = tex.replaceable_id
					
					if rid == 1:
						blend_colour = nodes.new("ShaderNodeBsdfDiffuse")
						blend_colour.inputs[0].default_value = (0.0, 1.0, 0.0, 1.0)
						continue
					elif rid == 2:
						nodes.remove(diffuse)
						diffuse = nodes.new("ShaderNodeEmission")
						diffuse.inputs[0].default_value = (0.0, 1.0, 0.0, 1.0)
					
					#tex_image.image = bpy.data.images.load(os.path.expanduser("~/Desktop/WC3Data/" + tex.filepath))
					tex_image.image = bpy.data.images.load("/home/bingh/下载/test.png")
					if not blend_colour:
						blend_colour = nodes.new("ShaderNodeBsdfTransparent")
						if rid == 2:
							blend_colour.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
						else:
							blend_colour.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
				
				if rid == 2:
					links.new(tex_image.outputs[0], mix.inputs[0])
				else:
					links.new(tex_image.outputs[0], diffuse.inputs[0])
					links.new(tex_image.outputs[1], mix.inputs[0])
					
				links.new(blend_colour.outputs[0], mix.inputs[1])
				links.new(diffuse.outputs[0], mix.inputs[2])
				links.new(mix.outputs[0], output.inputs[0])
					
				materials.append(mat)
			
			# Load in the meshes, and UVs, and add the materials to the correct one
			for i, geoset in enumerate(model.geosets):
			
				mesh = bpy.data.meshes.new("%s Mesh %i" % (model.name, i))
				obj = bpy.data.objects.new("%s Mesh %i" % (model.name, i), mesh)
				obj.location = (0.0, 0.0, 0.0)
				bpy.context.scene.objects.link(obj)
				
				mesh.vertices.add(len(geoset.vertices) // 3)
				mesh.vertices.foreach_set("co", geoset.vertices)
				
				mesh.tessfaces.add(len(geoset.faces) // 3)
				mesh.tessfaces.foreach_set("vertices", geoset.faces)
				
				mesh.vertices.foreach_set("normal", geoset.normals)
				
				mesh.update()
				
				vi_uv = {i: (u, 1.0 - v) for i, (u, v) in enumerate(geoset.uvs)}
				per_loop_list = [0.0] * len(mesh.loops)
				for loop in mesh.loops:
					per_loop_list[loop.index] = vi_uv[loop.vertex_index]
				
				per_loop_list = [uv for pair in per_loop_list for uv in pair]
				
				mesh.uv_textures.new("UV")
				mesh.uv_layers[0].data.foreach_set("uv", per_loop_list)
				
				mesh.materials.append(materials[geoset.material_id])
				
				mesh.update()
				
				objs.append(obj)
				meshs.append(mesh)
				overtices.append(geoset.vertices)

			#Load bones
			add_armature(model)
			#Create VertexGroup for geoset
			add_VertexGroup(model, objs, meshs)

		return {"FINISHED"}

def menu(self, context):
	self.layout.operator("import_mesh.mdl", text="WC3 MDL (.mdl)")

def register():
	bpy.utils.register_class(Importer)
	bpy.types.INFO_MT_file_import.append(menu)
	
def unregister():
	bpy.utils.unregister_class(Importer)
	bpy.types.INFO_MT_file_import.remove(menu)
		
if __name__ == "__main__":
	register()
	
	bpy.ops.import_mesh.mdl("INVOKE_DEFAULT")
