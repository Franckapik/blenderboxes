from bpy.types import Panel, Menu, Operator
import bpy
from bl_operators.presets import AddPresetBase

from bpy.props import FloatProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup

bpy.propertyGroupLayouts = {
    "Health": [
        { "name": "current", "type": "float" },
        { "name": "max", "type": "float" }
    ],
    "Character": [
        { "name": "first_name", "type": "string" },
        { "name": "last_name", "type": "string" }
    ]
}
bpy.samplePropertyGroups = {}


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
        wm = context.window_manager

        row1 = layout.row(align=True)
        row1.label(text="Boxes")

        box1 = layout.box()
        box1.label(text="Usinage", icon="X")
        
        box2 = layout.box()
        box2.label(text="2eme Box", icon="X")
        box2.prop(generatorProps, "generators")

        """ tex = bpy.data.textures['nameOfTexture']
        col = layout.box().column()
        col.template_preview(tex) """


        #dynamic
        obj = context.object

        # use our layout definition to dynamically create our panel items
        for groupName, attributeDefinitions in bpy.propertyGroupLayouts.items():
            # get the instance of our group
            # dynamic equivalent of `obj.samplePropertyGroup` from before
            propertyGroup = getattr(obj, groupName)
            print(groupName)
            # start laying this group out
            col = layout.column()
            col.label(text="Hello")

            # loop through all the attributes and show them
            for attributeDefinition in attributeDefinitions:
                col.prop(propertyGroup, attributeDefinition["name"])

            # draw a separation between groups
            layout.separator()


ui_classes = [Diffuseur_SideBar]

def register():
    for cls in ui_classes:
        bpy.utils.register_class(cls)
    
    #dynamic
    
    # iterate over our list of property groups
    for groupName, attributeDefinitions in bpy.propertyGroupLayouts.items():
        # build the attribute dictionary for this group
        attributes = {}
        for attributeDefinition in attributeDefinitions:
            attType = attributeDefinition['type']
            attName = attributeDefinition['name']
            if attType == 'float':
                attributes[attName] = FloatProperty(name=attName.title())
            elif attType == 'string':
                attributes[attName] = StringProperty(name=attName.title())
            else:
                raise TypeError('Unsupported type (%s) for %s on %s!' % (attType, attName, groupName))

        # now build the property group class
        propertyGroupClass = type(groupName, (PropertyGroup,), attributes)

        # register it with Blender
        bpy.utils.register_class(propertyGroupClass)

        # apply it to all Objects
        setattr(bpy.types.Object, groupName, PointerProperty(type=propertyGroupClass))

        # store it for later
        bpy.samplePropertyGroups[groupName] = propertyGroupClass


def unregister():
    for cls in ui_classes:
        bpy.utils.unregister_class(cls)
