import bpy
import os
import sys
import subprocess
import numpy
from bpy.types import Operator

class MURAMASA_INTERLINK_OT_updateasset(Operator):
    bl_idname = "muramasa.interlink_op_updateasset"
    bl_label = "Update Asset"
    bl_description = "Update asset to engine"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print("MURAMASA ASSET EXPORT START")
        
        file_base = bpy.context.blend_data.filepath
        project_root = os.path.abspath(os.path.join(os.path.dirname(file_base), bpy.context.scene.muramasa_project_root[2:]))
        content_root = project_root+"/Data/Content"
        binary_root = project_root
        file_base = file_base[:len(file_base)-6]

        import_main = False

        exe_name = "./Dev"
        if(sys.platform == 'win32'):
            exe_name = "Dev.exe"

        for i_collection in bpy.context.scene.collection.children:
            if i_collection.muramasa_prefab.include is True:
                # Prep up
                defer_import = False
                context_restore = bpy.context.copy()
                temp_compose_collection = []

                # Set active context
                original_active_collection = bpy.context.view_layer.active_layer_collection
                bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[i_collection.name]

                # 1. Set the file name
                file_collection = file_base
                if i_collection.muramasa_prefab.is_main is False:
                    file_collection += "_"+i_collection.name
                else:
                    import_main = True
                    defer_import = True
                    # Compose other collection to this scene if it has Composite checked as it's node
                    for checkcomp_collection in bpy.context.scene.collection.children:
                        if checkcomp_collection.muramasa_prefab.is_main is False:
                            if checkcomp_collection.muramasa_prefab.include is True:
                                if checkcomp_collection.muramasa_prefab.composite is True:
                                    print("COMPOSITE>"+checkcomp_collection.name)

                                    comp_object = bpy.data.objects.new(name="RLCOMPOSITE_"+checkcomp_collection.name, object_data=None)
                                    comp_object["muramasa_temp_instance_collection"] = checkcomp_collection
                                    comp_object.muramasa_prefab_instance.override = checkcomp_collection.muramasa_prefab.composite_data.override
                                    comp_object.muramasa_prefab_instance.copy_mode = checkcomp_collection.muramasa_prefab.composite_data.copy_mode
                                    comp_object.muramasa_prefab_instance.stream_mode = checkcomp_collection.muramasa_prefab.composite_data.stream_mode
                                    comp_object.muramasa_prefab_instance.bound_mul = checkcomp_collection.muramasa_prefab.composite_data.bound_mul

                                    bpy.context.view_layer.active_layer_collection.collection.objects.link(comp_object)
                                    temp_compose_collection.append(comp_object)
                file_collection = file_collection+".assetsmith"
                if not os.path.exists(file_collection):
                    os.mkdir(file_collection)
                
                # 2. Select which object to be exported (on the main context), cannot use context override, because the GLTF addon does not support that
                print("Exporting> "+file_collection)
                # Fix visibility
                visibility_restore_list = []
                for sub_collection in i_collection.children_recursive:
                    if sub_collection.hide_viewport is True:
                        visibility_restore_list.append(sub_collection)
                        sub_collection.hide_viewport = False
                # Select object and setup prefab instance
                for i_object in bpy.data.objects:
                    i_object.select_set(False)
                prefab_instance_restore_list = []
                for i_object in i_collection.all_objects:
                    # 2b. If object is a collection instance, do swap the instance type to none from collection!
                    if i_object.instance_collection is not None:
                        prefab_instance_restore_list.append({"object" : i_object, "instance_collection" : i_object.instance_collection})
                        i_object.instance_type = 'NONE'
                        i_object["muramasa_temp_instance_collection"] = i_object.instance_collection
                        i_object.instance_collection = None

                    # 2c. Check if object is a mesh and then check if it has specific vertex groups
                    if i_object.data is not None:
                        if isinstance(i_object.data, bpy.types.Mesh):
                            for vg in i_object.vertex_groups:
                                # print(weights)
                                # Pass vertex group VG_SOFTBODY to attribute SOFTBODY
                                if vg.name == "VG_SOFTBODY":
                                    if 'SOFTBODY' in i_object.data.attributes:
                                        i_object.data.attributes.remove(i_object.data.attributes['SOFTBODY'])
                                    i_object.data.attributes.new(name='SOFTBODY', type='FLOAT', domain='POINT')
                                    data_work = numpy.array(numpy.zeros(len(i_object.data.vertices), dtype=numpy.float32))
                                    for vtp_i in range(len(i_object.data.vertices)):
                                        data_work[vtp_i] = 1.0+(vg.weight(vtp_i)*-1.0)
                                    i_object.data.attributes['SOFTBODY'].data.foreach_set('value',data_work)

                                # Pass vertex group VG_WIND to attribute WIND
                                if vg.name == "VG_WIND":
                                    if 'WIND' in i_object.data.attributes:
                                        i_object.data.attributes.remove(i_object.data.attributes['WIND'])
                                    i_object.data.attributes.new(name='WIND', type='FLOAT', domain='POINT')
                                    data_work = numpy.array(numpy.zeros(len(i_object.data.vertices), dtype=numpy.float32))
                                    for vtp_i in range(len(i_object.data.vertices)):
                                        data_work[vtp_i] = vg.weight(vtp_i)
                                    i_object.data.attributes['WIND'].data.foreach_set('value',data_work)

                            # Pass vertex group for hairparticles to attribute HAIRPARTICLE_entityname
                            for pfx in i_object.particle_systems:
                                if pfx.settings.type == 'HAIR':
                                    if pfx.vertex_group_length != "":
                                        vg = i_object.vertex_groups[pfx.vertex_group_length]
                                        attrname = 'HAIRVGL_'+i_object.name+"_"+pfx.name
                                        if attrname in i_object.data.attributes:
                                            i_object.data.attributes.remove(i_object.data.attributes[attrname])
                                        i_object.data.attributes.new(name=attrname, type='FLOAT', domain='POINT')
                                        data_work = numpy.array(numpy.zeros(len(i_object.data.vertices), dtype=numpy.float32))
                                        for vtp_i in range(len(i_object.data.vertices)):
                                            data_work[vtp_i] = 1.0+(vg.weight(vtp_i)*-1.0)
                                        i_object.data.attributes[attrname].data.foreach_set('value',data_work)
                    
                    i_object.select_set(True)
                    print(i_object.name)
                    
                # 3. Export GLTF
                # Use the one that keeps textures in place, which will export binary separately too, sadly
                # You don't need to worry, I have tested this and it works, the only thing you need is to just believe me :3
                bpy.ops.export_scene.gltf(
                    filepath=file_collection+"/model.gltf",
                    export_format='GLTF_SEPARATE',
                    export_keep_originals=True,
                    use_selection=True,

                    # Export animation options for this 
                    export_animations=True,
                    export_animation_mode='ACTIONS',
                    export_optimize_animation_size=True,
                    export_optimize_animation_keep_anim_armature=False,
                    export_optimize_animation_keep_anim_object=False,

                    export_skins=True,
                    export_morph=True,
                    export_lights=True,
                    export_attributes=True,
                    export_cameras=True,
                    export_apply=True
                )

                # 4. Restore scene data
                for i_object in bpy.data.objects:
                    i_object.select_set(False)
                for i_object in context_restore['selected_objects']:
                    i_object.select_set(True)
                for i_list in prefab_instance_restore_list:
                    i_list["object"].instance_type = 'COLLECTION'
                    i_list["object"].instance_collection = i_list["instance_collection"]
                    del i_list["object"]["muramasa_temp_instance_collection"]
                for sub_collection in visibility_restore_list:
                    sub_collection.hide_viewport = True
                for comp_object in temp_compose_collection:
                    bpy.data.objects.remove(comp_object, do_unlink=True, do_id_user=True, do_ui_user=True)
                bpy.context.view_layer.active_layer_collection = original_active_collection
                

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
                
        print("MURAMASA ASSET EXPORT END")
        print("")
        return {'FINISHED'}

