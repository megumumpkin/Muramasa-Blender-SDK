# Redline interlink, a plugin to initiate asset workflow for redline framework

import bpy

bl_info = {
    "name" : "Redline Studio",
    "author" : "megumumpkin",
    "blender" : (3,3,0),
    "version" : (0,0,1),
    "location" : "View3D",
    "warning" : "Plugin is still in development",
    "category" : "Redline"
}

register, unregister = bpy.utils.register_submodule_factory(__package__, (
    'gltf_ext_assetsmith',
    'scenedata',
    'operator',
    'ui'
))

if __name__ == '__main__':
    register()

def register_panel():
    # Register the panel on demand, we need to be sure to only register it once
    # This is necessary because the panel is a child of the extensions panel,
    # which may not be registered when we try to register this extension
    try:
        bpy.utils.register_class(GLTF_PT_REDLINEExtensionPanel)
    except Exception:
        pass

    # If the glTF exporter is disabled, we need to unregister the extension panel
    # Just return a function to the exporter so it can unregister the panel
    return unregister_panel


def unregister_panel():
    # Since panel is registered on demand, it is possible it is not registered
    try:
        bpy.utils.unregister_class(GLTF_PT_REDLINEExtensionPanel)
    except Exception:
        pass

class glTF2ExportUserExtension:

    def __init__(self):
        # We need to wait until we create the gltf2UserExtension to import the gltf2 modules
        # Otherwise, it may fail because the gltf2 may not be loaded yet
        from io_scene_gltf2.io.com.gltf2_io_extensions import Extension
        self.Extension = Extension
        self.properties = bpy.context.scene.RedlineInterlinkExtensionProperties

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