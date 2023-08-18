import bpy
import os
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
        layout.prop(bpy.context.collection.muramasa_prefab, "is_main")
        layout.prop(bpy.context.collection.muramasa_prefab, "composite")
        pdata_panel = layout.box()
        pdata_panel.label(text="Prefab's Default Instancing Data")
        pdata_panel.prop(bpy.context.collection.muramasa_prefab.composite_data, "copy_mode")
        pdata_panel.prop(bpy.context.collection.muramasa_prefab.composite_data, "stream_mode")
        pdata_panel.prop(bpy.context.collection.muramasa_prefab.composite_data, "bound_mul")
        cmp_panel = layout.box()
        cmp_panel.label(text="Prefab Tiers")
        cmp_panel.operator("muramasa.edit_op_addprefabstreamtier")
        for ob_var in bpy.context.collection.keys():
            if("MURAMASA_PREFABTIER" in ob_var):
                ob_var_edit = "[\""+ob_var+"\"]"
                
                vstr = ""
                ob_var_split = ob_var.split('_')
                for i in range(len(ob_var_split)):
                    if (i < 2):
                        continue
                    vstr = vstr+ob_var_split[i]+" "
                
                cmp_panel.prop(bpy.context.collection,ob_var_edit,text=vstr)
                ''
            ''
        ''
            

class MURAMASA_INTERLINK_PT_properties_object_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_label = "Muramasa Object Data"
    bl_category = "Muramasa Devtool"

    # @classmethod
    # def poll(cls, context):
    #     # Get script properties from file
    #     bpy.ops.muramasa.edit_op_updateobjectvars('EXEC_DEFAULT')
    #     return True

    def draw(self, context):
        layout = self.layout
        if bpy.context.object.instance_collection is not None:
            layout.prop(bpy.context.object.muramasa_prefab_instance, "override")
            if bpy.context.object.muramasa_prefab_instance.override is True:
                layout.prop(bpy.context.object.muramasa_prefab_instance, "copy_mode")
                layout.prop(bpy.context.object.muramasa_prefab_instance, "stream_mode")
                layout.prop(bpy.context.object.muramasa_prefab_instance, "bound_mul")
            else:
                layout.prop(bpy.context.object.instance_collection.muramasa_prefab.composite_data, "copy_mode")
                layout.prop(bpy.context.object.instance_collection.muramasa_prefab.composite_data, "stream_mode")
                layout.prop(bpy.context.object.instance_collection.muramasa_prefab.composite_data, "bound_mul")
        else:
            object_panel = layout.box()
            object_panel.label(text="Object")
            object_panel.prop(bpy.context.object.muramasa_object, "renderable")
            object_panel.prop(bpy.context.object.muramasa_object, "cast_shadow")
            object_panel.prop(bpy.context.object.muramasa_object, "dynamic")
            object_panel.prop(bpy.context.object.muramasa_object, "request_planar_reflection")
            object_panel.prop(bpy.context.object.muramasa_object, "emissive_color")
            object_panel.prop(bpy.context.object.muramasa_object, "shadow_cascade_mask")

            filter_panel = layout.box()
            filter_panel.label(text="Filters")
            filter_panel.prop(bpy.context.object.muramasa_object,"filter_opaque")
            filter_panel.prop(bpy.context.object.muramasa_object,"filter_transparent")
            filter_panel.prop(bpy.context.object.muramasa_object,"filter_water")
            filter_panel.prop(bpy.context.object.muramasa_object,"filter_navigation_mesh")

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
                decal_panel.prop(bpy.context.object.muramasa_decal,"base_color_only_alpha")

            layout.prop(bpy.context.object.muramasa_emitter, "is_set", text="Is Emitter")
            if bpy.context.object.muramasa_emitter.is_set is True:
                emitter_panel = layout.box()
                emitter_panel.label(text="Emitter")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"material")
                emitter_panel.prop(bpy.context.object.muramasa_emitter,"mesh")
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

            var_panel = layout.box()
            var_panel.label(text="Object Variables")
            var_panel.operator("muramasa.edit_op_updateobjectvars")
            for ob_var in bpy.context.object.keys():
                if("MURAMASA_LUAPARAMETER" in ob_var):
                    ob_var_edit = "[\""+ob_var+"\"]"
                    
                    vstr = ""
                    ob_var_split = ob_var.split('_')
                    for i in range(len(ob_var_split)):
                        if (i < 2):
                            continue
                        vstr = vstr+ob_var_split[i]+" "
                    
                    var_panel.prop(bpy.context.object,ob_var_edit,text=vstr)

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

        layout.prop(bpy.context.material.muramasa_material, "use_user_blend_mode")
        if(bpy.context.material.muramasa_material.use_user_blend_mode is True):
            layout.prop(bpy.context.material.muramasa_material, "user_blend_mode")
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
        # layout.prop(bpy.context.light.muramasa_light, "cascade_distances")
        # if 'muramasa_mesh' in bpy.context.object.data is not None:
        if type(bpy.context.object.data) is bpy.types.Mesh:
            layout.label(text="Mesh Data")
            layout.prop(bpy.context.object.data.muramasa_mesh, "renderable")
            layout.prop(bpy.context.object.data.muramasa_mesh, "double_sided")
            layout.prop(bpy.context.object.data.muramasa_mesh, "dynamic")
            layout.prop(bpy.context.object.data.muramasa_mesh, "tlas_force_double_sided")
            layout.prop(bpy.context.object.data.muramasa_mesh, "double_sided_shadow")
            layout.prop(bpy.context.object.data.muramasa_mesh, "bvh_enabled")

            layout.prop(bpy.context.object.data.muramasa_mesh, "lod_mode")
        if 'muramasa_light' in bpy.context.object.data is not None:
            layout.label(text="Light Data")
            layout.prop(bpy.context.light.muramasa_light, "is_volumetric")
            layout.prop(bpy.context.light.muramasa_light, "cast_volume_cloud")
            layout.prop(bpy.context.light.muramasa_light, "cascade_distances")
        

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

