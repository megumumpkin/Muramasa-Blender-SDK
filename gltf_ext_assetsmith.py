import bpy
import os
from enum import Flag, auto

# glTF extensions are named following a convention with known prefixes.
# See: https://github.com/KhronosGroup/glTF/tree/master/extensions#about-gltf-extensions
# also: https://github.com/KhronosGroup/glTF/blob/master/extensions/Prefixes.md
glTF_extension_name = "REDLINE_assetsmith"

# Support for an extension is "required" if a typical glTF viewer cannot be expected
# to load a given model without understanding the contents of the extension.
# For RedlineInterlink, a compression scheme or new image format (with no fallback included)
# would be "required", but physics metadata or app-specific settings could be optional.
extension_is_required = False


class RedlineInterlinkExtensionProperties(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="Redline Interlink",
        description='Include this extension in the exported glTF file.',
        default=True
        )

def register():
    bpy.utils.register_class(RedlineInterlinkExtensionProperties)
    bpy.types.Scene.RedlineInterlinkExtensionProperties = bpy.props.PointerProperty(type=RedlineInterlinkExtensionProperties)
    bpy.utils.register_class(GLTF_PT_REDLINEExtensionPanel)

def unregister():
    # unregister_panel()
    bpy.utils.unregister_class(GLTF_PT_REDLINEExtensionPanel)
    bpy.utils.unregister_class(RedlineInterlinkExtensionProperties)
    del bpy.types.Scene.RedlineInterlinkExtensionProperties

class GLTF_PT_REDLINEExtensionPanel(bpy.types.Panel):

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
        props = bpy.context.scene.RedlineInterlinkExtensionProperties
        self.layout.prop(props, 'enabled')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        props = bpy.context.scene.RedlineInterlinkExtensionProperties
        layout.active = props.enabled

        box = layout.box()
        box.label(text=glTF_extension_name)

        props = bpy.context.scene.RedlineInterlinkExtensionProperties
        layout.prop(props, 'float_property', text="Some float value")

def gather_node_hook(self, gltf2_object, blender_object, export_settings):
    if gltf2_object.extensions is None:
        gltf2_object.extensions = {}
    extdata_build = {}

    if blender_object.instance_collection is not None:
        file_base = bpy.context.blend_data.filepath
        if blender_object.instance_collection.library is not None:
            file_base = bpy.path.abspath("//") + blender_object.instance_collection.library.filepath

        project_root = os.path.realpath(os.path.join(os.path.dirname(file_base), bpy.context.scene.redline_project_root[2:]))
        content_root = project_root+"/Data/Content"
        file_base = file_base[:len(file_base)-6]
        file_base = os.path.relpath(file_base, content_root)

        file_prefab = file_base
        if blender_object.instance_collection.name != "MAIN":
            file_prefab += "_"+blender_object.instance_collection.name
        file_prefab = file_prefab+".wiscene"
        
        extdata_build["prefab"]={
            "file": file_prefab,
            "copy_mode": blender_object.redline_prefab_instance.copy_mode,
            "stream_mode": blender_object.redline_prefab_instance.stream_mode
        }

    if blender_object.data is not None:
        if 'redline_mesh' in blender_object.data:
            flag_build = 0
            if bpy.context.object.redline_object.renderable:
                flag_build = flag_build | (1 << 0)
            if bpy.context.object.redline_object.cast_shadow:
                flag_build = flag_build | (1 << 1)
            if bpy.context.object.redline_object.dynamic:
                flag_build = flag_build | (1 << 2)
            if bpy.context.object.redline_object.request_planar_reflection:
                flag_build = flag_build | (1 << 4)
            extdata_build["object"]={
                "flags": flag_build,
                "emissivecolor": [
                    blender_object.redline_object.emissive_color[0],
                    blender_object.redline_object.emissive_color[1],
                    blender_object.redline_object.emissive_color[2],
                    blender_object.redline_object.emissive_color[3],
                ],
                "shadow_cascade_mask": 0, # TODO
            }

    if blender_object.redline_collider is not None:
        if blender_object.redline_collider.is_set is True:
            flag_build = 0
            if blender_object.redline_collider.set_CPU_enabled:
                flag_build = flag_build | (1 << 0)
            if blender_object.redline_collider.set_GPU_enabled:
                flag_build = flag_build | (1 << 1)
            extdata_build["collider"]={
                "flags": flag_build,
                "shape": blender_object.redline_collider.shape,
                "radius": blender_object.redline_collider.radius,
                "offset":[
                    blender_object.redline_collider.offset[0],
                    blender_object.redline_collider.offset[1],
                    blender_object.redline_collider.offset[2]
                ],
                "tail": [
                    blender_object.redline_collider.tail[0],
                    blender_object.redline_collider.tail[1],
                    blender_object.redline_collider.tail[2]
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
                blender_object.redline_rb_extents[0],
                blender_object.redline_rb_extents[1],
                blender_object.redline_rb_extents[2]
            ]
        }

    if blender_object.soft_body is not None:
        # NUMPY PROCESS WEIGHTS
        # 1 INVERT
        # 2 SERIALIZE uint8_t
        # 3 SERIALIZE base64

        extdata_build["softbody"]={
            "flags": 0,
            "mass": blender_object.soft_body.mass,
            "friction": blender_object.soft_body.friction,
            "restitution": 0, # TODO
            # "physicsgpumapping":0, #accessor index, unused, optional
            # "gpuphysicsmapping":0, #accessor index, unused, optional
            "weights": "-" #Base64 Float32 buffer, 0 is pinned, 1 is unpinned, need to invert the values from blender to wicked
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

    if blender_object.redline_decal is not None:
        if blender_object.redline_decal.is_set is True:
            extdata_build["decal"]=blender_object.redline_decal.material.name # material id in string

    if blender_object.redline_script is not None:
        if blender_object.redline_script:
            extdata_build["script"]=blender_object.redline_script

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