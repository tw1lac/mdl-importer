import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

from MDLParser import MDLParser
from add_VertexGroup import add_VertexGroup
from add_armature import add_armature
from createAnim import createAnim


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
			createAnim(model)

		return {"FINISHED"}