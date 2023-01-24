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

            layout.prop(bpy.context.object.redline_layer, "is_set")
            if bpy.context.object.redline_layer.is_set is True:
                layer_panel = layout.box()
                layer_panel.label(text="Layer Mask")
                layer_panel.prop(bpy.context.object.redline_layer,"mask")

            layout.prop(bpy.context.object.redline_decal, "is_set", text="Is Decal")
            if bpy.context.object.redline_decal.is_set is True:
                decal_panel = layout.box()
                decal_panel.label(text="Decal")
                decal_panel.prop(bpy.context.object.redline_decal,"material")

            layout.prop(bpy.context.object.redline_emitter, "is_set", text="Is Emitter")
            if bpy.context.object.redline_emitter.is_set is True:
                emitter_panel = layout.box()
                emitter_panel.label(text="Emitter")
                emitter_panel.prop(bpy.context.object.redline_emitter,"material")
                emitter_panel.prop(bpy.context.object.redline_emitter,"shadertype")
                emitter_panel.prop(bpy.context.object.redline_emitter,"size")
                emitter_panel.prop(bpy.context.object.redline_emitter,"random_factor")
                emitter_panel.prop(bpy.context.object.redline_emitter,"normal_factor")
                emitter_panel.prop(bpy.context.object.redline_emitter,"count")
                emitter_panel.prop(bpy.context.object.redline_emitter,"life")
                emitter_panel.prop(bpy.context.object.redline_emitter,"random_life")
                emitter_panel.prop(bpy.context.object.redline_emitter,"scale")
                emitter_panel.prop(bpy.context.object.redline_emitter,"rotation")
                emitter_panel.prop(bpy.context.object.redline_emitter,"motion_blur_amount")
                emitter_panel.prop(bpy.context.object.redline_emitter,"mass")
                emitter_panel.prop(bpy.context.object.redline_emitter,"random_color")
                emitter_panel.prop(bpy.context.object.redline_emitter,"velocity")
                emitter_panel.prop(bpy.context.object.redline_emitter,"gravity")
                emitter_panel.prop(bpy.context.object.redline_emitter,"drag")
                emitter_panel.prop(bpy.context.object.redline_emitter,"restitution")
                emitter_panel.prop(bpy.context.object.redline_emitter,"sph_h")
                emitter_panel.prop(bpy.context.object.redline_emitter,"sph_K")
                emitter_panel.prop(bpy.context.object.redline_emitter,"sph_p0")
                emitter_panel.prop(bpy.context.object.redline_emitter,"sph_e")
                emitter_panel.prop(bpy.context.object.redline_emitter,"sprite_frames")
                emitter_panel.prop(bpy.context.object.redline_emitter,"sprite_framecount")
                emitter_panel.prop(bpy.context.object.redline_emitter,"sprite_framestart")
                emitter_panel.prop(bpy.context.object.redline_emitter,"sprite_framerate")

            script_panel = layout.box()
            script_panel.label(text="Script")
            script_panel.prop(bpy.context.object, "redline_script", text="Script File")

class REDLINE_INTERLINK_PT_properties_material_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_label = "Redline Material Data"
    bl_category = "Redline Devtool"

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.material.redline_material, "shadow_cast")
        layout.prop(bpy.context.material.redline_material, "use_vertex_colors")
        layout.prop(bpy.context.material.redline_material, "workflow_specgloss")
        layout.prop(bpy.context.material.redline_material, "occlussion_primary")
        layout.prop(bpy.context.material.redline_material, "occlustion_secondary")
        layout.prop(bpy.context.material.redline_material, "use_wind")
        layout.prop(bpy.context.material.redline_material, "shadow_noreceive")
        layout.prop(bpy.context.material.redline_material, "outline")

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

class REDLINE_INTERLINK_PT_properties_particle_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "particle"
    bl_label = "Redline VFX Data"
    bl_category = "Redline Devtool"

    def draw(self, context):
        layout = self.layout
        if bpy.context.particle_system.settings.type == 'HAIR':
            hpfs_panel = layout.box()
            hpfs_panel.label(text="Hair Particle Data")
            hpfs_panel.prop(bpy.context.particle_system.settings, "redline_hairparticle_distance")

classes = (
    REDLINE_INTERLINK_PT_panel,
    REDLINE_INTERLINK_PT_properties_collection_panel,
    REDLINE_INTERLINK_PT_properties_object_panel,
    REDLINE_INTERLINK_PT_properties_material_panel,
    REDLINE_INTERLINK_PT_properties_obdata_panel,
    REDLINE_INTERLINK_PT_properties_physics_panel,
    REDLINE_INTERLINK_PT_properties_particle_panel
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)