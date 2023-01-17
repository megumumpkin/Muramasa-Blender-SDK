import bpy
import os
import sys
import subprocess
from bpy.types import Operator

class REDLINE_INTERLINK_OT_updateasset(Operator):
    bl_idname = "redline.interlink_op_updateasset"
    bl_label = "Update Asset"
    bl_description = "Update asset to engine"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print("REDLINE ASSET EXPORT START")
        
        file_base = bpy.context.blend_data.filepath
        project_root = os.path.realpath(os.path.join(os.path.dirname(file_base), bpy.context.scene.redline_project_root[2:]))
        content_root = project_root+"/Data/Content"
        binary_root = project_root+"/build"
        file_base = file_base[:len(file_base)-6]

        import_main = False

        exe_name = "./Dev"
        if(sys.platform == 'win32'):
            exe_name = "Dev.exe"

        for i_collection in bpy.context.scene.collection.children:
            if i_collection.redline_prefab.include is True:
                defer_import = False

                # 1. Set the file name
                file_collection = file_base
                if i_collection.name != "MAIN":
                    file_collection += "_"+i_collection.name
                else:
                    import_main = True
                    defer_import = True
                file_collection = file_collection+".assetsmith"
                if not os.path.exists(file_collection):
                    os.mkdir(file_collection)
                
                # 2. Select which object to be get selected, cannot use context override, because the GLTF addon does not support that
                print("Exporting> "+file_collection)
                context_restore = bpy.context.copy()
                bpy.ops.object.select_all(action='DESELECT')
                prefab_instance_restore_list = []
                for i_object in i_collection.all_objects:
                    # 2b. If object is a collection instance, do swap the instance type to none from collection!
                    if i_object.instance_collection is not None:
                        prefab_instance_restore_list.append({"object" : i_object, "instance_collection" : i_object.instance_collection})
                        i_object.instance_type = 'NONE'
                        i_object["redline_temp_instance_collection"] = i_object.instance_collection
                        i_object.instance_collection = None
                    i_object.select_set(True)
                    
                # 3. Export GLTF
                # Use the one that keeps textures in place, which will export binary separately too, sadly
                # You don't need to worry, I have tested this and it works, the only thing you need is to just believe me :3
                bpy.ops.export_scene.gltf(
                    filepath=file_collection+"/model.gltf",
                    export_format='GLTF_SEPARATE',
                    export_keep_originals=True,
                    use_selection=True,
                    export_animations=True,
                    export_skins=True,
                    export_morph=True,
                    export_lights=True
                )

                # 4. Restore scene data
                bpy.ops.object.select_all(action='DESELECT')
                for i_object in context_restore['selected_objects']:
                    i_object.select_set(True)
                for i_list in prefab_instance_restore_list:
                    i_list["object"].instance_type = 'COLLECTION'
                    i_list["object"].instance_collection = i_list["instance_collection"]
                    del i_list["object"]["redline_temp_instance_collection"]

                # 5. Execute import to engine, wait for completion
                if defer_import is not True:
                    subprocess.run(
                        [exe_name,"-t","SCENE_IMPORT","-i",os.path.relpath(file_collection, content_root)],
                        cwd=binary_root
                    )

        if import_main is True:
            subprocess.run(
                [exe_name,"-t","SCENE_IMPORT","-i",os.path.relpath(file_base+".assetsmith", content_root)],
                cwd=binary_root
            )
                
        print("REDLINE ASSET EXPORT END")
        print("")
        return {'FINISHED'}

class REDLINE_INTERLINK_OT_previewasset(Operator):
    bl_idname = "redline.interlink_op_previewasset"
    bl_label = "Preview Asset"
    bl_description = "Preview asset by running the engine"

    @classmethod
    def poll(cls, context):
        if context.collection is not None:
            if context.collection.redline_prefab is not None:
                if context.collection.redline_prefab.include is True:
                    return True

    def execute(self, context):
        file_base = bpy.context.blend_data.filepath
        project_root = os.path.realpath(os.path.join(os.path.dirname(file_base), bpy.context.scene.redline_project_root[2:]))
        content_root = project_root+"/Data/Content"
        binary_root = project_root+"/build"
        file_base = file_base[:len(file_base)-6]

        exe_name = "./Dev"
        if(sys.platform == 'win32'):
            exe_name = "Dev.exe"

        file_collection = file_base
        if context.collection.name != "MAIN":
            file_collection += "_"+context.collection.name
        else:
            import_main = True
            defer_import = True
        file_collection = file_collection+".wiscene"

        subprocess.Popen(
            [exe_name,"-t","SCENE_PREVIEW","-i",os.path.relpath(file_collection, content_root)],
            cwd=binary_root
        )
        
        return {'FINISHED'}

classes = (
    REDLINE_INTERLINK_OT_updateasset,
    REDLINE_INTERLINK_OT_previewasset
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)