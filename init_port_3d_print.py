import bpy
import bmesh
import math

# Dimensions (in meters)
outer_radius = 0.53*0.0254
thickness = 0.08*0.0254
inner_radius = outer_radius - thickness
height = 1.3*0.0254
bottom_height = 0.13*0.0254
bottom_hole_radius = 0.04*0.0254
bottom_tube_radius = 0.08*0.0254
bottom_tube_length = 0.23*0.0254
side_hole_radius = 0.07*0.0254
side_hole2_z = 0.35*0.0254

# Cutting plane parameters
z_intercept = 0.718*0.0254
x_intercept = 0.9265*0.0254

# Delete existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def boolen_modifier(object_1,object_2):
    bpy.context.view_layer.objects.active = object_1
    bpy.ops.object.modifier_add(type='BOOLEAN')
    object_1.modifiers["Boolean"].operation = 'DIFFERENCE'
    object_1.modifiers["Boolean"].object = object_2
    bpy.ops.object.modifier_apply(modifier="Boolean")
    bpy.data.objects.remove(object_2, do_unlink=True)

# Create cylinder
bpy.ops.mesh.primitive_cylinder_add(radius=outer_radius, depth=height, location=(0, 0, 0))
outer_cylinder = bpy.context.object
bpy.ops.mesh.primitive_cylinder_add(radius=inner_radius, depth=height, location=(0, 0, 0))
inner_cylinder = bpy.context.object
boolen_modifier(outer_cylinder,inner_cylinder)

# Cut the cylinder
bpy.ops.mesh.primitive_cube_add(size=1, location=(x_intercept,0,z_intercept))
cutting_cube = bpy.context.object
cutting_cube.scale[0] = (z_intercept*x_intercept/(z_intercept**2+x_intercept**2)**0.5)*2
cutting_cube.scale[1] = 2*outer_radius
cutting_cube.scale[2] = (x_intercept*x_intercept/(z_intercept**2+x_intercept**2)**0.5)*2
angle = math.atan2(z_intercept, x_intercept)
cutting_cube.rotation_euler = (0,-(angle), 0)
boolen_modifier(outer_cylinder,cutting_cube)

# Create side hole
bpy.ops.mesh.primitive_cylinder_add(radius=side_hole_radius, depth=2*outer_radius, location=(0, 0, 0))
side_hole_1 = bpy.context.object
bpy.context.object.rotation_euler[0] = 0.5*math.pi
boolen_modifier(outer_cylinder,side_hole_1)
bpy.ops.mesh.primitive_cylinder_add(radius=side_hole_radius, depth=2*outer_radius, location=(0, 0, side_hole2_z))
side_hole_1 = bpy.context.object
bpy.context.object.rotation_euler[0] = 0.5*math.pi
boolen_modifier(outer_cylinder,side_hole_1)

# Create bottom
bpy.ops.mesh.primitive_cylinder_add(radius=outer_radius, depth=bottom_height, location=(0,0,-0.5*height-0.5*bottom_height))
bottom = bpy.context.object
bpy.ops.mesh.primitive_cylinder_add(radius=bottom_hole_radius, depth=bottom_height, location=(0,0,-0.5*height-0.5*bottom_height))
bottom_hole = bpy.context.object
boolen_modifier(bottom,bottom_hole)

# Create bottom tube
bpy.ops.mesh.primitive_cylinder_add(radius=bottom_tube_radius, depth=bottom_tube_length, 
                                    location=(0,0,-0.5*height-bottom_height-0.5*bottom_tube_length))
bottom_tube = bpy.context.object
bpy.ops.mesh.primitive_cylinder_add(radius=bottom_hole_radius, depth=bottom_tube_length,
                                    location=(0,0,-0.5*height-bottom_height-0.5*bottom_tube_length))
bottom_tube_hole = bpy.context.object
boolen_modifier(bottom_tube,bottom_tube_hole)

# Create a block plate
mesh = bpy.data.meshes.new('TrapezoidPrism')
block_plate = bpy.data.objects.new('TrapezoidPrism', mesh)

bpy.context.collection.objects.link(block_plate)

bm = bmesh.new()

verts = [
    bm.verts.new((-0.06*0.0254,(1.18/2)*0.0254,(-0.68/2)*0.0254)),       # Bottom-left
    bm.verts.new((0.06*0.0254,1.18*0.0254/2,-0.68*0.0254/2)),       # Bottom-right
    bm.verts.new((0.06*0.0254,1.18*0.0254/2,0.82*0.0254/2)),     # Top-right
    bm.verts.new((-0.06*0.0254,1.18*0.0254/2,(0.67-0.82/2)*0.0254)),     # Top-left
    bm.verts.new((-0.06*0.0254,-1.18*0.0254/2,-0.68*0.0254/2)),       # Bottom-left (back)
    bm.verts.new((0.06*0.0254,-1.18*0.0254/2,-0.68*0.0254/2)),       # Bottom-right (back)
    bm.verts.new((0.06*0.0254,-1.18*0.0254/2,0.82*0.0254/2)),     # Top-right (back)
    bm.verts.new((-0.06*0.0254,-1.18*0.0254/2,(0.67-0.82/2)*0.0254))      # Top-left (back)
]

edges = [
    bm.edges.new((verts[0], verts[1])),
    bm.edges.new((verts[1], verts[2])),
    bm.edges.new((verts[2], verts[3])),
    bm.edges.new((verts[3], verts[0])),
    bm.edges.new((verts[4], verts[5])),
    bm.edges.new((verts[5], verts[6])),
    bm.edges.new((verts[6], verts[7])),
    bm.edges.new((verts[7], verts[4])),
    bm.edges.new((verts[0], verts[4])),
    bm.edges.new((verts[1], verts[5])),
    bm.edges.new((verts[2], verts[6])),
    bm.edges.new((verts[3], verts[7])),
]

faces = [
    bm.faces.new((verts[0], verts[1], verts[2], verts[3])),
    bm.faces.new((verts[4], verts[5], verts[6], verts[7])),
    bm.faces.new((verts[0], verts[1], verts[5], verts[4])),
    bm.faces.new((verts[1], verts[2], verts[6], verts[5])),
    bm.faces.new((verts[2], verts[3], verts[7], verts[6])),
    bm.faces.new((verts[3], verts[0], verts[4], verts[7]))
]

bm.to_mesh(mesh)
bm.free()
mesh.update()
block_plate.rotation_euler = (0,-(angle), 0)
block_plate.location.x += 0.67*0.0254
block_plate.location.z += 0.0005371
bpy.context.view_layer.update()

# Ensure the object is selected
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Rotate the object to lay flat on the build plate (adjust angles as needed)
for obj in bpy.context.selected_objects:
    obj.rotation_euler[0] = math.radians(180)
    obj.rotation_euler[1] = math.radians(90)-angle