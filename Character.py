import os
import bpy

class Character:
    def __init__(self, name, path):
        self.name = name
        self.path = os.path.join(path, name)
        
    def loadPose(self, poseName):
        file = open(os.path.join(self.path, "pre_def_poses", poseName + '.csv'),'r')
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
            lines.append(bone)
        file.close()
        human = bpy.data.objects[self.name]
        bpy.context.view_layer.objects.active = human
        bpy.ops.object.mode_set(mode = 'POSE')
        
        for line in lines:
            name = line['name']
            bone = human.pose.bones[name]
            bone.location = (bone.location[0]+line['pos_x'], bone.location[1]+line['pos_y'], bone.location[2]+line['pos_z'])
            w,x,y,z = bone.rotation_quaternion.w, bone.rotation_quaternion.x, bone.rotation_quaternion.y, bone.rotation_quaternion.z
            bone.rotation_quaternion = (line['rot_w']+w, line['rot_x']+x, line['rot_y']+y, line['rot_z']+z)
            
            
test = Character('skeleton_human_male', 'yourFolderPath')
test.loadPose('pose1')
