import bpy
import math

# Dimensions (in meters)
block1_x = 1.55*0.0254
block1_y = 1.17*0.0254
block1_z = 0.34*0.0254

block1_open_x = 0.9*0.0254
block1_open_y = 1.09*0.0254
block1_open_z = 0.07*0.0254

block1_open2_x = 0.21*0.0254
block1_open2_y = block1_y
block1_open2_z = block1_open_z

block1_cut_x = 0.126*0.0254
block1_cut_y = 0.2*0.0254
block1_cut_z = block1_z

block1_hole_radius = 0.07*0.0254
block1_hole_height = block1_z
block1_hole_x = (1.15/2+0.05)*0.0254
block1_hole_y = block1_y/2-0.14*0.0254

reward_hole_radius = 0.45*0.0254
reward_hole_height = 1.09*0.0254

cylinder_radius = 0.576*0.0254
cylinder_height = 0.85*0.0254

outter_tube_radius = 0.105*0.0254
outter_tube_height = 0.75*0.0254

inner_tube_radius = 0.0375*0.0254
inner_tube_height = 1*0.0254

def boolen_modifier(object_1,object_2):
    bpy.context.view_layer.objects.active = object_1
    bpy.ops.object.modifier_add(type='BOOLEAN')
    object_1.modifiers["Boolean"].operation = 'DIFFERENCE'
    object_1.modifiers["Boolean"].object = object_2
    bpy.ops.object.modifier_apply(modifier="Boolean")
    bpy.data.objects.remove(object_2, do_unlink=True)
    
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 
                                                  0, 
                                                  0.5*block1_z))
Block1 = bpy.context.object
Block1.scale[0] = block1_x
Block1.scale[1] = block1_y
Block1.scale[2] = block1_z

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 
                                                  block1_y-block1_open_y, 
                                                  0.5*block1_open_z))
Block1_open = bpy.context.object
Block1_open.scale[0] = block1_open_x
Block1_open.scale[1] = block1_open_y
Block1_open.scale[2] = block1_open_z
boolen_modifier(Block1,Block1_open)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 
                                                  0, 
                                                  0.5*block1_open_z))
Block1_open2 = bpy.context.object
Block1_open2.scale[0] = block1_open2_x
Block1_open2.scale[1] = block1_open2_y
Block1_open2.scale[2] = block1_open2_z
boolen_modifier(Block1,Block1_open2)

bpy.ops.mesh.primitive_cube_add(size=1, location=(block1_x/2-block1_cut_x/2, 
                                                  0,
                                                  0.5*block1_cut_z))
Block1_left_cut = bpy.context.object
Block1_left_cut.scale[0] = block1_cut_x
Block1_left_cut.scale[1] = block1_cut_y
Block1_left_cut.scale[2] = block1_cut_z
boolen_modifier(Block1,Block1_left_cut)

bpy.ops.mesh.primitive_cube_add(size=1, location=(-block1_x/2+block1_cut_x/2, 
                                                  0, 
                                                  0.5*block1_cut_z))
Block1_right_cut = bpy.context.object
Block1_right_cut.scale[0] = block1_cut_x
Block1_right_cut.scale[1] = block1_cut_y
Block1_right_cut.scale[2] = block1_cut_z
boolen_modifier(Block1,Block1_right_cut)

bpy.ops.mesh.primitive_cylinder_add(radius=block1_hole_radius, 
                                    depth=block1_hole_height, 
                                    location=(block1_hole_x, block1_hole_y, block1_z/2))
Block1_hole_1 = bpy.context.object
boolen_modifier(Block1,Block1_hole_1)

bpy.ops.mesh.primitive_cylinder_add(radius=block1_hole_radius, 
                                    depth=block1_hole_height, 
                                    location=(-block1_hole_x, block1_hole_y, block1_z/2))
Block1_hole_2 = bpy.context.object
boolen_modifier(Block1,Block1_hole_2)

bpy.ops.mesh.primitive_cylinder_add(radius=block1_hole_radius, 
                                    depth=block1_hole_height, 
                                    location=(block1_hole_x, -block1_hole_y, block1_z/2))
Block1_hole_3 = bpy.context.object
boolen_modifier(Block1,Block1_hole_3)

bpy.ops.mesh.primitive_cylinder_add(radius=block1_hole_radius, 
                                    depth=block1_hole_height, 
                                    location=(-block1_hole_x, -block1_hole_y, block1_z/2))
Block1_hole_4 = bpy.context.object
boolen_modifier(Block1,Block1_hole_4)

bpy.ops.mesh.primitive_cylinder_add(radius=reward_hole_radius, 
                                    depth=reward_hole_height, 
                                    location=(0, 0, reward_hole_height/2))
Reward_hole = bpy.context.object
boolen_modifier(Block1,Reward_hole)

bpy.ops.mesh.primitive_cylinder_add(radius=block1_hole_radius, 
                                    depth=block1_hole_height, 
                                    location=((block1_x/2-block1_cut_x-block1_open_x/2)/2+block1_open_x/2, 
                                              0, block1_z/2))
Block1_hole_5 = bpy.context.object
Block1_hole_5.rotation_euler[1] = math.radians(90)
boolen_modifier(Block1,Block1_hole_5)

bpy.ops.mesh.primitive_cylinder_add(radius=block1_hole_radius, 
                                    depth=block1_hole_height, 
                                    location=(-(block1_x/2-block1_cut_x-block1_open_x/2)/2-block1_open_x/2, 
                                              0, block1_z/2))
Block1_hole_6 = bpy.context.object
Block1_hole_6.rotation_euler[1] = math.radians(-90)
boolen_modifier(Block1,Block1_hole_6)

bpy.ops.mesh.primitive_cylinder_add(radius=cylinder_radius, 
                                    depth=cylinder_height, 
                                    location=(0,0,cylinder_height/2+block1_z))
Cylinder = bpy.context.object
bpy.ops.mesh.primitive_cylinder_add(radius=reward_hole_radius, 
                                    depth=reward_hole_height, 
                                    location=(0, 0, reward_hole_height/2))
Reward_hole = bpy.context.object
boolen_modifier(Cylinder,Reward_hole)

bpy.ops.mesh.primitive_cylinder_add(radius=outter_tube_radius, 
                                    depth=outter_tube_height, 
                                    location=(0,
                                              cylinder_radius,
                                              block1_z+cylinder_height))
Outter_tube = bpy.context.object
Outter_tube.rotation_euler[0] = math.radians(-45)
bpy.ops.mesh.primitive_cylinder_add(radius=reward_hole_radius, 
                                    depth=reward_hole_height, 
                                    location=(0, 0, reward_hole_height/2))
Reward_hole = bpy.context.object
boolen_modifier(Outter_tube,Reward_hole)
bpy.ops.mesh.primitive_cylinder_add(radius=inner_tube_radius, 
                                    depth=inner_tube_height, 
                                    location=(0,
                                              cylinder_radius,
                                              block1_z+cylinder_height))
Inner_tube = bpy.context.object
Inner_tube.rotation_euler[0] = math.radians(-45)
boolen_modifier(Outter_tube,Inner_tube)

bpy.ops.mesh.primitive_cylinder_add(radius=inner_tube_radius, 
                                    depth=inner_tube_height, 
                                    location=(0,
                                              cylinder_radius,
                                              block1_z+cylinder_height))
Inner_tube = bpy.context.object
Inner_tube.rotation_euler[0] = math.radians(-45)
boolen_modifier(Cylinder,Inner_tube)