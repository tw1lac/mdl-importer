# Copyright 2017 Yellow&bingh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import bpy

from Importer import Importer

bl_info = {
    "name": "MDL Importer",
    "description": "Imports Warcraft 3 models",
    "author": "Yellow, bingh & twilac",
    "version": (0, 1, 5),
    "blender": (2, 7, 8),
    "location": "File > Import > WC3 MDL (.mdl)",
    "category": "Import-Export"
}


# =========================================================> for BEGIN
# =========================================================> for 骨骼

# =========================================================> for 骨骼位置

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


# 定点组 VertexGroup -> (Groups) -> (骨骼IDs)
# 创建关联并指定权重

# for anim SequencesParser


'''
bpy.ops.action.new(
找到匹配bone（如果anim存在gid，则需要跟bone匹配）的 frames 集合（旋转、缩放、位移）
（即bone.xxx.frame在anim的begin、end之间）（按先后排序）

bpy.ops.anim.keyframe_insert_menu(type='LocRotScale', frame=?)

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

================================================================================
https://blender.stackexchange.com/questions/16084/how-to-animate-object-with-data-file/16088
================================================================================
import bpy

... # read x,y,z and t from a file, assuming seconds for t

# and do something like this in a loop for all keys:
f = bpy.data.scenes["Scene"].render.fps * t + 1 # stub
obj = bpy.data.objects["Cube"] # stub
obj.location = [x,y,z]
obj.keyframe_insert(data_path="location", frame=f)

# make interpolation between keyframes linear
for fc in obj.animation_data.action.fcurves: # stub
    for kp in fc.keyframe_points:
        kp.handle_left_type = 'VECTOR'
        kp.handle_right_type = 'VECTOR'
    fc.update()


or
================================================================================
https://blender.stackexchange.com/questions/141761/script-for-rotating-multiple-selected-objects-and-insert-keyframes
================================================================================
import bpy
from math import *  
import mathutils

scene = bpy.data.scenes["Scene"]
scene.frame_start = 1
scene.frame_end = 768

ob = bpy.context.object

bpy.context.scene.frame_set(24) # start with delay

ob.rotation_euler = (0,0,0)

bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

bpy.context.scene.frame_set(120) #half rotation 1

ob.rotation_euler = (0,0,3.14)

bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

'''


# =========================================================> for END


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
