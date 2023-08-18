# Muramasa interlink, a plugin to initiate asset workflow for muramasa development kit

import bpy
from . import gltf_ext_assetsmith
from . import scenedata
from . import operator
from . import ui

bl_info = {
    "name" : "Muramasa Development Kit",
    "author" : "megumumpkin",
    "blender" : (3,6,1),
    "version" : (2023,0,"alpha"),
    "location" : "View3D",
    "warning" : "Plugin is still in development",
    "category" : "Game Development"
}

# def register():
#     scenedata.register()
#     operator.register()
#     ui.register()
#     gltf_ext_assetsmith.register()

# def unregister():
#     gltf_ext_assetsmith.register()
#     ui.register()
#     operator.register()
#     scenedata.register()

register, unregister = bpy.utils.register_submodule_factory(__package__, [
    'gltf_ext_assetsmith',
    'scenedata',
    'operator',
    'ui'
])

if __name__ == '__main__':
    register()

def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(GLTF_PT_MURAMASAExtensionPanel)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    # Since panel is registered on demand, it is possible it is not registered
    try:
        bpy.utils.unregister_class(GLTF_PT_MURAMASAExtensionPanel)
    except Exception:
        pass

class glTF2ExportUserExtension:

    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        self.properties = bpy.context.scene.MuramasaInterlinkExtensionProperties

    def gather_node_hook(self, gltf2_object, blender_object, export_settings):
        if self.properties.enabled:
            gltf_ext_assetsmith.gather_node_hook(self, gltf2_object, blender_object, export_settings)
            
    def gather_joint_hook(self, gltf2_node, blender_bone, export_settings):
        if self.properties.enabled:
            gltf_ext_assetsmith.gather_joint_hook(self, gltf2_node, blender_bone, export_settings)

    def gather_material_hook(self, gltf2_material, blender_material, export_settings):
        if self.properties.enabled:
            gltf_ext_assetsmith.gather_material_hook(self, gltf2_material, blender_material, export_settings)

    def gather_texture_hook(self, gltf2_texture, blender_shader_sockets, export_settings):
        if self.properties.enabled:
            gltf_ext_assetsmith.gather_texture_hook(self, gltf2_texture, blender_shader_sockets, export_settings)

    def gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, materials, export_settings):
        if self.properties.enabled:
            gltf_ext_assetsmith.gather_mesh_hook(self, gltf2_mesh, blender_mesh, blender_object, vertex_groups, modifiers, materials, export_settings)

    def gather_actions_hook(self, blender_object, params, export_settings):
        if self.properties.enabled:
            gltf_ext_assetsmith.gather_actions_hook(self, blender_object, params, export_settings)

    def gather_gltf_extensions_hook(self, gltf2_plan, export_settings):
        if self.properties.enabled:
            gltf_ext_assetsmith.gather_gltf_extensions_hook(self, gltf2_plan, export_settings)