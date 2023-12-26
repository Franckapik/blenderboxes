from bpy.types import Panel, Menu, Operator
import bpy
from bl_operators.presets import AddPresetBase

from bpy.props import FloatProperty, StringProperty, PointerProperty, CollectionProperty, EnumProperty

import boxes  # in blender scripts/startup
import boxes.generators
import bpy, os
from bpy.types import (
    Operator,
    Panel,
    PropertyGroup,
)

import bpy.utils.previews
from bpy.types import WindowManager

def enum_previews_from_directory_items(self, context):

    
    #Extensions
    extensions = ('.jpeg', '.jpg', '.png')

    blend_dir = os.path.dirname(bpy.data.filepath)
    filename = bpy.path.abspath("boxes_pkg/static/samples")
    blenddir = bpy.path.abspath('//')

    userdir = bpy.utils.resource_path('USER')
    mypath  = os.path.join(blenddir,"boxes_pkg/static/samples")


    # Icons Directory    

    icons_dir = os.path.dirname(__file__)
    directory = os.path.join(icons_dir, "boxes_pkg/static/samples")

    enum_items = []

    if context is None:
        return enum_items

    pcoll = preview_collections["main"]

    if directory == pcoll.my_previews_dir:
        return pcoll.my_previews

    if directory and os.path.exists(directory):
        # Scan the directory for png files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(extensions):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            icon = pcoll.get(name)
            if filepath in pcoll:
                enum_items.append((name, name, "", pcoll[filepath].icon_id, i))
            else:
                thumb = pcoll.load(filepath, filepath, 'IMAGE')
                enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.my_previews = enum_items
    pcoll.my_previews_dir = directory
    return pcoll.my_previews


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

        wm = context.window_manager

        row = layout.row()
        row.template_icon_view(wm, "my_previews", show_labels=True)


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

preview_collections = {}


def register():
    for cls in ui_classes:
        bpy.utils.register_class(cls)
    
    WindowManager.my_previews_dir = StringProperty(
    name="Folder Path",
    subtype='DIR_PATH',
    default=""
    )

    WindowManager.my_previews = EnumProperty(
        items=enum_previews_from_directory_items,
    )

    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()

    preview_collections["main"] = pcoll


def unregister():
    for cls in ui_classes:
        bpy.utils.unregister_class(cls)
    
        del WindowManager.my_previews

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    del bpy.types.Scene.my_tool

