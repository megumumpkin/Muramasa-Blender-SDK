import bpy
import os
from enum import Flag, auto
import idprop
import json # For debugging

# glTF extensions are named following a convention with known prefixes.
# See: https://github.com/KhronosGroup/glTF/tree/master/extensions#about-gltf-extensions
# also: https://github.com/KhronosGroup/glTF/blob/master/extensions/Prefixes.md
glTF_extension_name = "MURAMASA_assetsmith"

# Support for an extension is "required" if a typical glTF viewer cannot be expected
# to load a given model without understanding the contents of the extension.
# For MuramasaInterlink, a compression scheme or new image format (with no fallback included)
# would be "required", but physics metadata or app-specific settings could be optional.
extension_is_required = False


class MuramasaInterlinkExtensionProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="Muramasa Interlink",
        description='Include this extension in the exported glTF file.',
        default=True
        )

def register():
    bpy.utils.register_class(MuramasaInterlinkExtensionProperties)
    bpy.types.Scene.MuramasaInterlinkExtensionProperties = bpy.props.PointerProperty(type=MuramasaInterlinkExtensionProperties)
    bpy.utils.register_class(GLTF_PT_MURAMASAExtensionPanel)

def unregister():
    # unregister_panel()
    bpy.utils.unregister_class(GLTF_PT_MURAMASAExtensionPanel)
    bpy.utils.unregister_class(MuramasaInterlinkExtensionProperties)
    del bpy.types.Scene.MuramasaInterlinkExtensionProperties

class GLTF_PT_MURAMASAExtensionPanel(bpy.types.Panel):

    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Enabled"
    bl_parent_id = "GLTF_PT_export_user_extensions"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORT_SCENE_OT_gltf"

    def draw_header(self, context):
        props = bpy.context.scene.MuramasaInterlinkExtensionProperties
        self.layout.prop(props, 'enabled')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        props = bpy.context.scene.MuramasaInterlinkExtensionProperties
        layout.active = props.enabled

        box = layout.box()
        box.label(text=glTF_extension_name)

        props = bpy.context.scene.MuramasaInterlinkExtensionProperties
        layout.prop(props, 'float_property', text="Some float value")

def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
    if gltf2_plan.extensions is None:
        gltf2_plan.extensions = {}
    extdata_build = {}

    extdata_build["exists"]={
        "does_exist": True,
    }

    gltf2_plan.extensions[glTF_extension_name] = self.Extension(
        name=glTF_extension_name,
        extension=extdata_build,
        required=extension_is_required
    )

