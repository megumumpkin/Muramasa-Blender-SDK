# Muramasa Blender SDK

![](docs/res/header.svg)

###### Blender and it's logo are all owned by Blender Foundation. Box Icon and Left Caret Icon all rights reserved to Font Awesome. Wicked Engine and it's logo all rights reserved to Turanski Janos
A Blender addon for WickedEngine-Demo game development, this turns blender into a game level editor which supports creating common types of components that exists within WickedEngine and this game demo software.

- # [Read the usage manual](https://github.com/megumumpkin/Muramasa-Blender-SDK/wiki/0-%E2%80%90-Setup)

Install by downloading this repo as zip and install through Blender's settings.

The name comes from the blades that are made by Senji Muramasa, the wicked blades.

Under the hood this addon utilizes Blender's internal GLTF import-export addon to accomplish data transmission between Blender and the engine, especially leveraging extensive usage of custom extensions.

Though to note: That the resulting GLTF interchange format is NOT intended to be used as a normal GLTF file since the exporter violates various standards of the GLTF format.

## What are the components that can be exported to the engine?

* Prefabs (Feature that exists within the WickedEngine game demo software)
* Lua Scripts (Exists in Wicked Engine but custom tailored for use in the game demo software)
* Rigidbody Physics
* Softbody Physics
* Physics Constraints
* Decals
* Lights
* Cameras(?)
* Sounds
* Force Fields
* Animations (Only what's supported by base GLTF formats for now)
* Particle Systems (Does not use blender's particle system)
* Hair Particle Systems (This one uses blender's particle system for hair)
* Hair Joints
