import bpy
#bpy.ops.mesh.primitive_cube_add(location=(1,2,1),size=1)
from bpy import context

import builtins as __builtin__

def console_print(*args, **kwargs):
    for a in context.screen.areas:
        if a.type == 'CONSOLE':
            c = {}
            c['area'] = a
            c['space_data'] = a.spaces.active
            c['region'] = a.regions[-1]
            c['window'] = context.window
            c['screen'] = context.screen
            s = " ".join([str(arg) for arg in args])
            for line in s.split("\n"):
                bpy.ops.console.scrollback_append(c, text=line)

def print(*args, **kwargs):
    """Console print() function."""

    console_print(*args, **kwargs)
    __builtin__.print(*args, **kwargs)




def select_obj(obj):
    objectToSelect = bpy.data.objects[obj]
    objectToSelect.select_set(True)    
    bpy.context.view_layer.objects.active = objectToSelect


def color_converter(r,g,b,alpha=1):
    return r/255,g/255,b/255,alpha




def set_material(obj,index):
    matg = bpy.data.materials.new(Block_name[index])
    matg.use_nodes = True
    
    tree = matg.node_tree
    nodes = tree.nodes
    bsdf = nodes["Principled BSDF"]
    
    bsdf.inputs[0].default_value=color_converter(rgb_palet[index][0],rgb_palet[index][1],rgb_palet[index][2])
    
    obj.active_material = matg
        
    

rgb_palet=[(255,0,0)]
Block_palet=[3]
Block_name=["Stone"]


data=[[[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 49, 3, 3, 3], [49, 89, 89, 49, 89, 89, 49], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [89, 89, 41, 49, 41, 89, 89], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [89, 41, 41, 49, 41, 41, 89], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[3, 3, 3, 152, 3, 3, 3], [49, 3, 3, 152, 3, 3, 3], [49, 49, 49, 57, 49, 49, 49], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [89, 41, 41, 49, 41, 41, 89], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 89], [89, 89, 41, 49, 41, 89, 89], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 49, 3, 89, 3], [49, 89, 89, 49, 89, 89, 49], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]]

todo_list_x=[]
todo_list_y=[]
todo_list_z=[]
color=[]
idCube=[]
idNow=0
try:
    for z in range(len(data[0])):
        for y in range(len(data[z])):
            for x in range(len(data[z][y])):
                if data[z][y][x] != 0:
                    todo_list_x.append(x)
                    todo_list_z.append(z)
                    todo_list_y.append(y)
                    color.append(data[z][y][x])
                    idCube.append(idNow)
                    idNow+=1
                   
except:
    None
todo_list=[]


for i in range(len(todo_list_x)):
    bpy.ops.mesh.primitive_cube_add(location=(todo_list_x[i],todo_list_z[i],todo_list_y[i]),size=1)
    bpy.context.active_object.select_set(False)



for colorId in set(color):
    for _,i in enumerate(idCube):
        if colorId == color[_]:
            if idCube[_] == 0:
                select_obj(f"Cube")
            elif idCube[_] < 10:
                select_obj(f"Cube.00{_}")
            elif idCube[_] >= 10 and idCube[_]<100:
                select_obj(f"Cube.0{_}")
            elif idCube[_] >= 100:
                select_obj(f"Cube.{_}")
    
    Geg=False
    for index in range(len(Block_palet)):
        if Block_palet[index] == colorId:
            bpy.ops.object.join()
            set_material(bpy.context.active_object,index)
            bpy.context.active_object.select_set(False)
            Geg=True
    
    if not Geg:
        bpy.ops.object.join()
        bpy.context.active_object.select_set(False)

      