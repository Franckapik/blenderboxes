import bpy
import sys

sys.path.insert(1, "/home/fanch/Documents/blenderboxes/boxes")

import boxes  # in blender scripts/startup
import boxes.generators

import argparse


from bpy.props import (
    FloatProperty,
    BoolProperty,
    IntProperty,
    FloatVectorProperty,
    StringProperty,
    EnumProperty,
    CollectionProperty,
)

productType = (
    ("0", "Diffuseur 2D", ""),
    ("1", "Diffuseur 1D", ""),
    ("2", "Absorbeur", ""),
    ("3", "Moule", ""),
)


def listGenerators():
    genByName = []

    all_generators = boxes.generators.getAllBoxGenerators()
    for index, gen in enumerate(all_generators):
        name = gen.split(".")[-1].lower()
        genByName.append((str(index), name, ""))
    return genByName


def listArgs(box):
    listeArguments = []
    for group in box.argparser._action_groups:
        argument = {}
        argument["group"] = group.title
        listParams = []
        for param in group._group_actions:
            paramObj = {}
            dest = param.dest
            type = param.type
            if not (
                isinstance(param, argparse._HelpAction)
                and isinstance(param, argparse._StoreAction)
            ):
                match dest:
                    case "input" | "output" | "format" | "layout"  :
                        pass
                    case _:
                        paramObj["dest"] = dest
                        paramObj["type"] = type
                        
                        if param.choices:
                            uniqueChoices = []
                            for option in param.choices:
                                if option not in uniqueChoices:
                                    uniqueChoices.append(option)
                            paramObj["options"] = uniqueChoices
                        else:
                            paramObj["options"] = None
                        listParams.append(paramObj)
        argument["params"] = listParams if len(listParams) > 1 else None
        listeArguments.append(argument)

    return listeArguments


""" class TestCase(bpy.types.Operator):  
   
 bl_idname = "object.testcase"  
 bl_label = "TestCase"  
 bl_options = {'REGISTER', 'UNDO'}  
  
 objects = EnumProperty(name="Objects", items = availableObjects) 
 """


class generatorProps(bpy.types.PropertyGroup):
    generators: EnumProperty(name="Generators", items=listGenerators())

    def getGenById(self):
        return listGenerators()[int(self.generators)]

    def allGen(self):
        allGen = boxes.generators.getAllBoxGenerators()
        return {
            name.split(".")[-1].lower(): generator for name, generator in allGen.items()
        }

    def getArgs(self):
        box = list(self.allGen().values())[int(self.generators)]()
        return listArgs(box)
        


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
