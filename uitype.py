import bpy
from bpy.props import FloatProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup

# TODO: load dynamically at runtime from a JSON file!
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

class SamplePanel(bpy.types.Panel):
    bl_label = "Boxes"
    bl_idname = "BOXES_PT_Boxes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Boxes"



    def draw(self, context):
        layout = self.layout
        obj = context.scene

        # use our layout definition to dynamically create our panel items
        for groupName, attributeDefinitions in bpy.propertyGroupLayouts.items():
            # get the instance of our group
            # dynamic equivalent of `obj.samplePropertyGroup` from before
            propertyGroup = getattr(obj, groupName)

            


            # start laying this group out
            col = layout.column()
            col.label(text=groupName)


            # loop through all the attributes and show them
            for attributeDefinition in attributeDefinitions:
                col.prop(propertyGroup, attributeDefinition["name"])

                pass
            # draw a separation between groups
            layout.separator()

def register():
    # register the panel class
    bpy.utils.register_class(SamplePanel)

    # iterate over our list of property groups
    for groupName, attributeDefinitions in bpy.propertyGroupLayouts.items():
        # build the attribute dictionary for this group
        attributes = {}
        for attributeDefinition in attributeDefinitions:
            attType = attributeDefinition['type']
            attName = attributeDefinition['name']
            if attType == 'float':
                attributes[attName] = FloatProperty(name=attName.title(), default=5)
            elif attType == 'string':
                attributes[attName] = StringProperty(name=attName.title(), default="cooucou")
            else:
                raise TypeError('Unsupported type (%s) for %s on %s!' % (attType, attName, groupName))

        # now build the property group class
        propertyGroupClass = type(groupName, (PropertyGroup,), attributes)

        # register it with Blender
        bpy.utils.register_class(propertyGroupClass)

        # apply it to all Objects
        setattr(bpy.types.Scene, groupName, PointerProperty(type=propertyGroupClass))

        # store it for later
        bpy.samplePropertyGroups[groupName] = propertyGroupClass

def unregister():
    # unregister the panel class
    bpy.utils.unregister_class(SamplePanel)

    # unregister our components
    try:
        for key, value in bpy.samplePropertyGroups.items():
            delattr(bpy.types.Scene, key)
            bpy.utils.unregister_class(value)
    except UnboundLocalError:
        pass
    bpy.samplePropertyGroups = {}