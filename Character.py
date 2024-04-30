import os
import bpy
import json
import math


# Extracts x,y,z values from vectors, eulers etc. into array.
def extract_to_array(elem):
    return [elem.x, elem.y, elem.z]


class Character:
    """Class to load model, poses & actions."""

    def __init__(self, name, path):
        self.name = name
        self.path = os.path.join(path, name)

    def load(self):  # Loads model into the Scene.
        if bpy.data.objects.get("skeleton_" + self.name) == None:
            model_path = os.path.join(self.path, "model", self.name + ".blend")
            with bpy.data.libraries.load(model_path) as (data_from, data_to):
                data_to.objects = [
                    name for name in data_from.objects if name.endswith(self.name)]

            orphan_list = [m for m in bpy.data.objects if m.users == 0]
            col = bpy.data.collections[0]

            for orphan in orphan_list:
                col.objects.link(orphan)

            skeleton = bpy.data.objects.get("skeleton_" + self.name)
            bpy.context.scene.frame_set(0)
            skeleton.animation_data.action.fcurves.clear()

    def loadPose(self, poseName):  # Loads pose to model at current frame.
        file = open(os.path.join(
            self.path, "predef_poses", poseName + '.json'), 'r')

        pose_data = json.load(file)

        skeleton = bpy.data.objects["skeleton_" + self.name]
        bpy.context.view_layer.objects.active = skeleton
        bpy.ops.object.mode_set(mode='POSE')

        for key in pose_data.keys():
            bone = skeleton.pose.bones[key]
            bone.rotation_mode = 'XYZ'

            if bone.parent == None or (bone.get('is_IK') != None and bone.get('is_IK') == True):
                loc = pose_data[key]['location']
                bone.location = [loc['x'], loc['y'], loc['z']]
                rot = pose_data[key]['rotation']
                bone.rotation_euler = (rot['x'], rot['y'], rot['z'])
            else:
                rot = pose_data[key]['rotation']
                bone.rotation_euler = (rot['x'], rot['y'], rot['z'])

    def loadAction(self, actionName):  # Loads action at current frame.
        f = open(os.path.join(self.path, "predef_actions",
                 actionName + '.json'), 'r')

        action_data = json.load(f)

        skeleton = bpy.data.objects["skeleton_" + self.name]
        bpy.context.view_layer.objects.active = skeleton
        bpy.ops.object.mode_set(mode='POSE')

        start_frame = bpy.context.scene.frame_current
        bpy.context.scene.frame_set(start_frame)
        end_frame = start_frame

        locr = extract_to_array(skeleton.pose.bones['root'].location)
        rotr = extract_to_array(skeleton.pose.bones['root'].rotation_euler)

        for key in action_data.keys():
            bone = skeleton.pose.bones[key]
            bone.rotation_mode = 'XYZ'
            if key != 'root':
                for trans_key in action_data[key].keys():
                    for axis_key in action_data[key][trans_key].keys():
                        for frame_key in action_data[key][trans_key][axis_key].keys():
                            bpy.context.scene.frame_set(
                                int(frame_key) + start_frame)

                            val = action_data[key][trans_key][axis_key][frame_key]

                            match trans_key:
                                case "location":
                                    bone.location[int(axis_key)] = val
                                case "rotation_euler":
                                    bone.rotation_euler[int(
                                        axis_key)] = val

                            bone.keyframe_insert(data_path=trans_key, index=int(
                                axis_key), frame=int(frame_key) + start_frame)

        frames = set()
        for trans_key in action_data['root'].keys():
            for axis_key in action_data['root'][trans_key].keys():
                for frame_key in action_data['root'][trans_key][axis_key]:
                    frames.add(int(frame_key))

        frames = list(frames)
        frames.sort()

        def getValueAtFrame(arm_name, translation, frame_no, axis):
            if str(frames[frame_no]) in action_data[arm_name][translation][axis].keys():
                val = action_data[arm_name][translation][axis][str(
                    frames[frame_no])]
            else:
                val = None
            return val if val != None else getValueAtFrame(arm_name, translation, frame_no - 1, axis)

        root_co_ordinates = {}

        for frame_no in range(len(frames)):
            root_co_ordinates[int(frames[frame_no])] = {}
            for trans in ['location', 'rotation_euler']:
                val = {}
                for axis in range(3):
                    val[axis] = getValueAtFrame(
                        'root', trans, frame_no, str(axis))
                root_co_ordinates[int(frames[frame_no])][trans] = val

        root = skeleton.pose.bones['root']

        for frame in root_co_ordinates:
            init_angle = rotr[2]
            pos = root_co_ordinates[frame]['location']
            rot = root_co_ordinates[frame]['rotation_euler']
            pos = [
                pos[0] * math.cos(init_angle) - pos[1] * math.sin(init_angle),
                pos[1] * math.cos(init_angle) + pos[0] * math.sin(init_angle),
                pos[2]
            ]
            for axis in range(3):
                root.location[axis] = pos[axis] + locr[axis]
                root.rotation_euler[axis] = rot[axis] + rotr[axis]

                for translation in ['location', 'rotation_euler']:
                    root.keyframe_insert(data_path=translation,
                                        index=axis, frame=frame + start_frame)
            
            end_frame = frame + start_frame

        bpy.context.scene.frame_set(end_frame)


def walk_from_stading(character, num_of_steps):
    if num_of_steps <= 0:
        print('Number of steps should be 1 or more.')
    else:
        character.loadAction('standing_to_walk_right')
        step_num = 1
        while step_num < num_of_steps:
            if step_num % 2 != 0:
                character.loadAction('walk_right_to_left')
            else:
                character.loadAction('walk_left_to_right')
            step_num += 1
        if step_num % 2 != 0:
            character.loadAction('walk_right_to_standing')
        else:
            character.loadAction('walk_left_to_standing')


subbaRao = Character('SubbaRao', '')
subbaRao.load()
walk_from_stading(subbaRao, 4)

