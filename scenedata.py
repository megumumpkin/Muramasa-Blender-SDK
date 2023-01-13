import bpy
from bpy.app.handlers import persistent

class RedlinePrefab(bpy.types.PropertyGroup):
    include : bpy.props.BoolProperty(name="Include in Export", default=False)
    composite : bpy.props.BoolProperty(name="Composite to Main Scene", default=False)

class RedlinePrefabInstance(bpy.types.PropertyGroup):
    copy_mode : bpy.props.EnumProperty(
        name="Copy Mode",
        description = "How will the prefab be loaded",
        items=[
            ("SHALLOW_COPY","Shallow Copy",""),
            ("DEEP_COPY","Deep Copy",""),
        ]
    )
    stream_mode : bpy.props.EnumProperty(
        name="Stream Mode",
        description = "How will the prefab be loaded",
        items=[
            ("DIRECT","Direct",""),
            ("DISTANCE","Distance",""),
            ("SCREEN_ESTATE","Screen Estate",""),
            ("MANUAL","Manual","")
        ]
    )
    composite : bpy.props.BoolProperty(name="Composite To This Prefab", default=False)

class RedlineObject(bpy.types.PropertyGroup):
    renderable : bpy.props.BoolProperty(name="Renderable", default=True)
    cast_shadow : bpy.props.BoolProperty(name="Cast Shadow", default=True)
    dynamic : bpy.props.BoolProperty(name="Dynamic", default=True)
    request_planar_reflection : bpy.props.BoolProperty(name="Request Planar Reflection", default=False)
    emissive_color : bpy.props.FloatVectorProperty(name="Emissive Color", subtype='COLOR', size=4)
    shadow_cascade_mask : bpy.props.BoolVectorProperty(name="Shadow Cascade Mask", subtype='LAYER', size=16)

class RedlineMesh(bpy.types.PropertyGroup):
    lod_mode : bpy.props.EnumProperty(
        name="LOD Mode",
        description = "How will the prefab be loaded",
        items=[
            ("NONE","None",""),
            ("STANDARD","Standard",""),
            ("HDM","HDM","")
        ]
    )

class RedlineCollider(bpy.types.PropertyGroup):
    is_set : bpy.props.BoolProperty(name="Use Collider", default=False)
    shape : bpy.props.EnumProperty(
        name="Collider shape",
        description = "Which type of collider to be used in runtime",
        items=[
            ("SPHERE","Sphere",""),
            ("CAPSULE","Capsule",""),
            ("PLANE","Plane","")
        ]
    )
    radius : bpy.props.FloatProperty(name="Collider Radius")
    offset : bpy.props.FloatVectorProperty(name="Collider Position Offset")
    tail : bpy.props.FloatVectorProperty(name="Collider Tail Position (for Capsule)")
    set_CPU_enabled : bpy.props.BoolProperty(name="Enable CPU Collision")
    set_GPU_enabled : bpy.props.BoolProperty(name="Enable GPU Collision")

class RedlineDecal(bpy.types.PropertyGroup):
    is_set : bpy.props.BoolProperty(name="Use Decal", default=False)
    material : bpy.props.PointerProperty(name="Material", type=bpy.types.Material)


classes = (
    RedlinePrefab,
    RedlinePrefabInstance,
    RedlineObject,
    RedlineMesh,
    RedlineCollider,
    RedlineDecal
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.types.Scene.redline_project_root = bpy.props.StringProperty(name="Project Root",default="",subtype="FILE_PATH")
    
    bpy.types.Mesh.redline_mesh = bpy.props.PointerProperty(type=RedlineMesh)
    bpy.types.Object.redline_object = bpy.props.PointerProperty(type=RedlineObject)
    bpy.types.Object.redline_script = bpy.props.StringProperty(name="Script File", subtype="FILE_PATH")
    bpy.types.Object.redline_collider = bpy.props.PointerProperty(type=RedlineCollider)
    bpy.types.Object.redline_decal = bpy.props.PointerProperty(type=RedlineDecal)
    bpy.types.Object.redline_rb_extents = bpy.props.FloatVectorProperty(name="Collider Extents", default=(1.0, 1.0, 1.0))
    
    bpy.types.Collection.redline_prefab = bpy.props.PointerProperty(type=RedlinePrefab)
    bpy.types.Object.redline_prefab_instance = bpy.props.PointerProperty(type=RedlinePrefabInstance)


def unregister():
    del bpy.types.Scene.redline_project_root

    del bpy.types.Mesh.redline_mesh
    del bpy.types.Object.redline_object
    del bpy.types.Object.redline_decal
    del bpy.types.Object.redline_script
    del bpy.types.Object.redline_collider
    del bpy.types.Object.redline_rb_extents

    del bpy.types.Collection.redline_prefab
    del bpy.types.Object.redline_prefab_instance

    for c in classes:
        bpy.utils.unregister_class(c)