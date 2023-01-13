import bpy
from bpy.types import Panel

class REDLINE_INTERLINK_PT_panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Redline Interlink"
    bl_category = "Redline Devtool"

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.scene, "redline_project_root")
        layout.operator("redline.interlink_op_updateasset")
        layout.operator("redline.interlink_op_previewasset")

class REDLINE_INTERLINK_PT_properties_collection_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"
    bl_label = "Redline Prefab Data"
    bl_category = "Redline Devtool"

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.collection.redline_prefab, "include")
        layout.prop(bpy.context.collection.redline_prefab, "composite")

class REDLINE_INTERLINK_PT_properties_object_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_label = "Redline Object Data"
    bl_category = "Redline Devtool"

    def draw(self, context):
        layout = self.layout
        if bpy.context.object.instance_collection is not None:
            layout.prop(bpy.context.object.redline_prefab_instance, "copy_mode")
            layout.prop(bpy.context.object.redline_prefab_instance, "stream_mode")
            layout.prop(bpy.context.object.redline_prefab_instance, "composite")
        else:
            object_panel = layout.box()
            object_panel.label(text="Object")
            object_panel.prop(bpy.context.object.redline_object, "renderable")
            object_panel.prop(bpy.context.object.redline_object, "cast_shadow")
            object_panel.prop(bpy.context.object.redline_object, "dynamic")
            object_panel.prop(bpy.context.object.redline_object, "request_planar_reflection")
            object_panel.prop(bpy.context.object.redline_object, "emissive_color")
            object_panel.prop(bpy.context.object.redline_object, "shadow_cascade_mask")

            layout.prop(bpy.context.object.redline_decal, "is_set", text="Is Decal")
            if bpy.context.object.redline_decal.is_set is True:
                decal_panel = layout.box()
                decal_panel.label(text="Decal")
                decal_panel.prop(bpy.context.object.redline_decal,"material")

            script_panel = layout.box()
            script_panel.label(text="Script")
            script_panel.prop(bpy.context.object, "redline_script", text="Script File")

class REDLINE_INTERLINK_PT_properties_obdata_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_label = "Redline Data"
    bl_category = "Redline Devtool"

    def draw(self, context):
        layout = self.layout
        if bpy.context.object.data.redline_mesh is not None:
            layout.label(text="Mesh Data")
            layout.prop(bpy.context.mesh.redline_mesh, "lod_mode")

class REDLINE_INTERLINK_PT_properties_physics_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "physics"
    bl_label = "Redline Physics Data"
    bl_category = "Redline Devtool"

    def draw(self, context):
        layout = self.layout
        if bpy.context.object.rigid_body is not None:
            rb_extent_panel = layout.box()
            rb_extent_panel.label(text="Rigid Body Data")
            rb_extent_panel.prop(bpy.context.object,"redline_rb_extents")

        layout.prop(bpy.context.object.redline_collider,"is_set")
        if bpy.context.object.redline_collider.is_set is True:
            collider_panel = layout.box()
            collider_panel.label(text="Collider Data")
            collider_panel.prop(bpy.context.object.redline_collider, "shape")
            collider_panel.prop(bpy.context.object.redline_collider, "radius")
            collider_panel.prop(bpy.context.object.redline_collider, "offset")
            collider_panel.prop(bpy.context.object.redline_collider, "tail")
            collider_panel.prop(bpy.context.object.redline_collider, "set_CPU_enabled")
            collider_panel.prop(bpy.context.object.redline_collider, "set_GPU_enabled")

classes = (
    REDLINE_INTERLINK_PT_panel,
    REDLINE_INTERLINK_PT_properties_collection_panel,
    REDLINE_INTERLINK_PT_properties_object_panel,
    REDLINE_INTERLINK_PT_properties_obdata_panel,
    REDLINE_INTERLINK_PT_properties_physics_panel
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)