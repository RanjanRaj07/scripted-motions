import bpy

def show_message_box(message = "", title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
        
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def write_pose(charName, filePath):
    human = bpy.data.objects[charName]
    bpy.context.view_layer.objects.active = human
    bpy.ops.object.mode_set(mode = 'POSE')
    
    f = open(filePath, 'w', encoding='utf-8')
    for bone in human.pose.bones:
        f.write(bone.name)
        f.write(", ")
        x = bone.location[0]
        y = bone.location[1]
        z = bone.location[2]
        f.write("%0.9f, %0.9f, %0.9f" % (x, y, z))
        f.write(", ")
        quat = bone.rotation_quaternion
        f.write("%0.9f, %0.9f, %0.9f, %0.9f" % (quat.w, quat.x, quat.y, quat.z))
        f.write("\n")
    f.close()
    show_message_box("Pose successfully written to file.")

write_pose("skeleton_human_male", "C:/Sahithi/projects/scripted motions/pose.csv")