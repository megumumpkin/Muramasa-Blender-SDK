import bpy
from bpy.app.handlers import persistent

class MuramasaPrefabInstance(bpy.types.PropertyGroup):
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
    bound_mul : bpy.props.FloatProperty(name="Streaming Boundary Multiplier", default=1.0)

class MuramasaPrefab(bpy.types.PropertyGroup):
    include : bpy.props.BoolProperty(name="Include in Export", default=False)
    composite : bpy.props.BoolProperty(name="Composite to Main Scene", default=False)
    composite_data : bpy.props.PointerProperty(type=MuramasaPrefabInstance)

class MuramasaObject(bpy.types.PropertyGroup):
    renderable : bpy.props.BoolProperty(name="Renderable", default=True)
    cast_shadow : bpy.props.BoolProperty(name="Cast Shadow", default=True)
    dynamic : bpy.props.BoolProperty(name="Dynamic", default=True)
    request_planar_reflection : bpy.props.BoolProperty(name="Request Planar Reflection", default=False)
    emissive_color : bpy.props.FloatVectorProperty(name="Emissive Color", subtype='COLOR', size=4)
    shadow_cascade_mask : bpy.props.BoolVectorProperty(name="Shadow Cascade Mask", subtype='LAYER', size=32)

class MuramasaLayer(bpy.types.PropertyGroup):
    is_set : bpy.props.BoolProperty(name="Use Layer Mask", default=False)
    mask : bpy.props.BoolVectorProperty(name="Layer Mask", subtype='LAYER', size=32, default=(
        True, True, True, True, True, True, True, True,
        True, True, True, True, True, True, True, True,
        True, True, True, True, True, True, True, True,
        True, True, True, True, True, True, True, True
    ))

class MuramasaMesh(bpy.types.PropertyGroup):
    lod_mode : bpy.props.EnumProperty(
        name="LOD Mode",
        description = "How will the prefab be loaded",
        items=[
            ("NONE","None",""),
            ("STANDARD","Standard",""),
            ("HDM","HDM","")
        ]
    )

class MuramasaMaterial(bpy.types.PropertyGroup):
    shadow_cast : bpy.props.BoolProperty(name="Cast Shadow", default=True)
    use_vertex_colors : bpy.props.BoolProperty(name="Use Vertex Colors", default=False)
    workflow_specgloss : bpy.props.BoolProperty(name="Specular Glossiness Workflow", default=False)
    occlussion_primary : bpy.props.BoolProperty(name="Enable Primary Occlussion", default=False)
    occlussion_secondary : bpy.props.BoolProperty(name="Enable Secondary Occlussion", default=False)
    use_wind : bpy.props.BoolProperty(name="Use Wind", default=False)
    shadow_noreceive : bpy.props.BoolProperty(name="Don't Receive Shadow", default=False)
    outline : bpy.props.BoolProperty(name="Enable Outline", default=False)

    shading_rate : bpy.props.EnumProperty(
        name="Shading Rate",
        description = "Set pixel fill rate for the material",
        items=[
            ("1X1","1x1",""),
            ("1X2","1x2",""),
            ("2X1","2x1",""),
            ("2X2","2x2",""),
            ("2X4","2x4",""),
            ("4X2","4x2",""),
            ("4x4","4x4","")
        ]
    )

    tex_anim_dir : bpy.props.FloatVectorProperty(name="Texture Scroll Direction", size=2)
    tex_anim_framerate : bpy.props.FloatProperty(name="Texture Scroll Framerate", min=0.0)
    tex_anim_elapsedtime : bpy.props.FloatProperty(name="Texture Scroll Rate", min=0.0)

class MuramasaCollider(bpy.types.PropertyGroup):
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

class MuramasaDecal(bpy.types.PropertyGroup):
    is_set : bpy.props.BoolProperty(name="Use Decal", default=False)
    material : bpy.props.PointerProperty(name="Material", type=bpy.types.Material)

