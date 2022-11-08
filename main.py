import bpy
from bpy import context
import builtins as __builtin__

data = [[[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 49, 3, 3, 3], [49, 89, 89, 49, 89, 89, 49], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [89, 89, 41, 49, 41, 89, 89], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [89, 41, 41, 49, 41, 41, 89], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[3, 3, 3, 152, 3, 3, 3], [49, 3, 3, 152, 3, 3, 3], [49, 49, 49, 57, 49, 49, 49], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [89, 41, 41, 49, 41, 41, 89], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 89], [89, 89, 41, 49, 41, 89, 89], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 49, 3, 89, 3], [49, 89, 89, 49, 89, 89, 49], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]]
         



Rgb_Palet = [(138, 138, 138),(255,0,0),(230,230,70),(36,34,47),(240,214,165),(141,224,212)]
Block_Palet = [3,152,41,49,89,57]
Block_Name = ["Stone","RedStone","Gold","Obsidian","GlowStone","Diamond"]




def console_print(*args, **kwargs):
    for a in context.screen.areas:
        if a.type == 'CONSOLE':
            c = {'area': a, 'space_data': a.spaces.active, 'region': a.regions[-1], 'window': context.window,
                 'screen': context.screen}
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


def color_converter(r, g, b, alpha=1):
    return r / 255, g / 255, b / 255, alpha


def set_material(obj, index):
    matg = bpy.data.materials.new(Block_Name[index])
    matg.use_nodes = True

    tree = matg.node_tree
    nodes = tree.nodes
    bsdf = nodes["Principled BSDF"]

    bsdf.inputs[0].default_value = color_converter(Rgb_Palet[index][0], Rgb_Palet[index][1], Rgb_Palet[index][2])

    obj.active_material = matg





Cordinate_List=[]
Id_Block = []
Id_Cube = []
Count=0

for z in range(len(data[0])):
    for y in range(len(data[z])):
        for x in range(len(data[z][y])):
            if data[z][y][x] != 0:
                Cordinate_List.append((x,z,y))
                Id_Block.append(data[z][y][x])
                Id_Cube.append(Count)
                Count+=1

for i in range(len(Cordinate_List)):
    bpy.ops.mesh.primitive_cube_add(location=(Cordinate_List[i][0], Cordinate_List[i][1], Cordinate_List[i][2]), size=1)
    bpy.context.active_object.select_set(False)

for Id_Color in set(Id_Block):
    for _, i in enumerate(Id_Cube):
        if Id_Color == Id_Block[_]:
            if Id_Cube[_] == 0:
                select_obj(f"Cube")
            elif Id_Cube[_] < 10:
                select_obj(f"Cube.00{_}")
            elif 10 <= Id_Cube[_] < 100:
                select_obj(f"Cube.0{_}")
            elif Id_Cube[_] >= 100:
                select_obj(f"Cube.{_}")

    TempVarible = False
    for index in range(len(Block_Palet)):
        if Block_Palet[index] == Id_Color:
            bpy.ops.object.join()
            set_material(bpy.context.active_object, index)
            bpy.context.active_object.select_set(False)
            TempVarible = True

    if not TempVarible:
        bpy.ops.object.join()
        bpy.context.active_object.select_set(False)