import bpy
import sys

sys.path.insert(1,"/home/fanch/Documents/blenderboxes/boxes")

import boxes #in blender scripts/startup
import boxes.generators

from bpy.props import (
    FloatProperty,
    BoolProperty,
    IntProperty,
    FloatVectorProperty,
    EnumProperty,
)

productType = (
    ("0", "Diffuseur 2D", ""),
    ("1", "Diffuseur 1D", ""),
    ("2", "Absorbeur", ""),
    ("3", "Moule", ""),
)

available_objects = []


def listGenerators():
    all_generators = boxes.generators.getAllBoxGenerators()
    for index, gen in enumerate(all_generators):
        name = gen.split('.')[-1].lower()
        available_objects.append((str(index), name, ""))  
    return available_objects  

   
""" class TestCase(bpy.types.Operator):  
   
 bl_idname = "object.testcase"  
 bl_label = "TestCase"  
 bl_options = {'REGISTER', 'UNDO'}  
  
 objects = EnumProperty(name="Objects", items = availableObjects) 
 """


class generatorProps(bpy.types.PropertyGroup):
    generators: EnumProperty(name="Generators",items=listGenerators())
    


class Usinageprops(bpy.types.PropertyGroup):
    fraise: FloatProperty(
        name="Fraise diametre",
        description="Diametre de la fraise",
        default=0.005,
        step=0.001,
        unit="LENGTH",
        precision=4,
    )
    offset: EnumProperty(
        name="Offset %",
        items=(
            ("0", "Aucune", ""),
            ("0.05", "5%", ""),
            ("0.10", "10%", ""),
            ("0.20", "20%", ""),
            ("0.30", "30%", ""),
            ("0.50", "50%", ""),
        ),
    )
    

    def getOffset(self):
        offset = float(self.offset) * float(self.fraise)
        return round(offset, 4)
        


    def listAttributes(self):
        return [
            "fraise",
            "offset",
            "offset_peigne",
        ]



classes = [
    generatorProps,
    Usinageprops,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.generatorProps = bpy.props.PointerProperty(type=generatorProps)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.generatorProps
