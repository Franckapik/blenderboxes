from bpy.types import Panel, Menu, Operator
import bpy
from bl_operators.presets import AddPresetBase

from bpy.props import FloatProperty, StringProperty, PointerProperty, CollectionProperty
from bpy.types import PropertyGroup

import boxes  # in blender scripts/startup
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
        generators = scene.generators

        boxe = generators.UBox
        box_attributes_names = tuple(
            p for p in boxe.bl_rna.properties.keys() if p not in {"rna_type", "name", "positional arguments"}
        )

        for ( attributeName ) in box_attributes_names:  # ABox Settings / Default Settings / ...
            box = layout.box()
            box.label(text=attributeName)

            box_group_attributes = getattr(boxe, attributeName)
            group_params_name = tuple( p for p in box_group_attributes.bl_rna.properties.keys() if p not in {"rna_type", "name"} )

            for paramName in group_params_name:  # Title / Category
                box.prop(box_group_attributes, paramName)


ui_classes = [Diffuseur_SideBar]


def register():
    for cls in ui_classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in ui_classes:
        bpy.utils.unregister_class(cls)