class MuramasaEmitter(bpy.types.PropertyGroup):
    is_set : bpy.props.BoolProperty(name="Use Emitter", default=False)
    material : bpy.props.PointerProperty(name="Material", type=bpy.types.Material)
    shadertype : bpy.props.EnumProperty(
        name="Shader Type",
        description = "Which type of shader to be used in runtime",
        items=[
            ("SOFT","Soft",""),
            ("SOFT_DISTORTION","Soft with Distortion",""),
            ("SIMPLE","Simple",""),
            ("SOFT_LIGHTING","Soft with Lighting affected",""),
        ]
    )
    size : bpy.props.FloatProperty(name="Size", default=1.0)
    random_factor : bpy.props.FloatProperty(name="Random Factor", default=1.0)
    normal_factor : bpy.props.FloatProperty(name="Normal Factor", default=1.0)
    count : bpy.props.FloatProperty(name="Emitter Count", default=0.0)
    life : bpy.props.FloatProperty(name="Emitter Lifetime", default=1.0)
    random_life : bpy.props.FloatProperty(name="Emitter Lifetime Randomness", default=1.0)
    scale : bpy.props.FloatVectorProperty(name="Emitter Scale", size=2)
    rotation : bpy.props.FloatProperty(name="Emitter Rotation", default=1.0)
    motion_blur_amount : bpy.props.FloatProperty(name="Motion Blur Amount", default=0.0)
    mass : bpy.props.FloatProperty(name="Mass", default=1.0)
    random_color : bpy.props.FloatProperty(name="Emitter Color Randomness", default=1.0)
    velocity : bpy.props.FloatVectorProperty(name="Starting Velocity", size=3)
    gravity : bpy.props.FloatVectorProperty(name="Constant Gravity Force", size=3)
    drag : bpy.props.FloatProperty(name="Drag", default=1.0)
    restitution : bpy.props.FloatProperty(name="Restitution", default=1.0)
    sph_h : bpy.props.FloatProperty(name="SPH Smoothing Radius (h)", default=1.0)
    sph_K : bpy.props.FloatProperty(name="SPH Pressure Constant (K)", default=250.0)
    sph_p0 : bpy.props.FloatProperty(name="SPH Reference Density (p0)", default=1.0)
    sph_e : bpy.props.FloatProperty(name="SPH Viscocity Constant (e)", default=0.018)
    sprite_frames : bpy.props.IntVectorProperty(name="Spritesheet Frames Area (X,Y)", size=2, min=0)
    sprite_framecount : bpy.props.IntProperty(name="Spritesheet Frame Count", default=1, min=0)
    sprite_framestart : bpy.props.IntProperty(name="Spritesheet Starting Frame", default=0, min=0)
    sprite_framerate : bpy.props.FloatProperty(name="Spritesheet Animation Frame Rate", default=0, min=0)


classes = (
    MuramasaPrefabInstance,
    MuramasaPrefab,
    MuramasaObject,
    MuramasaLayer,
    MuramasaMaterial,
    MuramasaMesh,
    MuramasaCollider,
    MuramasaDecal,
    MuramasaEmitter
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.types.Scene.muramasa_project_root = bpy.props.StringProperty(name="Project Root", default="", subtype="FILE_PATH", options={'HIDDEN'})
    
    bpy.types.ParticleSettings.muramasa_hairparticle_distance = bpy.props.FloatProperty(name="View Distance", default=10.0, options={'HIDDEN'})
    bpy.types.Material.muramasa_material = bpy.props.PointerProperty(type=MuramasaMaterial, options={'HIDDEN'})
    bpy.types.Mesh.muramasa_mesh = bpy.props.PointerProperty(type=MuramasaMesh, options={'HIDDEN'})
    bpy.types.Object.muramasa_object = bpy.props.PointerProperty(type=MuramasaObject, options={'HIDDEN'})
    bpy.types.Object.muramasa_layer = bpy.props.PointerProperty(type=MuramasaLayer, options={'HIDDEN'})
    bpy.types.Object.muramasa_script = bpy.props.StringProperty(name="Script File", subtype="FILE_PATH", options={'HIDDEN'})
    bpy.types.Object.muramasa_collider = bpy.props.PointerProperty(type=MuramasaCollider, options={'HIDDEN'})
    bpy.types.Object.muramasa_decal = bpy.props.PointerProperty(type=MuramasaDecal, options={'HIDDEN'})
    bpy.types.Object.muramasa_emitter = bpy.props.PointerProperty(type=MuramasaEmitter, options={'HIDDEN'})
    bpy.types.Object.muramasa_rb_extents = bpy.props.FloatVectorProperty(name="Collider Extents", default=(1.0, 1.0, 1.0), options={'HIDDEN'})
    
    bpy.types.Collection.muramasa_prefab = bpy.props.PointerProperty(type=MuramasaPrefab, options={'HIDDEN'})
    bpy.types.Object.muramasa_prefab_instance = bpy.props.PointerProperty(type=MuramasaPrefabInstance, options={'HIDDEN'})


def unregister():
    del bpy.types.Scene.muramasa_project_root

    del bpy.types.ParticleSettings.muramasa_hairparticle_distance
    del bpy.types.Material.muramasa_material
    del bpy.types.Mesh.muramasa_mesh
    del bpy.types.Object.muramasa_object
    del bpy.types.Object.muramasa_layer
    del bpy.types.Object.muramasa_script
    del bpy.types.Object.muramasa_collider
    del bpy.types.Object.muramasa_decal
    del bpy.types.Object.muramasa_emitter
    del bpy.types.Object.muramasa_rb_extents

    del bpy.types.Collection.muramasa_prefab
    del bpy.types.Object.muramasa_prefab_instance

    for c in classes:
        bpy.utils.unregister_class(c)