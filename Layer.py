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
