import os
import bpy
import json

# This class
class CharacterCreator:

    def __init__(self, name, path):
        self.name = name
        self.path = os.path.join(path, name)

    def save(self):
        if bpy.context.selectable_objects:
            skeleton = bpy.context.selected_objects[0]
            if skeleton.type != 'ARMATURE':
                print('Selected Object is not an Armature. Character not saved.')
                return
        else:
            print('Nothing is selected. Please select armature of character to save.')
            return

        mesh = None
        isParent = False
        for obj in bpy.data.objects:
            if obj.parent == skeleton:
                isParent = True
                mesh = obj
                break

        if isParent:
            skeleton.name = 'skeleton_' + self.name
            mesh.name = 'mesh_' + self.name
        else:
            print('No mesh is attached to skeleton. Character not saved.')
            return

        os.makedirs(self.path, exist_ok=True)
        os.makedirs(os.path.join(self.path, "model"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "predef_poses"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "predef_actions"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "custom_actions"), exist_ok=True)

        bpy.context.view_layer.objects.active = skeleton
        bpy.ops.object.mode_set(mode='POSE')

        for bone in skeleton.pose.bones:
            bone.rotation_mode = 'XYZ'

        filepath = os.path.join(self.path, "model", self.name + ".blend")

        data_blocks = {
            obj for obj in bpy.data.objects if obj.name.endswith(self.name)}

        bpy.data.libraries.write(filepath, data_blocks)

        f = open(os.path.join(self.path, "data.json"),
                 'w', encoding='utf-8')
        data = {}
        data['fps'] = bpy.context.scene.render.fps
        json.dump(data, f, indent=4)

    def savePose(self, poseName):
        skeleton = bpy.data.objects['skeleton_' + self.name]
        bpy.context.view_layer.objects.active = skeleton
        bpy.ops.object.mode_set(mode='POSE')

        f = open(os.path.join(self.path, "predef_poses",
                 poseName + '.json'), 'w', encoding='utf-8')
        pose_data = {}
        for bone in skeleton.pose.bones:
            bone_pose_data = {}
            if bone.get('is_IK') != None and bone.get('is_IK') == True:
                if bone.parent == None:
                    continue
                loc = bone.location
                bone_pose_data['location'] = {
                    'x': round(loc[0], 3), 'y': round(loc[1], 3), 'z': round(loc[2], 3)}
                rot = bone.rotation_euler
                bone_pose_data['rotation'] = {
                    'x': round(rot.x, 3), 'y': round(rot.y, 3), 'z': round(rot.z, 3)}
            else:
                if bone.parent == None:
                    continue
                rot = bone.rotation_euler
                bone_pose_data['rotation'] = {
                    'x': round(rot.x, 3), 'y': round(rot.y, 3), 'z': round(rot.z, 3)}
            pose_data[bone.name] = bone_pose_data

        json.dump(pose_data, f, indent=4)
        f.close()

    def saveAction(self, actionName, start_frame, end_frame):
        skeleton = bpy.data.objects['skeleton_' + self.name]
        bpy.context.view_layer.objects.active = skeleton
        bpy.ops.object.mode_set(mode='POSE')

        f = open(os.path.join(self.path, "predef_actions",
                 actionName + '.json'), 'w', encoding='utf-8')
        
        action_data = []

        fcurves = skeleton.animation_data.action.fcurves

        for fcurve in fcurves:
            keyframe_points = []
            
            for keyframe in fcurve.keyframe_points:
                if start_frame <= keyframe.co[0] <= end_frame:
                    keyframe_points.append([keyframe.co[0] - start_frame,round(keyframe.co[1], 3)])
            
            action_data.append([fcurve.data_path,fcurve.array_index,keyframe_points])

        json.dump(action_data, f, indent=4)
        f.close()

subbaRao = CharacterCreator('SubbaRao', 'D:\phani')
#subbaRao.save()
#subbaRao.savePose('walk_right')
subbaRao.saveAction('walk_left_to_standing', 1, 13)
