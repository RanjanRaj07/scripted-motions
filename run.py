import sys
import bpy

pth = 'C:\\Sahithi\\projects\\major project\\scripted-motions'
if pth not in sys.path:
    sys.path.append(pth)

from character_functions import move_from_standing, turn
from Character import Character

#subbaRao = Character('SubbaRao', 'C:\Sahithi\projects\major project')
#subbaRao.load()
#move_from_standing(subbaRao, 'run', 4)
#move_from_standing(subbaRao, 'walk', 5)
#turn(subbaRao, -45)
#move_from_standing(subbaRao, 'sneak', 5)

def is_char_in_list(char_name, list_of_characters):
    val = False
    for item in list_of_characters:
        if char_name == item['name']:
            val = True
    return val

def get_path(char_name, list_of_characters):
    path = ''
    for item in list_of_characters:
        if char_name == item['name']:
            path = item['path']
    return path

def run_script(list_of_actions, list_of_characters):
    for action_dict in list_of_actions:
        
        char_name = action_dict['CHARACTER']
        if is_char_in_list(char_name, list_of_characters) == False:
            return
        action = action_dict['ACTION']
        iteration = 0
        duration = 0
        angle = 0.0
        destination = ''
        if action_dict['ITERATION'] != 0:
            iteration = action_dict['ITERATION']
        
        if action_dict['DURATION'] != 0:
            duration = action_dict['DURATION']

        if action_dict['ANGLE'] != 0.0:
            angle = action_dict['ANGLE']

        if action_dict['DESTINATION'] != '':
            destination = action_dict['DESTINATION']

        char = Character(char_name, get_path(char_name, list_of_characters))
        if iteration != 0:
            char.loadBipedAction(action,iteration)
        elif duration != 0:
            print('not yet implemented')
        elif action == 'turn' and angle != 0.0:
            char.turn(angle)