import bpy
import sys
import os

from bpy.types import Panel, Operator, PropertyGroup
from bpy.types import EnumProperty, PointerProperty

dir = "C:\\Sahithi\\projects\\major project\\ui"
if not dir in sys.path:
    sys.path.append(dir)
    
from Character_02 import Character

active_char = None

pose_list = []
action_list = []

test_list = ["something", "just for fun", "hope this works", "lol"] #considering this as a temp list of file names, will consider actual dynamic list of file names later

#char_list = ["raju", "aman", "shalini"] still working on this 

class MyPropertyGroup(PropertyGroup) :
    
    pose_enum : bpy.props.EnumProperty(
        items=[(name, name, '') for name in test_list],
        name="Poses",
    )
    
    action_enum : bpy.props.EnumProperty(
        items=[(name, name, '') for name in test_list],
        name="Actions",
    )
    
    char_path : bpy.props.StringProperty(
        name = "Character Path",
        description="Choose a directory:",
        subtype='DIR_PATH'
    )


class ScriptedMotionPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Scripted Motion"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)

class CreatorPanel(ScriptedMotionPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Creator"
    bl_label = "Creator"
    
    def draw(self, context):
        
        self.layout.label(text="creator panel buttons")

class DirectorPanel(ScriptedMotionPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Director"
    bl_label = "Director"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool, "char_path")
        
        layout.operator("wm.loadchar_operator")
        
        layout.label(text="Character Active : " + mytool.char_path.split("\\")[-2])
        
#        layout.prop(mytool, "pose_enum")
        layout.label(text="Poses")
        
        if mytool.char_path:
            folder_files = os.listdir(os.path.join(mytool.char_path,"predef_poses"))
            for file_name in folder_files:
                row = layout.row()
                row.label(text="\t\t\t\t"+file_name,)
        
#        layout.prop(mytool, "action_enum")
        layout.label(text="Actions")
        if mytool.char_path:
            folder_files = os.listdir(os.path.join(mytool.char_path,"predef_actions"))
            for file_name in folder_files:
                row = layout.row()
                row.label(text="\t\t\t\t"+file_name)
        
        layout.operator("wm.inputtext_operator")
#        if active_char == None:
#            it.active = False
        
        layout.label(text="Input Text Summary:\n")
        
        layout.operator("wm.runscript_operator")
        
class LoadCharacterOperator(bpy.types.Operator) :
    bl_label = "Load Character"
    bl_idname = "wm.loadchar_operator"
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        path = mytool.char_path
        if path.endswith("\\"):
            path = path[:-1]
        
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
      
        character = Character(basename, dirname)
        character.load()
        active_char = bpy.data.objects["skeleton_" + character.name]
        
#        global pose_list, action_list  # Use global variables
#        pose_list = [f for f in os.listdir(os.path.join(path, "predef_poses"))]
#        action_list = [f for f in os.listdir(os.path.join(path,"predef_actions"))]

class InputTextOperator(bpy.types.Operator) :
    bl_label = "Enter Script"
    bl_idname = "wm.inputtext_operator"
    
#    input : bpy.props.StringProperty()
    
    def execute(self,context) :
        os.system("python.exe C:\nlp\nlp.py shalini walks 3 steps.")
        return {'FINISHED'}
    
#    def invoke(self, context, event) :
#        return context.window_manager.invoke_props_dialog(self)
#    
#    def draw(self, context) :
#        layout = self.layout
#        layout.prop(self, "input")

class RunScriptOperator(bpy.types.Operator) :
    bl_label = "Run Script"
    bl_idname = "wm.runscript_operator"
    
    
    def execute(self,context) :
        return {'FINISHED'}


classes = (
    MyPropertyGroup,
    CreatorPanel,
    DirectorPanel,
    LoadCharacterOperator,
    InputTextOperator,
    RunScriptOperator
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyPropertyGroup)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()