def gather_node_hook(self, gltf2_object, blender_object, export_settings):
    if gltf2_object.extensions is None:
        gltf2_object.extensions = {}
    extdata_build = {}

    if 'muramasa_temp_instance_collection' in blender_object:
        # file_base = bpy.context.blend_data.filepath
        # if blender_object["muramasa_temp_instance_collection"].library is not None:
        #     file_base = bpy.path.abspath("//") + blender_object["muramasa_temp_instance_collection"].library.filepath

        # project_root = os.path.realpath(os.path.join(os.path.dirname(file_base), bpy.context.scene.muramasa_project_root[2:]))
        # content_root = project_root+"/Data/Content"
        # file_base = file_base[:len(file_base)-6]
        # file_base = os.path.relpath(file_base, content_root)

        file_base = bpy.path.abspath("//")
        project_root = os.path.abspath(os.path.join(os.path.dirname(file_base), bpy.context.scene.muramasa_project_root[2:]))
        content_root = project_root+"/Data/Content"
        binary_root = project_root
        if blender_object["muramasa_temp_instance_collection"].library is not None:
            file_base = bpy.path.abspath(blender_object["muramasa_temp_instance_collection"].library.filepath)
        else:
            file_base = bpy.context.blend_data.filepath
        file_base = os.path.relpath(file_base, content_root)
        file_base = file_base[:len(file_base)-6]

        file_prefab = file_base
        if blender_object["muramasa_temp_instance_collection"].muramasa_prefab.is_main is False:
            file_prefab += "_"+blender_object["muramasa_temp_instance_collection"].name
        file_prefab = file_prefab+".wiscene"

        if blender_object.muramasa_prefab_instance.override is True:
            extdata_build["prefab"]={
                "file": "content/" + file_prefab,
                "copy_mode": blender_object.muramasa_prefab_instance.copy_mode,
                "stream_mode": blender_object.muramasa_prefab_instance.stream_mode,
                "stream_distance_multiplier": blender_object.muramasa_prefab_instance.bound_mul
            }
        else:
            extdata_build["prefab"]={
                "file": "content/" + file_prefab,
                "copy_mode": blender_object["muramasa_temp_instance_collection"].muramasa_prefab.composite_data.copy_mode,
                "stream_mode": blender_object["muramasa_temp_instance_collection"].muramasa_prefab.composite_data.stream_mode,
                "stream_distance_multiplier": blender_object["muramasa_temp_instance_collection"].muramasa_prefab.composite_data.bound_mul
            }

    if blender_object.data is not None:
        if isinstance(blender_object.data, bpy.types.Mesh):
            flag_build = 0
            if blender_object.muramasa_object.renderable:
                flag_build = flag_build | (1 << 0)
            if blender_object.muramasa_object.cast_shadow:
                flag_build = flag_build | (1 << 1)
            if blender_object.muramasa_object.dynamic:
                flag_build = flag_build | (1 << 2)
            if blender_object.muramasa_object.request_planar_reflection:
                flag_build = flag_build | (1 << 4)
            shc_mask_build = 0
            for i in range(32):
                if blender_object.muramasa_object.shadow_cascade_mask[i] is True:
                    shc_mask_build = shc_mask_build | (1 << i)
            filter_mask_build = 0
            if blender_object.muramasa_object.filter_opaque:
                filter_mask_build = filter_mask_build | (1 << 0)
            if blender_object.muramasa_object.filter_transparent:
                filter_mask_build = filter_mask_build | (1 << 1)
            if blender_object.muramasa_object.filter_water:
                filter_mask_build = filter_mask_build | (1 << 2)
            if blender_object.muramasa_object.filter_navigation_mesh:
                filter_mask_build = filter_mask_build | (1 << 3)
            extdata_build["object"]={
                "flags": flag_build,
                "filtermask": filter_mask_build,
                "emissivecolor": [
                    blender_object.muramasa_object.emissive_color[0],
                    blender_object.muramasa_object.emissive_color[1],
                    blender_object.muramasa_object.emissive_color[2],
                    blender_object.muramasa_object.emissive_color[3],
                ],
                "shadow_cascade_mask": shc_mask_build,
            }
            
            # Hair particle systems
            hpfxlist = {}
            for pfx in blender_object.particle_systems:
                if pfx.settings.type == 'HAIR':
                    material_get = ""
                    if blender_object.material_slots[pfx.settings.material-1].material is not None:
                        material_get = blender_object.material_slots[pfx.settings.material-1].material.name
                    hpfxlist[blender_object.name+"_"+pfx.name] = {
                        "strand_count":pfx.settings.count,
                        "segment_count":pfx.settings.hair_step - 1,
                        "random_seed":pfx.seed,
                        "length":pfx.settings.hair_length,
                        "stiffness":pfx.settings.effect_hair,
                        "randomness":pfx.settings.grid_random,
                        "view_distance":pfx.settings.muramasa_hairparticle_distance,
                        "material":material_get
                    }
            extdata_build["hairsettings"]=hpfxlist
        if isinstance(blender_object.data, bpy.types.Light):
            flag_build = 0
            if blender_object.data.muramasa_light.is_volumetric is True:
                flag_build = flag_build | 1 << 1
            if blender_object.data.muramasa_light.cast_volume_cloud is True:
                flag_build = flag_build | 1 << 4
            if blender_object.data.use_shadow is True:
                flag_build = flag_build | 1 << 0
            extdata_build["light"]={
                "flags":flag_build,
                "cascade_distances":[
                    blender_object.data.muramasa_light.cascade_distances[0],
                    blender_object.data.muramasa_light.cascade_distances[1],
                    blender_object.data.muramasa_light.cascade_distances[2],
                    blender_object.data.muramasa_light.cascade_distances[3],
                    blender_object.data.muramasa_light.cascade_distances[4],
                    blender_object.data.muramasa_light.cascade_distances[5],
                ]
            }
            # Fix light level to match wicked
            # {'color': [1.0, 0.9893096089363098, 0.9576399922370911], 'intensity': 3415.0, 'spot': None, 'type': 'directional', 'range': None, 'name': 'Light', 'extensions': None, 'extras': None}
            light_data = gltf2_object.extensions["KHR_lights_punctual"].extension["light"].extension
            light_data["intensity"] = light_data["intensity"] / 683.0
            print(gltf2_object.extensions["KHR_lights_punctual"].extension["light"].extension["intensity"])

    if blender_object.muramasa_layer is not None:
        if blender_object.muramasa_layer.is_set is True:
            layer_build = 0
            for i in range(32):
                if blender_object.muramasa_layer.mask[i] is True:
                    layer_build = layer_build | (1 << i)
            extdata_build["layermask"]=layer_build

    if blender_object.muramasa_collider is not None:
        if blender_object.muramasa_collider.is_set is True:
            flag_build = 0
            if blender_object.muramasa_collider.set_CPU_enabled:
                flag_build = flag_build | (1 << 0)
            if blender_object.muramasa_collider.set_GPU_enabled:
                flag_build = flag_build | (1 << 1)
            extdata_build["collider"]={
                "flags": flag_build,
                "shape": blender_object.muramasa_collider.shape,
                "radius": blender_object.muramasa_collider.radius,
                "offset":[
                    blender_object.muramasa_collider.offset[0],
                    blender_object.muramasa_collider.offset[1],
                    blender_object.muramasa_collider.offset[2]
                ],
                "tail": [
                    blender_object.muramasa_collider.tail[0],
                    blender_object.muramasa_collider.tail[1],
                    blender_object.muramasa_collider.tail[2]
                ],
            }

    if blender_object.rigid_body is not None:
        extdata_build["rigidbody"]={
            "flags": 0,
            "shape": blender_object.rigid_body.collision_shape,
            "mass": blender_object.rigid_body.mass,
            "friction":blender_object.rigid_body.friction,
            "restitution": blender_object.rigid_body.restitution,
            "damping_linear": blender_object.rigid_body.linear_damping,
            "damping_angular": blender_object.rigid_body.angular_damping,
            "extents": [
                blender_object.muramasa_rb_extents[0],
                blender_object.muramasa_rb_extents[1],
                blender_object.muramasa_rb_extents[2]
            ]
        }

    if blender_object.soft_body is not None:
        extdata_build["softbody"]={
            "flags": 0,
            "mass": blender_object.soft_body.mass,
            "friction": blender_object.soft_body.friction,
            "restitution": 0, # TODO
            # Uses _SOFTBODY vertex attribute for weights, make sure the values are inverted
        }

    if blender_object.rigid_body_constraint is not None:
        if blender_object.rigid_body_constraint.type == 'GENERIC_SPRING': #ONLY ACCEPT GENERIC SPRING FOR EXPORT!
            extdata_build["spring"]={
                "flags": 9,
                "stiffnessForce": 0.5,
                "dragforce": 0.5,
                "windforce": 0.5,
                "hitradius": 0.0,
                "gravitypower": 0.5
            }

    if blender_object.field is not None:
        if blender_object.field.type == 'FORCE':
            extdata_build["force"]={
                "flags": 9,
                "gravity": 1.0+(blender_object.field.strength*(-1.0)),
                "range": blender_object.field.distance_max,
            }

    if blender_object.muramasa_decal is not None:
        if blender_object.muramasa_decal.is_set is True:
            if blender_object.muramasa_decal.material is not None:
                flag_build = 0
                if blender_object.muramasa_decal.base_color_only_alpha is True:
                    flag_build = flag_build | 1<<0
                extdata_build["decal"]={
                    "flags": flag_build,
                    "material": blender_object.muramasa_decal.material.name # material id in string
                } 

    if blender_object.muramasa_emitter is not None:
        if blender_object.muramasa_emitter.is_set is True:
            extdata_build["emitter"]={
                "shadertype": blender_object.muramasa_emitter.shadertype,
                "size": blender_object.muramasa_emitter.size,
                "random_factor": blender_object.muramasa_emitter.random_factor,
                "normal_factor": blender_object.muramasa_emitter.normal_factor,
                "count": blender_object.muramasa_emitter.count,
                "life": blender_object.muramasa_emitter.life,
                "random_life": blender_object.muramasa_emitter.random_life,
                "scale": [
                    blender_object.muramasa_emitter.scale[0],
                    blender_object.muramasa_emitter.scale[1],
                ],
                "rotation": blender_object.muramasa_emitter.rotation,
                "motion_blur_amount": blender_object.muramasa_emitter.motion_blur_amount,
                "mass": blender_object.muramasa_emitter.mass,
                "random_color": blender_object.muramasa_emitter.random_color,
                "velocity": [
                    blender_object.muramasa_emitter.velocity[0],
                    blender_object.muramasa_emitter.velocity[1],
                    blender_object.muramasa_emitter.velocity[2],
                ],
                "gravity": [
                    blender_object.muramasa_emitter.gravity[0],
                    blender_object.muramasa_emitter.gravity[1],
                    blender_object.muramasa_emitter.gravity[2],
                ],
                "drag": blender_object.muramasa_emitter.drag,
                "restitution": blender_object.muramasa_emitter.restitution,
                "sph_h": blender_object.muramasa_emitter.sph_h,
                "sph_K": blender_object.muramasa_emitter.sph_K,
                "sph_p0": blender_object.muramasa_emitter.sph_p0,
                "sph_e": blender_object.muramasa_emitter.sph_e,
                "sprite_frames": [
                    blender_object.muramasa_emitter.sprite_frames[0],
                    blender_object.muramasa_emitter.sprite_frames[1],
                ],
                "sprite_framecount": blender_object.muramasa_emitter.sprite_framecount,
                "sprite_framestart": blender_object.muramasa_emitter.sprite_framestart,
                "sprite_framerate": blender_object.muramasa_emitter.sprite_framerate,
            }
            if blender_object.muramasa_emitter.material is not None:
                extdata_build["emitter"]["material"] = blender_object.muramasa_emitter.material.name
            if blender_object.muramasa_emitter.mesh is not None:
                extdata_build["emitter"]["mesh"] = blender_object.muramasa_emitter.mesh.name
    
    if blender_object.muramasa_script is not None:
        if blender_object.muramasa_script:
            file_base = bpy.path.abspath("//")
            project_root = os.path.abspath(os.path.join(os.path.dirname(file_base), bpy.context.scene.muramasa_project_root[2:]))
            content_root = project_root+"/Data/Content"
            file_script = bpy.path.abspath(blender_object.muramasa_script)
            file_script = os.path.relpath(file_script, content_root)
            extdata_build["script"]="content/" + file_script

    params_build = ""
    for key, value in blender_object.items():
        if key[:7] == "MURAMASA_LUAPARAMETER_":
            mkey = key[7:]
            print(type(value))
            if isinstance(value, str):
                if (value == "true") or (value == "false"):
                    params_build = params_build + "D." + mkey + " = " + value + ";"
                else:
                    params_build = params_build + "D." + mkey + " = \"" + value + "\";"
            if isinstance(value, int) or isinstance(value, float):
                params_build = params_build + "D." + mkey + " = " + str(value) + ";"
            if isinstance(value, idprop.types.IDPropertyArray):
                if len(value) > 0:
                    if isinstance(value[0], float):
                        if len(value) == 2:
                            params_build = params_build + "D." + mkey + " = Vector(" + str(value[0]) + "," + str(value[1]) + ");"
                        if len(value) == 3:
                            params_build = params_build + "D." + mkey + " = Vector(" + str(value[0]) + "," + str(value[1]) + "," + str(value[2]) + ");"

    if len(params_build) > 0:
        extdata_build["params"]=params_build
            
    gltf2_object.extensions[glTF_extension_name] = self.Extension(
        name=glTF_extension_name,
        extension=extdata_build,
        required=extension_is_required
    )

