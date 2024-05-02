import bpy
import sys
import os

from bpy.types import Panel, Operator, PropertyGroup
from bpy.types import EnumProperty, PointerProperty

dir = "C:\\Sahithi\\projects\\major_project\\scripted-motions"
if not dir in sys.path:
    sys.path.append(dir)
    
from nlp.nlp import run_nlp

from Character import Character
from CharacterCreator import CharacterCreator

from run import run_script


class MyCreatorPanelPropertyGroup(PropertyGroup):
    
    name : bpy.props.StringProperty(name = "Filename")
    
    path : bpy.props.StringProperty(
        name = "Path",
        description="Choose a directory:",
        subtype='DIR_PATH'
        )
        
    folder_exists : bpy.props.BoolProperty()
    
    pose_name : bpy.props.StringProperty(name = "Pose Name")
    
    action_name : bpy.props.StringProperty(name = "Action Name")
    
    start_frame : bpy.props.IntProperty(name = "Start Frame")
    
    end_frame : bpy.props.IntProperty(name = "End Frame")
    
    biped_action : bpy.props.StringProperty(name = "Biped Action Name")


class MyPropertyGroup(PropertyGroup) :
    
    char_path : bpy.props.StringProperty(
        name = "Character Path",
        description="Choose a directory:",
        subtype='DIR_PATH'
    )
    
    inputText : bpy.props.StringProperty()
    
    active_char_name : bpy.props.StringProperty()
    
    
class MyListPropertyGroup(PropertyGroup) :
    
    name : bpy.props.StringProperty()
    
    path : bpy.props.StringProperty()
    
    
class MyDictPropertyGroup(PropertyGroup) :
    
    name : bpy.props.StringProperty()
    
    action : bpy.props.StringProperty()
    
    iteration : bpy.props.IntProperty()
    
    angle : bpy.props.FloatProperty()
    
    duration : bpy.props.IntProperty()
    
    destination : bpy.props.StringProperty()


class ScriptedMotionPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Scripted Motion"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)

