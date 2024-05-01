import bpy
import sys
import math

pth = 'D:\\phani\\blenderAnimPlugin'
if pth not in sys.path:
    sys.path.append(pth)

from Character import Character

# Moves the character with the type of move specified number of times specified.
def move_from_standing(character:Character, move, num_of_steps):
    if num_of_steps <= 0:
        print('Number of steps should be 1 or more.')
    else:
        character.loadAction(move + '_right_from_standing')
        step_num = 1
        while step_num < num_of_steps:
            if step_num % 2 != 0:
                character.loadAction(move + '_right_to_left')
            else:
                character.loadAction(move + '_left_to_right')
            step_num += 1
        if step_num % 2 != 0:
            character.loadAction(move + '_right_to_standing')
        else:
            character.loadAction(move + '_left_to_standing')

#----------------------------------------------------------------
# Turns the Character by the angle specified.
def turn(character, angle):
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

    skeleton = bpy.data.objects["skeleton_" + character.name]
    root = skeleton.pose.bones['root']
    root.rotation_mode = 'XYZ'

    turn_angle = math.radians(turn_angle)
    pre_angle = root.rotation_euler[2]

    for x in range(times):
        character.loadAction('turn_' + direction)
        root.rotation_euler = (0, 0, pre_angle + (x + 1) * turn_angle * dir_factor)
        root.keyframe_insert(data_path='rotation_euler',
                            index=2, frame=bpy.context.scene.frame_current)