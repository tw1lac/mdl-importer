import bpy


def add_armature(mode):
	armature_name = mode.name
	bpy.ops.object.armature_add()  # Create the armature
	bpy.context.active_object.name = armature_name  # Name the armature
	bpy.data.objects[armature_name].data.name = armature_name  # Name the next level
	# set location for armature
	bpy.data.objects[armature_name].location = (0.0, 0.0, 0.0)
	bpy.ops.object.editmode_toggle()
	data_basebone = bpy.data.objects[armature_name].data.edit_bones["Bone"]
	bpy.data.objects[armature_name].data.edit_bones.remove(data_basebone)  # Delete default bone
	print("edit bones?")
	for i, bone in enumerate(mode.bones):
		# print(bone)
		bpy.ops.armature.bone_primitive_add(name=bone.name)  # Add bones in edit mode
		data_editbone = bpy.data.armatures[armature_name].edit_bones[bone.name]  # A bone TYPE
		bpy.data.armatures[armature_name].edit_bones.active = data_editbone  # "Naming the bones, so troublesome"
		pos = (float(mode.pivots[bone.objectId].pos[1]), float(mode.pivots[bone.objectId].pos[2]), float(mode.pivots[bone.objectId].pos[3]))
		bpy.context.active_bone.head = pos  # Bone root position
		pos = (float(mode.pivots[bone.objectId].pos[1]), float(mode.pivots[bone.objectId].pos[2]), float(mode.pivots[bone.objectId].pos[3]) + 1 / 20)
		bpy.context.active_bone.tail = pos  # Bone tip position
		#print("create bone with ID=%s NAME=%s \n" % (bone.objectId, bone.name))

	#Enter object mode first
	#bpy.ops.object.mode_set(mode='OBJECT')

	for i, bone in enumerate(mode.bones):
		#clear select flag
		#See https://blender.stackexchange.com/questions/102983/how-do-i-set-parent-to-armature
		bpy.ops.armature.select_all(action='DESELECT')
		if(bone.parent >= 0):
			data_editbone = bpy.data.armatures[armature_name].edit_bones[bone.name]
			#bpy.data.armatures[armature_name].edit_bones.active=data_editbone # Activate a certain bone
			for j, parent in enumerate(mode.bones):
				# print("look for parent bone")
				# find parent bone!!!
				if(bone.parent == parent.objectId):
					data_editbone.parent = bpy.data.armatures[armature_name].edit_bones[parent.name]
					#data_editbone = bpy.data.armatures[armature_name].edit_bones[parent.name]
					#bpy.data.armatures[armature_name].edit_bones.active=data_editbone # Activate a certain bone
					#bpy.ops.armature.parent_set(type='OFFSET') # The connection between the bones, the type is to keep the offset
					#bone.select = True
					#parent.select = True
					#the active object will be the parent of all selected object
					#bpy.data.armatures[armature_name].edit_bones.active = data_editbone
					#bpy.ops.armature.parent_set(type='OFFSET')
					#bpy.ops.object.parent_set(type='BONE', keep_transform=True)
					#print("create parent with C=%s P=%s " % (bone.name, parent.name))
					break