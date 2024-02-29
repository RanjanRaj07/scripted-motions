import bpy

def load_pose(charName, filePath):
    file = open(filePath,'r')
    lines = []
    while True:
        line = file.readline()
        if not line:
            break;
        x = line.strip().split(", ")
        bone = {}
        bone['name'] = x[0]
        bone['pos_x'], bone['pos_y'], bone['pos_z'] = float(x[1]), float(x[2]), float(x[3]), 
        bone['rot_w'], bone['rot_x'], bone['rot_y'], bone['rot_z'] = float(x[4]), float(x[5]), float(x[6]), float(x[7])
        lines.append(bone)
    file.close()
    human = bpy.data.objects[charName]
    bpy.context.view_layer.objects.active = human
    bpy.ops.object.mode_set(mode = 'POSE')
    
    for line in lines:
        name = line['name']
        bone = human.pose.bones[name]
        bone.location = (line['pos_x'], line['pos_y'], line['pos_z'])
        bone.rotation_quaternion = (line['rot_w'], line['rot_x'], line['rot_y'], line['rot_z'])

load_pose("skeleton_human_male", "C:/Sahithi/projects/scripted motionspose.csv")