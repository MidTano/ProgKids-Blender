import bpy
from bpy import context
import builtins as __builtin__
import os.path
import random

data = [[[89, 49, 89], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[41, 49, 41], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[41, 49, 41], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[49, 57, 49], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[41, 49, 41], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[41, 49, 41], [0, 57, 0], [0, 57, 0], [0, 57, 0]], [[89, 49, 89], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[49, 49, 49], [0, 57, 0], [0, 57, 0], [0, 57, 0]]]



Rgb_Palet = [(138, 138, 138),(255,0,0),(230,230,70),(36,34,47),(240,214,165),(141,224,212),(0,255,0),(111,74,48)]
Block_Palet = [1,152,41,49,89,57,2,3]
Block_Name = ["Stone","RedStone","Gold","Obsidian","GlowStone","Diamond","Grass","Dirt"]


Obsidian={"color":"C:\\blender\\c.png","normal":"C:\\blender\\n.png","roughness":"C:\\blender\\r.png","metallic":"C:\\blender\\m.png"}


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
    """Select object"""
    objectToSelect = bpy.data.objects[obj]
    objectToSelect.select_set(True)
    bpy.context.view_layer.objects.active = objectToSelect


def color_converter(r:int, g:int, b:int, alpha:float=1):
    """Convert RBG to Blender Color"""
    return r / 255, g / 255, b / 255, alpha


def create_material(obj, index: int):
    """Create material using texture,if texture not set,use color_palet to create material"""
    matg = bpy.data.materials.new(Block_Name[index])
    
    color=None
    roughness=None
    normal=None
    metallic=None
    
    try:
        eval(Block_Name[index])
        try:color=eval(Block_Name[index])['color'];os.path.exists(color)
        except:pass
        try:roughness=eval(Block_Name[index])['roughness'];os.path.exists(roughness)
        except:pass
        try:normal=eval(Block_Name[index])['normal'];os.path.exists(normal)
        except:pass
        try:metallic=eval(Block_Name[index])['metallic'];os.path.exists(metallic)
        except:pass
    except:pass
    
    matg.use_nodes = True
    tree = matg.node_tree
    nodes = tree.nodes
    bsdf = nodes["Principled BSDF"]

    if color !=None and os.path.exists(color)==True:
        Color_map = matg.node_tree.nodes.new('ShaderNodeTexImage')
        Color_map.location = (-500, 550)
        Color_map.image = bpy.data.images.load(color)
        matg.node_tree.links.new(bsdf.inputs['Base Color'], Color_map.outputs['Color'])
    
    if roughness != None and os.path.exists(roughness)==True:
        Roughness_map = matg.node_tree.nodes.new('ShaderNodeTexImage')
        Roughness_map.location = (-500, 250)
        Roughness_map.image = bpy.data.images.load(roughness)
        matg.node_tree.links.new(bsdf.inputs['Roughness'], Roughness_map.outputs['Color'])
    if normal != None and os.path.exists(normal)==True:
        
        Normal_Map_Node=matg.node_tree.nodes.new('ShaderNodeNormalMap')
        Normal_Map_Node.location = (-200, -150)
        Normal_Map_Node.inputs[0].default_value = 1.15
        
        Normal_map = matg.node_tree.nodes.new('ShaderNodeTexImage')
        Normal_map.image = bpy.data.images.load(normal)
        Normal_map.location = (-500, -150)
        matg.node_tree.links.new(bsdf.inputs['Normal'], Normal_map.outputs['Color'])
        matg.node_tree.links.new(Normal_map.outputs['Color'],Normal_Map_Node.inputs['Color'])
        matg.node_tree.links.new(Normal_Map_Node.outputs['Normal'],bsdf.inputs['Normal'])
    if metallic != None:
        Metallic_map = matg.node_tree.nodes.new('ShaderNodeTexImage')
        Metallic_map.image = bpy.data.images.load(metallic)
        Metallic_map.location = (-500, -450)
        matg.node_tree.links.new(bsdf.inputs['Metallic'], Metallic_map.outputs['Color'])
    
    if not color and not roughness and not normal and not metallic:
        bsdf.inputs[0].default_value = color_converter(Rgb_Palet[index][0], Rgb_Palet[index][1], Rgb_Palet[index][2])
    
    return matg

def set_material(obj,material):
    obj.active_material = material



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
            set_material(obj=bpy.context.active_object,material=create_material(bpy.context.active_object, index))
            bpy.context.active_object.select_set(False)
            TempVarible = True

    if not TempVarible:
        bpy.ops.object.join()
        bpy.context.active_object.select_set(False)