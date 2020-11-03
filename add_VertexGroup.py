import bpy


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