# blender_bone is a posebone
def gather_joint_hook(self, gltf2_node, blender_bone, export_settings):
    if gltf2_node.extensions is None:
        gltf2_node.extensions = {}
    extdata_build = {}
    if blender_bone.bone.muramasa_spring is not None:
        if blender_bone.bone.muramasa_spring.is_set is True:
            flag_build = 0
            if blender_bone.bone.muramasa_spring.reset is True:
                flag_build = flag_build | 1 << 0
            if blender_bone.bone.muramasa_spring.disabled is True:
                flag_build = flag_build | 1 << 1
            if blender_bone.bone.muramasa_spring.enable_stretch is True:
                flag_build = flag_build | 1 << 2
            if blender_bone.bone.muramasa_spring.enable_gravity is True:
                flag_build = flag_build | 1 << 3
            extdata_build["spring"]={
                "flags":flag_build,
                "stiffness_force":blender_bone.bone.muramasa_spring.stiffness_force,
                "drag_force":blender_bone.bone.muramasa_spring.drag_force,
                "wind_force":blender_bone.bone.muramasa_spring.wind_force,
                "hit_radius":blender_bone.bone.muramasa_spring.hit_radius,
                "gravity_power":blender_bone.bone.muramasa_spring.gravity_power,
                "gravity_dir":[
                    blender_bone.bone.muramasa_spring.gravity_dir[0],
                    blender_bone.bone.muramasa_spring.gravity_dir[1],
                    blender_bone.bone.muramasa_spring.gravity_dir[2],
                ]
            }
    # Check bone constraints and see if it has ik
    # [c for c in bone.constraints if c.type=='COPY_LOCATION']
    for constraint in blender_bone.constraints:
        if constraint.type == 'IK':
            extdata_build["inversekinematics"]={
                "flags":0,
                "target":constraint.target.name, #node name 
                "chainlength":constraint.chain_count,
                "iterationcount":constraint.iterations
            }
    gltf2_node.extensions[glTF_extension_name] = self.Extension(
        name=glTF_extension_name,
        extension=extdata_build,
        required=extension_is_required
    )

