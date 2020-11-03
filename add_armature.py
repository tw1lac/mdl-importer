import bpy


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