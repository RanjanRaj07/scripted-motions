import os
import bpy
import json

class Character:
    def __init__(self, name, path):
        self.name = name
        self.path = os.path.join(path, name)

    def loadPose(self, poseName):
        file = open(os.path.join(self.path, "pre_def_poses", poseName + '.json'),'r')

        pose_data = json.load(file)

        human = bpy.data.objects[self.name]
        bpy.context.view_layer.objects.active = human
        bpy.ops.object.mode_set(mode = 'POSE')

        for key in pose_data.keys():
            bone = human.pose.bones[key]
            bone.rotation_mode = 'XYZ'
            
            if bone.parent == None:
                loc = pose_data[key]['location']
                bone.location = [loc['x'], loc['y'], loc['z']]
            else:
                rot = pose_data[key]['rotation']
                bone.rotation_euler = (rot['x'], rot['y'], rot['z'])
                
    def loadAction(self, actionName, start_frame):
        f = open(os.path.join(self.path, "pre_def_actions", actionName + '.json'),'r')
        
        action_data = json.load(f)
        
        human = bpy.data.objects[self.name]
        bpy.context.view_layer.objects.active = human
        bpy.ops.object.mode_set(mode = 'POSE')
        
        for key in action_data.keys():
            bone = human.pose.bones[key]
            bone.rotation_mode = 'XYZ'

            for trans_key in action_data[key].keys():
                for axis_key in action_data[key][trans_key].keys():
                    for frame_key in action_data[key][trans_key][axis_key].keys():
                        match trans_key:
                            case "location":
                                bone.location[int(axis_key)] = action_data[key][trans_key][axis_key][frame_key]
                            case "rotation_euler":
                                bone.rotation_euler[int(axis_key)] = action_data[key][trans_key][axis_key][frame_key]
                                
                        bone.keyframe_insert(data_path=trans_key, index=int(axis_key), frame=int(frame_key) + start_frame)

subbaRao = Character('skeleton_human_male','D:\phani')
subbaRao.loadCharacter()