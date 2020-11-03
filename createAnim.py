import bpy


def createAnim(mode):
	#bpy.data.scenes["Scene"].transform_orientation = "Local"
	bpy.data.scenes["Scene"].render.fps = 900
	armature = bpy.data.objects[mode.name]
	bpy.ops.object.select_all(action='DESELECT')
	armature.select = True
	bpy.context.scene.objects.active = armature
	#姿态模式插入帧动画
	bpy.ops.object.mode_set(mode='POSE')
	#for simple animation for all bone!!!
	for bone in mode.bones:
		for bdata in bone.boneData:
			for data in bdata.data:
				obj = armature.pose.bones[bone.name]
				obj.bone.select = True
				orgLoc = [obj.location.x, obj.location.y, obj.location.z]
				#obj = bpy.data.armatures[mode.name].pose_bones[bone.name]
				#bpy.data.armatures[mode.name].pose_bones.active = obj # 激活某根骨头
				#obj = bpy.data.objects[mode.name + ":" + bone.name]
				#bpy.context.scene.frame_set(data.time)
				if bdata.name.find("Rotation") >= 0:
					obj.rotation_euler = (data.val[1], data.val[2], data.val[3])
					obj.keyframe_insert(data_path="rotation_euler", frame=data.time)
					print("[%s]obj.keyframe_insert rotation_euler %d" % (bone.name, data.time))
				elif bdata.name.find("Translation") >= 0:
					#print("data.val = %s" % (data.val))
					obj.location = [data.val[1], data.val[2], data.val[3]]
					obj.keyframe_insert(data_path="location", frame=data.time)
					print("[%s]obj.keyframe_insert location %d" % (bone.name, data.time))
				#rotation_euler scale location
				#obj.keyframe_insert(data_path="location", frame=data.time)
				#obj.keyframe_insert(data_path="rotation_euler", frame=data.time)
				obj.rotation_euler = (0, 0, 0)
				#print("orgLoc 2 = %s %s" % (orgLoc, obj.location))
				obj.location = orgLoc
				obj.bone.select = False
	# make interpolation between keyframes linear
	for fc in armature.animation_data.action.fcurves: # stub
		for kp in fc.keyframe_points:
			kp.handle_left_type = 'VECTOR'
			kp.handle_right_type = 'VECTOR'
		fc.update()
	'''
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