class MURAMASA_INTERLINK_PT_properties_bone_panel(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "bone"
    bl_label = "Muramasa Bone Data"
    bl_category = "Muramasa Devtool"

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.bone.muramasa_spring, "is_set")
        spring_panel = layout.box()
        spring_panel.label(text="Spring Data")
        if bpy.context.bone.muramasa_spring.is_set is True:
            spring_panel.prop(bpy.context.bone.muramasa_spring, "reset")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "disabled")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "enable_stretch")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "enable_gravity")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "stiffness_force")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "drag_force")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "wind_force")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "hit_radius")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "gravity_power")
            spring_panel.prop(bpy.context.bone.muramasa_spring, "gravity_dir")
        else:
            spring_panel.label(text="Spring is not enabled")
        spring_panel.operator("muramasa.edit_op_setspringdatachildren")
        spring_panel.operator("muramasa.edit_op_setspringdataselected")

class MURAMASA_INTERLINK_PT_properties_anim_panel(Panel):
    bl_space_type = "DOPESHEET_EDITOR"
    bl_region_type = "UI"
    bl_label = "Muramasa Action Data"
    bl_category = "Muramasa Devtool"

    def draw(self, context):
        if bpy.context.active_action is not None:
            layout = self.layout
            action_panel = layout.box()
            action_panel.label(text="Action Data")
            action_panel.prop(bpy.context.active_action.muramasa_action, "do_export")
            action_panel.prop(bpy.context.active_action.muramasa_action, "autoplay")

classes = (
    MURAMASA_INTERLINK_PT_panel,
    MURAMASA_INTERLINK_PT_properties_collection_panel,
    MURAMASA_INTERLINK_PT_properties_object_panel,
    MURAMASA_INTERLINK_PT_properties_material_panel,
    MURAMASA_INTERLINK_PT_properties_obdata_panel,
    MURAMASA_INTERLINK_PT_properties_physics_panel,
    MURAMASA_INTERLINK_PT_properties_particle_panel,
    MURAMASA_INTERLINK_PT_properties_bone_panel,
    MURAMASA_INTERLINK_PT_properties_anim_panel
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)