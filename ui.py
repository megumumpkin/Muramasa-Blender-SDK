import bpy
from bpy.types import Panel

class MURAMASA_INTERLINK_PT_panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Muramasa Asset IO"
    bl_category = "Muramasa SDK"

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.scene, "muramasa_project_root")
        layout.operator("muramasa.interlink_op_updateasset")
        layout.operator("muramasa.interlink_op_previewasset")

class MURAMASA_INTERLINK_PT_properties_collection_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"
    bl_label = "Muramasa Prefab Data"
    bl_category = "Muramasa Devtool"

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.collection.muramasa_prefab, "include")
        layout.prop(bpy.context.collection.muramasa_prefab, "composite")
        if bpy.context.collection.muramasa_prefab.composite is True:
            compdata_panel = layout.box()
            compdata_panel.label(text="Composite Prefab Instance Data")
            compdata_panel.prop(bpy.context.collection.muramasa_prefab.composite_data, "copy_mode")
            compdata_panel.prop(bpy.context.collection.muramasa_prefab.composite_data, "stream_mode")
            compdata_panel.prop(bpy.context.collection.muramasa_prefab.composite_data, "bound_mul")

class MURAMASA_INTERLINK_PT_properties_object_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_label = "Muramasa Object Data"
    bl_category = "Muramasa Devtool"

    def draw(self, context):
        layout = self.layout
        if bpy.context.object.instance_collection is not None:
            layout.prop(bpy.context.object.muramasa_prefab_instance, "copy_mode")
            layout.prop(bpy.context.object.muramasa_prefab_instance, "stream_mode")
            layout.prop(bpy.context.object.muramasa_prefab_instance, "bound_mul")
        else:
            object_panel = layout.box()
            object_panel.label(text="Object")
            object_panel.prop(bpy.context.object.muramasa_object, "renderable")
            object_panel.prop(bpy.context.object.muramasa_object, "cast_shadow")
            object_panel.prop(bpy.context.object.muramasa_object, "dynamic")
            object_panel.prop(bpy.context.object.muramasa_object, "request_planar_reflection")
            object_panel.prop(bpy.context.object.muramasa_object, "emissive_color")
            object_panel.prop(bpy.context.object.muramasa_object, "shadow_cascade_mask")

            layout.prop(bpy.context.object.muramasa_layer, "is_set")
            if bpy.context.object.muramasa_layer.is_set is True:
                layer_panel = layout.box()
                layer_panel.label(text="Layer Mask")
                layer_panel.prop(bpy.context.object.muramasa_layer,"mask")

            layout.prop(bpy.context.object.muramasa_decal, "is_set", text="Is Decal")
            if bpy.context.object.muramasa_decal.is_set is True:
                decal_panel = layout.box()
                decal_panel.label(text="Decal")
                decal_panel.prop(bpy.context.object.muramasa_decal,"material")

            layout.prop(bpy.context.object.muramasa_emitter, "is_set", text="Is Emitter")
            if bpy.context.object.muramasa_emitter.is_set is True:
                emitter_panel = layout.box()
                emitter_panel.label(text="Emitter")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"material")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"shadertype")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"size")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"random_factor")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"normal_factor")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"count")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"life")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"random_life")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"scale")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"rotation")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"motion_blur_amount")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"mass")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"random_color")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"velocity")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"gravity")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"drag")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"restitution")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"sph_h")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"sph_K")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"sph_p0")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"sph_e")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"sprite_frames")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"sprite_framecount")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"sprite_framestart")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"sprite_framerate")

            script_panel = layout.box()
            script_panel.label(text="Script")
            script_panel.prop(bpy.context.object, "muramasa_script", text="Script File")

class MURAMASA_INTERLINK_PT_properties_material_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_label = "Muramasa Material Data"
    bl_category = "Muramasa Devtool"

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.material.muramasa_material, "shadow_cast")
        layout.prop(bpy.context.material.muramasa_material, "use_vertex_colors")
        layout.prop(bpy.context.material.muramasa_material, "workflow_specgloss")
        layout.prop(bpy.context.material.muramasa_material, "occlussion_primary")
        layout.prop(bpy.context.material.muramasa_material, "occlustion_secondary")
        layout.prop(bpy.context.material.muramasa_material, "use_wind")
        layout.prop(bpy.context.material.muramasa_material, "shadow_noreceive")
        layout.prop(bpy.context.material.muramasa_material, "outline")

        layout.prop(bpy.context.material.muramasa_material, "shading_rate")

        layout.prop(bpy.context.material.muramasa_material, "tex_anim_dir")
        layout.prop(bpy.context.material.muramasa_material, "tex_anim_framerate")
        layout.prop(bpy.context.material.muramasa_material, "tex_anim_elapsedtime")

class MURAMASA_INTERLINK_PT_properties_obdata_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_label = "Muramasa Data"
    bl_category = "Muramasa Devtool"

    def draw(self, context):
        layout = self.layout
        if bpy.context.object.data.muramasa_mesh is not None:
            layout.label(text="Mesh Data")
            layout.prop(bpy.context.mesh.muramasa_mesh, "lod_mode")

class MURAMASA_INTERLINK_PT_properties_physics_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "physics"
    bl_label = "Muramasa Physics Data"
    bl_category = "Muramasa Devtool"

    def draw(self, context):
        layout = self.layout
        if bpy.context.object.rigid_body is not None:
            rb_extent_panel = layout.box()
            rb_extent_panel.label(text="Rigid Body Data")
            rb_extent_panel.prop(bpy.context.object,"muramasa_rb_extents")

        layout.prop(bpy.context.object.muramasa_collider,"is_set")
        if bpy.context.object.muramasa_collider.is_set is True:
            collider_panel = layout.box()
            collider_panel.label(text="Collider Data")
            collider_panel.prop(bpy.context.object.muramasa_collider, "shape")
            collider_panel.prop(bpy.context.object.muramasa_collider, "radius")
            collider_panel.prop(bpy.context.object.muramasa_collider, "offset")
            collider_panel.prop(bpy.context.object.muramasa_collider, "tail")
            collider_panel.prop(bpy.context.object.muramasa_collider, "set_CPU_enabled")
            collider_panel.prop(bpy.context.object.muramasa_collider, "set_GPU_enabled")

class MURAMASA_INTERLINK_PT_properties_particle_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "particle"
    bl_label = "Muramasa VFX Data"
    bl_category = "Muramasa Devtool"

    def draw(self, context):
        layout = self.layout
        if bpy.context.particle_system.settings.type == 'HAIR':
            hpfs_panel = layout.box()
            hpfs_panel.label(text="Hair Particle Data")
            hpfs_panel.prop(bpy.context.particle_system.settings, "muramasa_hairparticle_distance")

classes = (
    MURAMASA_INTERLINK_PT_panel,
    MURAMASA_INTERLINK_PT_properties_collection_panel,
    MURAMASA_INTERLINK_PT_properties_object_panel,
    MURAMASA_INTERLINK_PT_properties_material_panel,
    MURAMASA_INTERLINK_PT_properties_obdata_panel,
    MURAMASA_INTERLINK_PT_properties_physics_panel,
    MURAMASA_INTERLINK_PT_properties_particle_panel
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)