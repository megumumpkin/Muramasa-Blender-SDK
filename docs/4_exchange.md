# Exchangable Data Between Blender and WickedEngine

Some of the default data on Blender are able to be exported to WickedEngine, since the underlying tech are utilizing GLTF as a transmission format you may need to first refer to Blender's GLTF Manual: https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html

This addon extends the scope on additional data that will be transferred to the engine, which will be expanded upon below.

## Object Data

- **Object Color** : Sets the object color, will multiply the object's diffuse material color to this object color <br> <h5>Location : Properties Editor > Object Editor > Viewport Display > Color</h5>

## Hair Particle Data

- **Number** : Sets the amount of hair particle spawn on the surface <br> <h5> Location : Properties Editor > Particle Editor > Hair Particle > Emission > Number </h5>

- **Seed** : Sets the seed of the placement of the hair particle <br> <h5> Location : Properties Editor > Particle Editor > Hair Particle > Emission > Seed </h5>

- **Hair Length** : Sets the size of the hair particle <br> <h5> Location : Properties Editor > Particle Editor > Hair Particle > Emission > Hair Length </h5>

- **Segments** : Sets the number of segments of a single strand (the actual amount is `segments-1`) <br> <h5> Location : Properties Editor > Particle Editor > Hair Particle > Emission > Segments </h5>

- **Stiffness** : Sets the stiffness of the hair particle <br> <h5> Location : Properties Editor > Particle Editor > Hair Particle > Hair Dynamics > Structure > Stiffness </h5>

- **Randomness** : Sets the randomness of the hair particle <br> <h5> Location : Properties Editor > Particle Editor > Hair Particle > Hair Dynamics > Structure > Random </h5>

- **Material** : Sets the material of the particle <br> <h5> Location : Properties Editor > Particle Editor > Hair Particle > Render > Material</h5>

- **Density + Length** : Use the density vertex group pointer to affect both density and length per vertex faces. To make it more visually accurate in blender you may want to set the same vertex group that you use for `Density` into `Length`<br> <h5> Location : Properties Editor > Particle Editor > Hair Particle > Vertex Groups > Density</h5>

## Force Field Data
- **Strength** : Sets the strength of the force field <br> <h5> Location : Properties Editor > Physics Editor > Force Field > Settings > Strength</h5>
- **Max Range** : Sets the maximum range of the force field, minimum is always `0.0` <br> <h5> Location : Properties Editor > Physics Editor > Force Field > Falloff > Max Distance </h5>

## Rigid Body Data
- **Shape** : Sets the shape of the rigid body physics object <br> <h5> Location : Properties Editor > Physics Editor > Rigid Body > Collisions > Shape </h5>
- **Mass** : Sets the mass of the rigid body <br> <h5> Location : Properties Editor > Physics Editor > Rigid Body > Settings > Mass </h5>
- **Friction** : Sets the friction of the rigid body <br> <h5> Location : Properties Editor > Physics Editor > Rigid Body > Surface Response > Friction </h5>
- **Restitution** : Sets the restitution of the rigid body <br> <h5> Location : Properties Editor > Physics Editor > Rigid Body > Surface Response > Bounciness </h5>
- **Linear Damping** : Sets the linear damping of the rigid body <br> <h5> Location : Properties Editor > Physics Editor > Rigid Body > Dynamics > Damping Translation </h5>
- **Angular Damping** : Sets the linear damping of the rigid body <br> <h5> Location : Properties Editor > Physics Editor > Rigid Body > Dynamics > Rotation </h5>

## Soft Body Data
- **Mass** : Sets the mass of the soft body <br> <h5> Location : Properties Editor > Physics Editor > Soft Body > Object > Mass </h5>
- **Friction** : Sets the friction of the soft body <br> <h5> Location : Properties Editor > Physics Editor > Soft Body > Object > Friction </h5>
- **Restitution** **[TODO?]** : Sets the restitution of the soft body <br> <h5> Location : Properties Editor > Physics Editor > Soft Body > ??? </h5>

## Bone's Inverse Kinematics Constraint
- **Target** : Sets the IK target <br> <h5> Location : Properties Editor > Bone Constraint Editor > Inverse Kinematics > Target </h5>
- **Chain Length** : Sets the IK chain length <br> <h5> Location : Properties Editor > Bone Constraint Editor > Inverse Kinematics > Chain Length </h5>
- **Iterations** : Sets the IK iteration per frame (the higher the iteration the more possibilities of the pose be resolved), 50 or less iterations are recommended <br> <h5> Location : Properties Editor > Bone Constraint Editor > Inverse Kinematics > Iterations </h5>