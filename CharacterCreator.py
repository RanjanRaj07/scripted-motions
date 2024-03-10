import os
import bpy
class CharacterCreator:
    
    def __init__(self, name, path):
        self.name = name
        self.path = os.path.join(path, name)
    
    def save(self):
        os.makedirs(self.path, exist_ok=True)
        os.makedirs(os.path.join(self.path, "model"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "pre_def_poses"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "pre_def_actions"), exist_ok=True)
        print(self.path + '\pre_def_poses')
        
    def savePose(self, poseName):
        human = bpy.data.objects[self.name]
        bpy.context.view_layer.objects.active = human
        bpy.ops.object.mode_set(mode = 'POSE')
        
        f = open(os.path.join(self.path, "pre_def_poses", poseName + '.csv'), 'w', encoding='utf-8')
        for bone in human.pose.bones:
            f.write(bone.name)
            f.write(", ")
            x = bone.location[0]
            y = bone.location[1]
            z = bone.location[2]
            f.write("%0.9f, %0.9f, %0.9f" % (x, y, z))
            f.write(", ")
            quat = bone.rotation_quaternion
            f.write("%0.9f, %0.9f, %0.9f, %0.9f" % (quat.w, quat.x, quat.y, quat.z))
            f.write("\n")
        f.close()

test = CharacterCreator('skeleton_human_male', 'giveFolderPath')
test.save()
test.savePose('pose1')