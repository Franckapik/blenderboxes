from bpy.types import Panel, Menu, Operator
import bpy
from .ops import classes
from bl_operators.presets import AddPresetBase


class DIF_MT_Presets(Menu):
    bl_label = "Diffuseurs Presets"
    preset_subdir = "object/display"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


# Enregistrement du preset dans le fichier suivant
# /home/fanch/.config/blender/3.6/scripts/presets/object/display/


class OT_AddMyPreset(AddPresetBase, Operator):
    bl_idname = "my.add_preset"
    bl_label = "Ajouter un preset"
    preset_menu = "DIF_MT_Presets"
    # Common variable used for all preset values
    preset_defines = ["obj = bpy.context.object", "scene = bpy.context.scene"]
    # Properties to store in the preset
    preset_values = [
        "scene.dif_props",
        "scene.array_props",
        "scene.pos_props",
        "scene.prep_props",
        "scene.product_props",
        "scene.usinage_props",
    ]
    # Directory to store the presets
    preset_subdir = "object/display"
    


class Diffuseur_SideBar(Panel):
    """Diffuseur options panel"""

    bl_label = "Diffuseurs"
    bl_idname = "DIFFUSEURS_PT_Diffuseurs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DIFFUSEURS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        difprops = scene.dif_props
        arrayprops = scene.array_props
        posprops = scene.pos_props
        prepprops = scene.prep_props
        productprops = scene.product_props
        usinageprops = scene.usinage_props

        # presets
        row1 = layout.row(align=True)
        row1.menu(DIF_MT_Presets.__name__, text=DIF_MT_Presets.bl_label)
        row1.operator(OT_AddMyPreset.bl_idname, text="", icon="ADD")
        row1.operator(
            OT_AddMyPreset.bl_idname, text="", icon="REMOVE"
        ).remove_active = True

        # Diffuseur name
        box = layout.box()
        box.label(text="Usinage ", icon="X")
        for att in (x for x in usinageprops.listAttributes()):
            box.prop(usinageprops, att)
        box.prop(difprops, "offset_peigne")
        
        box.label(text=f"Offset de fraise : {usinageprops.getOffset() * 1000} mm")
        box.label(text=f"Offset des peignes : {difprops.getOffsetPeigne() * 1000} mm")

        # Dimensions
        layout.separator()
        box = layout.box()
        box.label(
            text="Dimensions : "
            + (
                "D2"
                if productprops.product_type == "0"
                else "D1"
                if productprops.product_type == "1"
                else "A"
                if productprops.product_type == "2"
                else "M"
            )
            + difprops.getDifName(),
            icon="X",
        )
        row = box.row()
        row.prop(productprops, "product_type", expand=True)
        for att in (x for x in difprops.listAttributes(productprops.product_type)):
            box.prop(difprops, att)
        box.label(text=f"Rang : {difprops.getRang() * 1000} mm")
        box.label(text=f"Pilier : {difprops.getLargeurPilier() * 1000} mm")

        # Array
        layout.separator()
        box = layout.box()
        box.label(text="Array", icon="X")
        box.prop(arrayprops, "array_offset")
        split = box.split()
        col1 = split.column()
        col2 = split.column()
        col1.label(
            text="X count",
        )
        col2.label(text="Y count")
        for arr in (
            x
            for x in arrayprops.listAttributes(productprops.product_type)
            if x != "array_offset"
        ):
            if arr[-1] == "x":
                col1.prop(arrayprops, arr)
            if arr[-1] == "y":
                col2.prop(arrayprops, arr)

        # Generateur
        layout.separator()
        box = layout.box()
        box.label(text="Générateur", icon="X")

        cursor = bpy.context.scene.cursor.location
        box.label(
            text=f"Cursor 3D : X{round(cursor[0], 2)}  Y{round(cursor[1], 2)}  Z{round(cursor[2], 2)}"
        )

        for piece in posprops.listAttributes(productprops.product_type):
            row = box.row()
            if "_position" in piece:
                row.prop(posprops, piece)
                op = row.operator("mesh.pick_position", text="", icon="EYEDROPPER")
                op.cursor = cursor
                op.target = piece
                row.prop(
                    posprops,
                    piece.replace("_position", "_rotation"),
                    icon="EVENT_R",
                    text="",
                )
                row.operator(
                    f"mesh.{piece.replace('_position', '')}", text="", icon="ADD"
                )

        match productprops.product_type:
            case "0":
                box.operator("mesh.add_diffuseur")
            case "1":
                box.operator("mesh.add_diffuseur")
            case "2":
                box.operator("mesh.add_absorbeur")
            case "3":
                box.operator("mesh.add_moule")

        # Prepare to Cam
        layout.separator()
        box = layout.box()
        box.label(text="Préparation CAM", icon="X")

        row = box.row()
        row.prop(prepprops, "selection_prepare", expand=True)

        box.prop(prepprops, "isNewMesh_prepare")

        if prepprops.isNewMesh_prepare:
            box.prop(prepprops, "isDeleteOldMesh_prepare")
        """ else:
            prepprops.isDeleteOldMesh_prepare = False """

        box.prop(prepprops, "isConvertToCurve_prepare")
        if prepprops.isConvertToCurve_prepare:
            box.prop(prepprops, "isCRemove_prepare")

            if prepprops.isJoin_prepare:
                box.prop(prepprops, "isOvercuts")

        box.prop(prepprops, "isJoin_prepare")

        box.operator("mesh.prepare_cam")

        # Motif
        layout.separator()
        box = layout.box()
        box.label(text="Motif", icon="X")


        box.prop(difprops, "decalage_h")
        box.prop(difprops, "decalage_v")

        ratio = difprops.getRatio()

        for i in range(difprops.type):
            row = box.row()
            split = box.split()
            for k in range(difprops.type):
                
                col = split.column()
                col.label(text=str(
                    int(ratio[i*difprops.type + k] * 1000)
                    
                    ))


ui_classes = [DIF_MT_Presets, OT_AddMyPreset]


def menu_func(self, context):
    for cls in classes:
        self.layout.operator(cls.bl_idname, icon="MESH_CUBE")


def register():
    for cls in ui_classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_class(Diffuseur_SideBar)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    for cls in ui_classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(Diffuseur_SideBar)
