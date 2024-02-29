bl_info = {
    "name": "Scripted Motions",
    "author": "Bhavani Sahithi Ranjan",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D Viewport > Sidebar",
    "description": "text to animation",
    "category": "",
}

import bpy
import os

from bpy_extras.io_utils import ImportHelper

from bpy.props import (StringProperty, PointerProperty)
                       
from bpy.types import (Panel, PropertyGroup, Operator)

def write_pose_data(name ,filepath):
    human = bpy.data.objects[name]
    bpy.context.view_layer.objects.active = human
    bpy.ops.object.mode_set(mode = 'POSE')
    f = open(filepath, 'w', encoding='utf-8')
    
    for bone in human.pose.bones:
        f.write(bone.name)
        f.write(", ")
        #print(bone.rotation_quaternion)
        x = bone.location[0]
        y = bone.location[1]
        z = bone.location[2]
        f.write("%0.9f, %0.9f, %0.9f" % (x, y, z))
        f.write(", ")
        quat = bone.rotation_quaternion
        f.write("%0.9f, %0.9f, %0.9f, %0.9f" % (quat.w, quat.x, quat.y, quat.z))
        f.write("\n")
    f.close()
    
def load_pose_data(charName, filepath):
    file = open(filepath, 'r')
    lines = []
    while True:
        line = file.readline()
        if not line:
            break;
        x = line.strip().split(", ")
        bone = {}
        bone['name'] = x[0]
        bone['pos_x'], bone['pos_y'], bone['pos_z'] = float(x[1]), float(x[2]), float(x[3]), 
        bone['rot_w'], bone['rot_x'], bone['rot_y'], bone['rot_z'] = float(x[4]), float(x[5]), float(x[6]), float(x[7])
        #print(bone)
        lines.append(bone)
    file.close()
    human = bpy.data.objects[charName]
    bpy.context.view_layer.objects.active = human
    bpy.ops.object.mode_set(mode = 'POSE')
    for line in lines:
        name = line['name']
        bone = human.pose.bones[name]
        bone.location = (line['pos_x'], line['pos_y'], line['pos_z'])
        bone.rotation_quaternion = (line['rot_w'], line['rot_x'], line['rot_y'], line['rot_z'])
        

class WritePoseOperator(Operator, ImportHelper):
    bl_idname = "pose.write_pose_operator"
    bl_label = "Write Pose"

    
    def execute(self, context):
        write_pose_data("skeleton_human_male", self.filepath)
        return {'FINISHED'}
    
class LoadPoseOperator(Operator, ImportHelper):
    bl_idname = "pose.load_pose_operator"
    bl_label = "Load Pose"
    
    def execute(self, context):
        load_pose_data("skeleton_human_male", self.filepath)
        return {'FINISHED'}


class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Scripted Motion"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)


class WritePose(View3DPanel, Panel):
    bl_idname = "VIEW3D_PT_write_pose"
    bl_label = "Write Pose"

    def draw(self, context):
        layout = self.layout  
        scn = context.scene
        
        
        row = layout.row()
        row.label(text="Select file to write pose data")
        
        row = layout.row()
        row.operator("pose.write_pose_operator", text="Write")
        
class LoadPose(View3DPanel, Panel):
    bl_idname = "VIEW3D_PT_load_pose"
    bl_label = "Load Pose"
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        
        row = layout.row()
        row.label(text="Select file to load")
        
        row = layout.row()
        row.operator("pose.load_pose_operator", text="Load")


classes = (
    WritePoseOperator,
    LoadPoseOperator,
    WritePose,
    LoadPose
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()