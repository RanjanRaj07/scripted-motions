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
            if bpy.context.active_object != None:
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
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
            # skeleton.animation_data.action.fcurves.clear()
            bpy.context.view_layer.objects.active = skeleton
            bpy.ops.object.select_all(action='DESELECT')

    def loadPose(self, poseName):  # Loads pose to model at current frame.
        if bpy.context.active_object != None:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        skeleton = bpy.data.objects["skeleton_" + self.name]
        if skeleton == None:
            return
        
        file = open(os.path.join(
            self.path, "predef_poses", poseName + '.json'), 'r')

        pose_data = json.load(file)

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

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    def loadAction(self, actionName, biped_action = ''):
        skeleton = bpy.data.objects["skeleton_" + self.name]
        if skeleton == None:
            return
        predef_path = os.path.join(self.path, "predef_actions")
        if biped_action != '':
            predef_path = os.path.join(predef_path, biped_action)
        f = open(os.path.join(predef_path,
                 actionName + '.json'), 'r')

        action_data = json.load(f)

        if bpy.context.active_object != None:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        bpy.context.view_layer.objects.active = skeleton
        bpy.ops.object.mode_set(mode='POSE')

        start_frame = bpy.context.scene.frame_current
        bpy.context.scene.frame_set(start_frame)
        end_frame = start_frame

        locr = extract_to_array(skeleton.pose.bones['root'].location)
        rotr = extract_to_array(skeleton.pose.bones['root'].rotation_euler)

        if skeleton.animation_data == None:
            skeleton.animation_data_create()
            skeleton.animation_data.action = bpy.data.actions.new(
                name=self.name + "_Action")

        if skeleton.animation_data.action == None:
            skeleton.animation_data.action = bpy.data.actions.new(
                name=self.name + "_Action")

        fcurves = skeleton.animation_data.action.fcurves
        root_frames = set()
        root_action_data = {}
        for fcurve in action_data:
            if fcurve[0].split("\"")[1] != 'root':
                if fcurves.find(data_path=fcurve[0], index=int(fcurve[1])) == None:
                    fc = fcurves.new(data_path=fcurve[0], index=int(fcurve[1]))
                else:
                    fc = fcurves.find(
                        data_path=fcurve[0], index=int(fcurve[1]))

                for pnt in range(len(fcurve[2])):
                    co = fcurve[2][pnt]
                    fc.keyframe_points.insert(
                        int(co[0]) + start_frame, float(co[1]))
            else:
                trans_name = fcurve[0].split(".")[2]
                if trans_name not in root_action_data:
                    root_action_data[trans_name] = {}
                index = int(fcurve[1])
                if index not in root_action_data[trans_name]:
                    root_action_data[trans_name][index] = {}

                for frame in fcurve[2]:
                    root_action_data[trans_name][index][int(
                        frame[0])+start_frame] = frame[1]

                for pnt in range(len(fcurve[2])):
                    co = fcurve[2][pnt]
                    root_frames.add(int(co[0]) + start_frame)

        root_frames = list(root_frames)
        root_frames.sort()

        def getValueAtFrame(translation, frame_no, axis):
            if root_frames[frame_no] in root_action_data[translation][axis].keys():
                val = root_action_data[translation][axis][
                    root_frames[frame_no]]
            else:
                val = None
            return val if val != None else getValueAtFrame(translation, frame_no - 1, axis)

        root_co_ordinates = {}

        for frame_no in range(len(root_frames)):
            root_co_ordinates[root_frames[frame_no]] = {}
            for trans in ['location', 'rotation_euler']:
                val = {}
                for axis in range(3):
                    val[axis] = getValueAtFrame(
                        trans, frame_no, axis)
                root_co_ordinates[root_frames[frame_no]][trans] = val

        for frame in root_co_ordinates:
            init_angle = rotr[2]
            pos = root_co_ordinates[frame]['location']
            rot = root_co_ordinates[frame]['rotation_euler']
            pos = [
                pos[0] * math.cos(init_angle) - pos[1] *
                math.sin(init_angle) + locr[0],
                pos[1] * math.cos(init_angle) + pos[0] *
                math.sin(init_angle) + locr[1],
                pos[2] + locr[2]
            ]
            rot = [
                rot[0] + rotr[0],
                rot[1] + rotr[1],
                rot[2] + rotr[2]
            ]
            root_co_ordinates[frame]['location'] = pos
            root_co_ordinates[frame]['rotation_euler'] = rot

        for trans in ['location', 'rotation_euler']:
            for index in range(3):
                if fcurves.find(data_path="pose.bones[\"root\"]." + trans, index=index) == None:
                    fc = fcurves.new(
                        data_path="pose.bones[\"root\"]." + trans, index=index)
                else:
                    fc = fcurves.find(
                        data_path="pose.bones[\"root\"]." + trans, index=index)
                for frame in root_co_ordinates:
                    co = [frame, root_co_ordinates[frame][trans][index]]
                    fc.keyframe_points.insert(co[0], co[1])
                    end_frame = co[0]

        bpy.context.scene.frame_set(end_frame)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
    
    def loadBipedAction(self, actionName, num_of_steps):
        if num_of_steps <= 0:
            print('Number of steps should be 1 or more.')
        else:
            self.loadAction(actionName + '_right_from_standing', actionName)
            step_num = 1
            while step_num < num_of_steps:
                if step_num % 2 != 0:
                    self.loadAction(actionName + '_right_to_left', actionName)
                else:
                    self.loadAction(actionName + '_left_to_right', actionName)
                step_num += 1
            if step_num % 2 != 0:
                self.loadAction(actionName + '_right_to_standing', actionName)
            else:
                self.loadAction(actionName + '_left_to_standing', actionName)
    
    def turn(self, angle):
        if angle == 0:
            return
        turn_angle = angle % 360
        if turn_angle > 180:
            direction = 'right'
            dir_factor = -1
            turn_angle = 360 - turn_angle
        else:
            direction = 'left'
            dir_factor = 1

        times = 1
        if turn_angle > 90:
            times = 2
            turn_angle = turn_angle * 0.5

        skeleton = bpy.data.objects["skeleton_" + self.name]
        root = skeleton.pose.bones['root']
        root.rotation_mode = 'XYZ'

        turn_angle = math.radians(turn_angle)
        pre_angle = root.rotation_euler[2]

        for x in range(times):
            self.loadAction('turn_' + direction)
            root.rotation_euler = (0, 0, pre_angle + (x + 1) * turn_angle * dir_factor)
            root.keyframe_insert(data_path='rotation_euler',
                                index=2, frame=bpy.context.scene.frame_current)
# ------------------------------------------
