import sys
import bpy

pth = 'C:\\Sahithi\\projects\\major project\\scripted-motions'
if pth not in sys.path:
    sys.path.append(pth)

from character_functions import move_from_standing, turn
from Character import Character

subbaRao = Character('SubbaRao', 'C:\Sahithi\projects\major project')
subbaRao.load()
move_from_standing(subbaRao, 'run', 4)
move_from_standing(subbaRao, 'walk', 5)
turn(subbaRao, -45)
move_from_standing(subbaRao, 'sneak', 5)

def run_script(list_of_actions):
    for action_dict in list_of_actions:
        
        char_name = action_dict['CHARACTER']
        action = action_dict['ACTION']
        iteration = None
        duration = None
        angle = None
        destination = None
        if action_dict['ITERATION'] != None:
            iteration = int(action_dict['ITERATION'].split(" ")[0])
        
        if action_dict['DURATION'] != None:
            duration = int(action_dict['DURATION'].split(" ")[0])

        if action_dict['ANGLE'] != None:
            angle = float(action_dict['ANGLE'].split(" ")[0])

        if action_dict['DESTINATION'] != None:
            destination = action_dict['DESTINATION']

        char = bpy.data.objects.get(char_name)
        if iteration != None:
            move_from_standing(char,action,int(iteration))
        elif duration != None:
            pass
        elif action == 'turn' and angle != None:
            turn(char, angle)