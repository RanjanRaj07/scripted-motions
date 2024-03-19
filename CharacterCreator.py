import os
import bpy
import json

class CharacterCreator:

    def __init__(self, name, path):
        self.name = name
        self.path = os.path.join(path, name)

    def save(self):
        os.makedirs(self.path, exist_ok=True)
        os.makedirs(os.path.join(self.path, "model"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "pre_def_poses"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "pre_def_actions"), exist_ok=True)

        human = bpy.data.objects[self.name]
        bpy.context.view_layer.objects.active = human
        bpy.ops.object.mode_set(mode = 'POSE')

        for bone in human.pose.bones:
            bone.rotation_mode = 'XYZ'

        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(self.path, "model", self.name + ".blend"), copy=True)

    def savePose(self, poseName):
        human = bpy.data.objects[self.name]
        bpy.context.view_layer.objects.active = human
        bpy.ops.object.mode_set(mode = 'POSE')

        f = open(os.path.join(self.path, "pre_def_poses", poseName + '.json'), 'w', encoding='utf-8')
        pose_data = {}
        for bone in human.pose.bones:
            bone_pose_data = {}
            if bone.parent == None:
                loc = bone.location
                bone_pose_data['location'] = {'x':loc[0], 'y':loc[1], 'z':loc[2]}
            else:
                rot = bone.rotation_euler
                bone_pose_data['rotation'] = {'x':rot.x, 'y':rot.y, 'z':rot.z}
            pose_data[bone.name] = bone_pose_data

        json.dump(pose_data, f, indent=4)
        f.close()

    def saveAction(self, actionName, start_frame, end_frame):
        human = bpy.data.objects[self.name]
        bpy.context.view_layer.objects.active = human
        bpy.ops.object.mode_set(mode = 'POSE')

        f = open(os.path.join(self.path, "pre_def_actions", actionName + '.json'), 'w', encoding='utf-8')
        action_data = {}

        # Get the action associated with the armature
        fcurves = human.animation_data.action.fcurves

        for fcurve in fcurves:
            #print(fcurve.array_index)
            data_path = fcurve.data_path
            bone_name = data_path.split("\"")[1]

            if bone_name not in action_data:
                action_data[bone_name] = {}
            trans_name = data_path.split(".")[2]

            if trans_name not in action_data[bone_name]:
                action_data[bone_name][trans_name] = {}

            index = fcurve.array_index

            if index not in action_data[bone_name][trans_name]:
                action_data[bone_name][trans_name][index] = {}

            for keyframe in fcurve.keyframe_points:
                if start_frame <= keyframe.co[0] <= end_frame:
                    action_data[bone_name][trans_name][index][int(keyframe.co[0] - start_frame)] = keyframe.co[1]

        json.dump(action_data, f, indent=4)
        f.close()

subbaRao = CharacterCreator('skeleton_human_male', 'yourFilePath')
subbaRao.save()
subbaRao.savePose('SubbaRao')
subbaRao.saveAction('AppaRao', 5, 20)