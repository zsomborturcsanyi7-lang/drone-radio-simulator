# -*- coding: utf-8 -*-
import bpy
import math

def create_uav():
    # Alaphelyzet
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # ANYAGOK LÉTREHOZÁSA
    carbon = bpy.data.materials.new(name="CarbonFiber")
    carbon.diffuse_color = (0.02, 0.02, 0.02, 1)
    
    metal = bpy.data.materials.new(name="Aluminum")
    metal.diffuse_color = (0.7, 0.7, 0.7, 1)
    metal.metallic = 0.9

    # 1. KÖZPONTI VÁZ (Core Frame)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    frame = bpy.context.object
    frame.scale = (2.5, 1.2, 0.4)
    frame.data.materials.append(carbon)

    # 2. HIBRID GENERÁTOR EGYSÉG (Detailed assembly)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.4, 0, 0.5))
    gen_box = bpy.context.object
    gen_box.scale = (1.2, 1.2, 1.5)
    gen_box.data.materials.append(metal)
    gen_box.name = "Generator_Core"

    # 3. KAROK, ESC-k ÉS MOTOROK
    arm_coords = [(1.8, 1.3), (1.8, -1.3), (-1.8, 1.3), (-1.8, -1.3)]
    for i, (ax, ay) in enumerate(arm_coords):
        # Kar cső
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=4.288, location=(ax/2, ay/2, 0))
        arm_obj = bpy.context.object
        arm_obj.rotation_euler[2] = math.atan2(ay, ax)
        arm_obj.rotation_euler[1] = math.pi/2
        arm_obj.data.materials.append(carbon)

        # Motor tartó és Motor
        bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.2, location=(ax, ay, 0.15))
        motor_obj = bpy.context.object
        motor_obj.data.materials.append(metal)
        motor_obj.name = f"Motor_{i}"

    # 4. EMI SHIELD (Faraday Cage)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.8))
    shield = bpy.context.object
    shield.scale = (1.5, 1.3, 0.5)
    shield.data.materials.append(metal)

    # 5. HF ANTENNA RENDSZER
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=2.5, location=(2.8, 0, 1.5))
    bpy.context.object.name = "HF_Antenna_Array"

create_uav()
