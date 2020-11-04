import bpy


def createAnim(model):
	#bpy.data.scenes["Scene"].transform_orientation = "Local"
	bpy.data.scenes["Scene"].render.fps = 900
	armature = bpy.data.objects[model.name]
	bpy.ops.object.select_all(action='DESELECT')
	armature.select = True
	bpy.context.scene.objects.active = armature
	# Insert frame animation in pose mode
	bpy.ops.object.mode_set(mode='POSE')
	# for simple animation for all bone!!!
	for bone in model.bones:
		for bdata in bone.boneData:
			for data in bdata.data:
				this_bone = armature.pose.bones[bone.name]
				this_bone.bone.select = True
				# orgLoc = [this_bone.location.x, this_bone.location.y, this_bone.location.z]
				orgLoc = [this_bone.location[0], this_bone.location[1], this_bone.location[2]]

				# this_bone = bpy.data.armatures[model.name].pose_bones[bone.name]
				# bpy.data.armatures[model.name].pose_bones.active = this_bone # Activate a certain bone
				# this_bone = bpy.data.objects[model.name + ":" + bone.name]
				# bpy.context.scene.frame_set(data.time)
				try:
					if bdata.name.find("Rotation") >= 0:
						this_bone.rotation_euler = (data.val[1], data.val[2], data.val[3])
						this_bone.keyframe_insert(data_path='rotation_euler', frame=data.time)
						# print("rot - [%s]this_bone.keyframe_insert rotation_euler %d" % (bone.name, data.time))
					elif bdata.name.find("Translation") >= 0:
						#print("data.val = %s" % (data.val))
						this_bone.location = [data.val[1], data.val[2], data.val[3]]
						this_bone.keyframe_insert(data_path="location", frame=data.time)
						# print("trens - [%s]this_bone.keyframe_insert location %d" % (bone.name, data.time))
				except:
					print("failed on: ", this_bone)
				# rotation_euler scale location
				# this_bone.keyframe_insert(data_path="location", frame=data.time)
				# this_bone.keyframe_insert(data_path="rotation_euler", frame=data.time)
				this_bone.rotation_euler = (0, 0, 0)
				# print("orgLoc 2 = %s %s" % (orgLoc, this_bone.location))
				this_bone.location = orgLoc
				this_bone.bone.select = False
	# make interpolation between keyframes linear
	for fc in armature.animation_data.action.fcurves: # stub
		for kp in fc.keyframe_points:
			kp.handle_left_type = 'VECTOR'
			kp.handle_right_type = 'VECTOR'
		fc.update()

	# # armature = bpy.data.objects[model.name]
	# for anim in model.anims:
	# 	this_bone = bpy.context.object
	# 	this_bone.animation_data_create()
	# 	# Create an action for each anim
	# 	this_bone.animation_data.action = bpy.data.actions.new(name=anim.name)
	# 	# find match bone
	# 	for bone in model.bones:
	# 		for bdata in bone.boneData:
	# 			for data in bdata.data:
	# 				if data.time >= anim.start and data.time <= anim.end:
	# 					print("animate! :O")
	# 					# #
	# 					# if bdata.name == "Rotation":
	# 					# 	#TODO
	# 					# elif bdata.name == "Translation":
	# 					# 	#TODO
	# 					# 	fcu_z = this_bone.animation_data.action.fcurves.new(data_path="location", index=2)
