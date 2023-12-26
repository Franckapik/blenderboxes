import bpy
import boxes  # in blender scripts/startup
import boxes.generators

import argparse

d = ["p1", "p2"]

for prop in d:
    setattr(bpy.types.Scene, prop, bpy.props.IntProperty(default=2))


""" class MyPropGroup(bpy.types.PropertyGroup):
    pass """

MyPropGroup = type(
    "MyPropGroup2",
    (bpy.types.PropertyGroup,),
    {"myfloat": bpy.props.IntProperty(name="myfloat", default=2)},
)


bpy.utils.register_class(MyPropGroup)


for i in range(10):
    setattr(MyPropGroup, "p" + str(i), bpy.props.FloatProperty(default=i))

    """ name = "prop"+ str(i)
    
    groupProp = type(name,
                   (bpy.types.PropertyGroup, ),
                   {"myfloat" : bpy.props.IntProperty(name="myfloat", default=i)}
                   )
    
    
    setattr(bpy.types.Scene, name,  groupProp ) """

setattr(bpy.types.Scene, "propGroup", bpy.props.PointerProperty(type=MyPropGroup))

###############

allGen = boxes.generators.getAllBoxGenerators()
ess = {name.split(".")[-1].lower(): generator for name, generator in allGen.items()}
listboxes = list(ess.values())


class Generators(bpy.types.PropertyGroup):
        pass 
    
bpy.utils.register_class(Generators)

for box in listboxes:

    class MyBox(bpy.types.PropertyGroup):
        pass 
    
    bpy.utils.register_class(MyBox)


    listeArguments = []
    for group in box().argparser._action_groups:
        class MyGroup(bpy.types.PropertyGroup):
            pass 
    
        bpy.utils.register_class(MyGroup)

        argument = {}
        #cmt faire pour plusieurs group ? group1 group2 etc ? Un autre PropGroup? 
        argument["group"] = group.title

        listParams = []
        for param in group._group_actions:
            paramObj = {}
            dest = param.dest
            type = param.type
            default = param.default
            if not (
                isinstance(param, argparse._HelpAction)
                and isinstance(param, argparse._StoreAction)
            ):
                match dest:
                    case "input" | "output" | "format" | "layout":
                        pass
                    case _:
                        paramObj["dest"] = dest
                        paramObj["type"] = type

                        if type is float:
                            setattr(MyGroup, dest, bpy.props.FloatProperty(default=float(default)))
                        if type is int:
                            setattr(MyGroup, dest, bpy.props.IntProperty(default=default))
                        if type is str:
                            if param.choices:
                                list_of_choices = []
                                default_index = 0
                                for index , choice in enumerate(param.choices):
                                    list_of_choices.append((str(index), choice, ""))
                                    if choice == default:
                                        default_index = index
                                setattr(MyGroup, dest, bpy.props.EnumProperty(items=list_of_choices, default=default_index))

                            else :
                                setattr(MyGroup, dest, bpy.props.StringProperty(default=default))

                        if isinstance(type, boxes.BoolArg):
                            setattr(MyGroup, dest, bpy.props.BoolProperty(default=bool(default)))
        setattr(MyBox, group.title, bpy.props.PointerProperty(type=MyGroup))


    setattr(Generators, box.__name__, bpy.props.PointerProperty(type=MyBox))
setattr(bpy.types.Scene, 'generators', bpy.props.PointerProperty(type=Generators))

