from bpy.types import Panel, Menu, Operator
import bpy
from bl_operators.presets import AddPresetBase

from bpy.props import FloatProperty, StringProperty, PointerProperty, CollectionProperty
from bpy.types import PropertyGroup

import boxes #in blender scripts/startup
import boxes.generators

class Diffuseur_SideBar(Panel):
    """Diffuseur options panel"""

    bl_label = "Boxes"
    bl_idname = "BOXES_PT_Boxes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Boxes"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        generatorProps = scene.generatorProps

        row1 = layout.row(align=True)
        row1.label(text="Boxes")

        box1 = layout.box()
        box1.label(text="Usinage", icon="X")
        
        box2 = layout.box()
        box2.label(text="2eme Box", icon="X")
        box2.prop(generatorProps, "generators")

        listeArguments = generatorProps.getArgs()

        for group in listeArguments:
            box=layout.box()
            box.label(text=group['group']) 
            if group['params'] != None : 
                for param in group['params'] :
                    row = box.row()

                    row.label(text=param['dest'])
                    row.label(text=str(param['type']))

                    particle = scene.particle_instancer
                   
                    if param['type'] is float :
                        self.layout.prop(bpy.context.scene,"my_float")

# Assign a collection.
class SceneSettingItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Test Property", default="Unknown")
    value: bpy.props.IntProperty(name="Test Property", default=22)



ui_classes = [Diffuseur_SideBar]

def register():

    bpy.types.Scene.my_float = bpy.props.FloatProperty(default=0)

    for cls in ui_classes:
        bpy.utils.register_class(cls)
    

def unregister():
    for cls in ui_classes:
        bpy.utils.unregister_class(cls)