class MURAMASA_INTERLINK_OT_previewasset(Operator):
    bl_idname = "muramasa.interlink_op_previewasset"
    bl_label = "Preview Asset"
    bl_description = "Preview asset by running the engine"

    @classmethod
    def poll(cls, context):
        if context.collection is not None:
            if context.collection.muramasa_prefab is not None:
                if context.collection.muramasa_prefab.include is True:
                    return True

    def execute(self, context):
        file_base = bpy.context.blend_data.filepath
        project_root = os.path.abspath(os.path.join(os.path.dirname(file_base), bpy.context.scene.muramasa_project_root[2:]))
        content_root = project_root+"/Data/Content"
        binary_root = project_root
        file_base = file_base[:len(file_base)-6]

        exe_name = "./Dev"
        if(sys.platform == 'win32'):
            exe_name = "Dev.exe"

        file_collection = file_base
        if context.collection.muramasa_prefab.is_main is False:
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

def _internal_setspringdatarecursive(bone):
    for child in bone.children.values():
        # print(bone.muramasa_spring.items())
        child.muramasa_spring.is_set = bone.muramasa_spring.is_set
        child.muramasa_spring.enable_stretch = bone.muramasa_spring.enable_stretch
        child.muramasa_spring.enable_gravity = bone.muramasa_spring.enable_gravity
        child.muramasa_spring.stiffness_force = bone.muramasa_spring.stiffness_force
        child.muramasa_spring.drag_force = bone.muramasa_spring.drag_force
        child.muramasa_spring.wind_force = bone.muramasa_spring.wind_force
        child.muramasa_spring.hit_radius = bone.muramasa_spring.hit_radius
        child.muramasa_spring.gravity_power = bone.muramasa_spring.gravity_power
        child.muramasa_spring.gravity_dir = bone.muramasa_spring.gravity_dir
        _internal_setspringdatarecursive(child)