def gather_material_hook(self, gltf2_material, blender_material, export_settings):
    if gltf2_material.extensions is None:
        gltf2_material.extensions = {}
    extdata_build = {}
    if blender_material.muramasa_material is not None:
        flag_build = (1 << 0)
        if blender_material.muramasa_material.shadow_cast:
            flag_build = flag_build | (1 << 1)
        if blender_material.muramasa_material.use_vertex_colors:
            flag_build = flag_build | (1 << 5)
        if blender_material.muramasa_material.workflow_specgloss:
            flag_build = flag_build | (1 << 6)
        if blender_material.muramasa_material.occlussion_primary:
            flag_build = flag_build | (1 << 7)
        if blender_material.muramasa_material.occlussion_secondary:
            flag_build = flag_build | (1 << 8)
        if blender_material.muramasa_material.use_wind:
            flag_build = flag_build | (1 << 9)
        if blender_material.muramasa_material.shadow_noreceive:
            flag_build = flag_build | (1 << 10)
        if blender_material.muramasa_material.outline:
            flag_build = flag_build | (1 << 12)
        extdata_build["material_extra"] = {
            "flags":flag_build,
            "use_user_blend_mode":blender_material.muramasa_material.use_user_blend_mode,
            "user_blend_mode":blender_material.muramasa_material.user_blend_mode,
            "shading_rate":blender_material.muramasa_material.shading_rate,
            "tex_anim_dir":[
                blender_material.muramasa_material.tex_anim_dir[0],
                blender_material.muramasa_material.tex_anim_dir[1]
            ],
            "tex_anim_framerate":blender_material.muramasa_material.tex_anim_framerate,
            "tex_anim_elapsedtime":blender_material.muramasa_material.tex_anim_elapsedtime,
        }
    gltf2_material.extensions[glTF_extension_name] = self.Extension(
        name=glTF_extension_name,
        extension=extdata_build,
        required=extension_is_required
    )

