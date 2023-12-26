""" bl_info = {
    "name": "Add Object",
    "author": "Rakesh",
    "version": (1, 0, 0),
    "blender": (2, 83, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "category": "Add Mesh",
}

 """
import bpy, os
from bpy.types import (
    Operator,
    Panel,
    PropertyGroup,
)
from bpy.props import *
import bpy.utils.previews
from bpy.types import WindowManager


def update_category(self, context):
    enum_previews_from_directory_items(self, context)


class Categories(PropertyGroup):
    mesh_options = [
        ("Objects", "Objects", '', 0),

    ]

    cat: bpy.props.EnumProperty(

        items=mesh_options,
        description="Select a Category",
        default="Objects",
        update=update_category
    )


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


class PreviewsExamplePanel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Add object Panel"
    bl_idname = "OBJECT_PT_previews"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.template_icon_view(wm, "my_previews", show_labels=True)



# We can store multiple preview collections here,
# however in this example we only store "main"
preview_collections = {}


def register():

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

    bpy.utils.register_class(PreviewsExamplePanel)


def unregister():

    del WindowManager.my_previews

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    bpy.utils.unregister_class(PreviewsExamplePanel)


if __name__ == "__main__":
    register()