class MURAMASA_EDIT_OT_setspringdatachildren(Operator):
    bl_idname = "muramasa.edit_op_setspringdatachildren"
    bl_label = "Apply to All Children"
    bl_description = "Apply spring properties to all children of this bone"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bone = context.armature.bones.active
        _internal_setspringdatarecursive(bone)
        
        return {'FINISHED'}

class MURAMASA_EDIT_OT_setspringdataselected(Operator):
    bl_idname = "muramasa.edit_op_setspringdataselected"
    bl_label = "Apply to All Selected Bones"
    bl_description = "Apply spring properties to all selection of bones in this armature"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ref_bone = context.armature.bones.active
        for bone in context.armature.bones.values():
            if bone.select is True:
                bone.muramasa_spring.is_set = ref_bone.muramasa_spring.is_set
                bone.muramasa_spring.reset = ref_bone.muramasa_spring.reset
                bone.muramasa_spring.disabled = ref_bone.muramasa_spring.disabled
                bone.muramasa_spring.enable_stretch = ref_bone.muramasa_spring.enable_stretch
                bone.muramasa_spring.enable_gravity = ref_bone.muramasa_spring.enable_gravity
                bone.muramasa_spring.stiffness_force = ref_bone.muramasa_spring.stiffness_force
                bone.muramasa_spring.drag_force = ref_bone.muramasa_spring.drag_force
                bone.muramasa_spring.wind_force = ref_bone.muramasa_spring.wind_force
                bone.muramasa_spring.hit_radius = ref_bone.muramasa_spring.hit_radius
                bone.muramasa_spring.gravity_power = ref_bone.muramasa_spring.gravity_power
                bone.muramasa_spring.gravity_dir = ref_bone.muramasa_spring.gravity_dir
        return {'FINISHED'}

class MURAMASA_EDIT_OT_updateobjectvars(Operator):
    bl_idname = "muramasa.edit_op_updateobjectvars"
    bl_label = "Refresh Object Variables"
    bl_description = "Reload script linting"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if bpy.context.object.muramasa_script:
            print(os.path.abspath(bpy.path.abspath(bpy.context.object.muramasa_script)))
            with open(os.path.abspath(bpy.path.abspath(bpy.context.object.muramasa_script)), 'r') as file:
                data = file.read().split('\n')
                muramasa_part : bool = False
                for line in data:
                    part = line.split(' ')
                    print(part)
                    if (part[0] != "--"):
                        break

                    if ((not muramasa_part)):
                        if (part[1] == "MURAMASA_HINT"):
                            muramasa_part = True
                        else:
                            break

                    if(part[1] == "FLOAT"):
                        strname = "RLPARM_"+part[2]
                        if(strname not in bpy.context.object):
                            bpy.context.object[strname] = 0.0
                    if(part[1] == "STRING"):
                        strname = "RLPARM_"+part[2]
                        if(strname not in bpy.context.object):
                            bpy.context.object[strname] = ""
                    ''
            ''
        return {'FINISHED'}

classes = (
    MURAMASA_INTERLINK_OT_updateasset,
    MURAMASA_INTERLINK_OT_previewasset,
    MURAMASA_EDIT_OT_setspringdatachildren,
    MURAMASA_EDIT_OT_setspringdataselected,
    MURAMASA_EDIT_OT_updateobjectvars
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)