#Need to rename the texture name to texture path
def gather_texture_hook(self, gltf2_texture, blender_shader_sockets, export_settings):
    gltf2_texture.source.name = gltf2_texture.source.uri

def gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, materials, export_settings):
    if gltf2_mesh.extensions is None:
        gltf2_mesh.extensions = {}
    extdata_build = {}
    if blender_mesh.muramasa_mesh is not None:
        mesh_flag_build = 0
        if blender_mesh.muramasa_mesh.renderable is True:
            mesh_flag_build = mesh_flag_build | 1 << 0
        if blender_mesh.muramasa_mesh.double_sided is True:
            mesh_flag_build = mesh_flag_build | 1 << 1
        if blender_mesh.muramasa_mesh.dynamic is True:
            mesh_flag_build = mesh_flag_build | 1 << 2
        if blender_mesh.muramasa_mesh.tlas_force_double_sided is True:
            mesh_flag_build = mesh_flag_build | 1 << 6
        if blender_mesh.muramasa_mesh.double_sided_shadow is True:
            mesh_flag_build = mesh_flag_build | 1 << 7
        if blender_mesh.muramasa_mesh.bvh_enabled is True:
            mesh_flag_build = mesh_flag_build | 1 << 8
        extdata_build["mesh"] = {
            "flags":mesh_flag_build,
        }
    gltf2_mesh.extensions[glTF_extension_name] = self.Extension(
        name=glTF_extension_name,
        extension=extdata_build,
        required=extension_is_required
    )