class Creator_PT_Panel(ScriptedMotionPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Creator"
    bl_label = "Creator"
    
    def draw(self, context):
        scene = context.scene
        mytools = scene.my_tools 
        
#        self.layout.label(text="creator panel buttons")
        layout = self.layout
        layout.operator("wm.savechar_operator")
        
        layout.label(text="character name : " + mytools.name)
        print(mytools.folder_exists)
        
        row = layout.row()
        if mytools.folder_exists == False:
            row.enabled = False
        row.operator("wm.savepose_operator")
        row.operator("wm.saveaction_operator")
        

class Director_PT_Panel(ScriptedMotionPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Director"
    bl_label = "Director"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool, "char_path")
        
        layout.operator("wm.loadchar_operator")
        
        if mytool.active_char_name != None:    
            layout.label(text="Active Character : " + mytool.active_char_name)
        
class Pose_PT_Panel(ScriptedMotionPanel, bpy.types.Panel):
    bl_parent_id = "VIEW3D_PT_Director"
    bl_label = "Poses"
    
    def draw(self,context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        if mytool.char_path:
            folder_files = os.listdir(os.path.join(mytool.char_path,"predef_poses"))
            for file_name in folder_files:
                row = layout.row()
                row.label(text="\t\t\t\t"+file_name,)
        

class Action_PT_Panel(ScriptedMotionPanel, bpy.types.Panel):
    bl_parent_id = "VIEW3D_PT_Director"
    bl_label = "Actions"
    
    def draw(self,context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        if mytool.char_path:
            folder_files = os.listdir(os.path.join(mytool.char_path,"predef_actions"))
            for file_name in folder_files:
                row = layout.row()
                row.label(text="\t\t\t\t"+file_name)
                
class InputText_PT_Panel(ScriptedMotionPanel, bpy.types.Panel):
    bl_parent_id = "VIEW3D_PT_Director"
    bl_label = "Enter Script"
    
    def draw(self,context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool,"inputText")
        layout.operator("wm.inputtext_operator")
        
class RunScript_PT_Panel(ScriptedMotionPanel, bpy.types.Panel):
    bl_parent_id = "VIEW3D_PT_Director"
    bl_label = "Run Script"
    
    def draw(self,context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.operator("wm.runscript_operator")

class SaveCharacterOperator(bpy.types.Operator) :
    bl_label = "Save Character"
    bl_idname = "wm.savechar_operator"
    
    def execute(self, context):
        scene = context.scene
        mytools = scene.my_tools
        
        character = CharacterCreator(mytools.name, mytools.path)
        character.save()
        if os.path.exists(os.path.join(mytools.path, mytools.name)):
            mytools.folder_exists = True
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytools = scene.my_tools
        
        layout.prop(mytools, "name")
        layout.prop(mytools, "path")
        
class SavePoseOperator(bpy.types.Operator) :
    bl_label = "Save Pose"
    bl_idname = "wm.savepose_operator"
    
    def execute(self, context):
        scene = context.scene
        mytools = scene.my_tools
        
        character = CharacterCreator(mytools.name, mytools.path)
        character.savePose(mytools.pose_name)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytools = scene.my_tools
        
        layout.prop(mytools, "pose_name")
    
    
class SaveActionOperator(bpy.types.Operator) :
    bl_label = "Save Action"
    bl_idname = "wm.saveaction_operator"
    
    def execute(self, context):
        scene = context.scene
        mytools = scene.my_tools
        
        character = CharacterCreator(mytools.name, tools.path)
        character.saveAction(mytools.action_name, mytools.start_frame, mytools.end_frame, mytools.biped_action)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytools = scene.my_tools
        
        layout.prop(mytools, "action_name")
        layout.prop(mytools, "start_frame")
        layout.prop(mytools, "end_frame")
        layout.prop(mytools, "biped_action")
        
class LoadCharacterOperator(bpy.types.Operator) :
    bl_label = "Load Character"
    bl_idname = "wm.loadchar_operator"
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        mylist = scene.my_list
        
        path = mytool.char_path
        if path.endswith("\\"):
            path = path[:-1]
        
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
      
        character = Character(basename, dirname)
        character.load()
       
        mytool.active_char_name = character.name
        
        char = mylist.add()
        char.name = character.name
        char.path = dirname
        
        return {'FINISHED'}


class InputTextOperator(bpy.types.Operator) :
    bl_label = "Enter Script"
    bl_idname = "wm.inputtext_operator"
    
    
    def execute(self,context) :
        scene = context.scene
        mytool = scene.my_tool
        mydict = scene.my_dict
        
        mydict.clear()
        output = run_nlp(mytool.inputText)
        
        for dict in output:
            d = mydict.add()
            if 'CHARACTER' in dict.keys():
#                d = mydict.add()
                d.name = dict['CHARACTER']
            if 'ACTION' in dict.keys():
#                d = mydict.add()
                d.action = dict['ACTION']
            if 'ITERATION' in dict.keys():
#                d = mydict.add()
                d.iteration = int(dict['ITERATION'][:-5])
            if 'ANGLE' in dict.keys():
#                d = mydict.add()
                d.angle = float(dict['ANGLE'][:-3])
            if 'DURATION' in dict.keys():
#                d = mydict.add()
                d.duration = int(dict['DURATION'][:-4])
            if 'DESTINATION' in dict.keys():
#                d = mydict.add()
                d.destination = dict['DESTINATION']
            
        return {'FINISHED'}

class RunScriptOperator(bpy.types.Operator) :
    bl_label = "Run Script"
    bl_idname = "wm.runscript_operator"
    
    
    def execute(self,context) :
        scene = context.scene
        mylist = scene.my_list
        mydict = scene.my_dict
        
        list_of_actions = []
        list_of_characters = []
        
        for item in mylist:
            list_of_characters.append({'name' : item.name, 'path' : item.path})
        for item in mydict:
            list_of_actions.append({
                'CHARACTER' : item.name,
                'ACTION' : item.action,
                'ITERATION' : item.iteration,
                'DURATION' : item.duration,
                'ANGLE' : item.angle,
                'DESTINATION' : item.destination,
            })
#        print(list_of_actions)
#        print(list_of_characters)
        run_script(list_of_actions, list_of_characters)
        return {'FINISHED'}


classes = (
    MyPropertyGroup,
    MyListPropertyGroup,
    MyDictPropertyGroup,
    MyCreatorPanelPropertyGroup,
    Creator_PT_Panel,
    Director_PT_Panel,
    LoadCharacterOperator,
    SaveCharacterOperator,
    SavePoseOperator,
    SaveActionOperator,
    InputTextOperator,
    RunScriptOperator,
    Pose_PT_Panel,
    Action_PT_Panel,
    InputText_PT_Panel,
    RunScript_PT_Panel,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tools = bpy.props.PointerProperty(type=MyCreatorPanelPropertyGroup)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyPropertyGroup)
    bpy.types.Scene.my_list = bpy.props.CollectionProperty(type=MyListPropertyGroup)
    bpy.types.Scene.my_dict = bpy.props.CollectionProperty(type=MyDictPropertyGroup)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool
    del bpy.types.Scene.my_list
    del bpy.types.Scene.my_dict


if __name__ == "__main__":
    register()