GLTF_EXTENSION_DATA = {
    "animation_extra":{},
}

def gather_actions_hook(self, blender_object, params, export_settings):
    global GLTF_EXTENSION_DATA

    actions_refilter = []

    for blender_action in params.blender_actions:
        do_export : bool = (GLTF_EXTENSION_DATA["animation_extra"].get(blender_action.name) is None) and (blender_action.muramasa_action is not None)
        if do_export:
            do_export = blender_action.muramasa_action.do_export
        if do_export:
            animex_flag_build = 0
            if blender_action.muramasa_action.autoplay is True:
                animex_flag_build = animex_flag_build | 1 << 0
            GLTF_EXTENSION_DATA["animation_extra"][blender_action.name] = {
                "flags":animex_flag_build,
            }
            actions_refilter.append(blender_action)

    params.blender_actions = actions_refilter
    # print(actions_refilter)
    ''

# Combine all extradata
def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
    global GLTF_EXTENSION_DATA

    if gltf2_plan.extensions is None:
        gltf2_plan.extensions = {}
    extdata_build = {}

    # Scene prefab LOD tier data
    extdata_build["prefab_tiers"] = []
    prefab_tier_idx = 0
    for ob_var in bpy.context.scene.keys():
        if("MURAMASA_PREFABTIER" in ob_var):
            extdata_build["prefab_tiers"].append(bpy.context.scene[ob_var])
            del(bpy.context.scene[ob_var])
            prefab_tier_idx + 1
            ''
        ''
    ''

    # Finalizing all extension data to this compendium or sort
    for extension_name, extension_data in GLTF_EXTENSION_DATA.items():
        final_data_build = []
        for id_str, object_data in extension_data.items():
            object_data["name"] = id_str
            final_data_build.append(object_data)
        extdata_build[extension_name] = final_data_build
        GLTF_EXTENSION_DATA[extension_name] = {}
    
    gltf2_plan.extensions[glTF_extension_name] = self.Extension(
        name=glTF_extension_name,
        extension=extdata_build,
        required=extension_is_required
    )