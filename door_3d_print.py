import bpy
import bmesh

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
cube = bpy.context.object
cube.name = "Cube"
cube.scale[0] = 5.13*0.0254
cube.scale[1] = 0.3*0.0254
cube.scale[2] = 0.15*0.0254

for x in [-2.01*0.0254,2.01*0.0254]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x,(-1.53/2)*0.0254,-0.055*0.0254))
    cube = bpy.context.object
    cube.name = f"leg_{x}"
    cube.scale[0] = 0.8*0.0254
    cube.scale[1] = 1.53*0.0254
    cube.scale[2] = 0.04*0.0254

def create_triangular_prism(location):
    mesh = bpy.data.meshes.new(name="Triangular_Prism")
    tri_prism = bpy.data.objects.new(name="Triangular_Prism", object_data=mesh)
    bpy.context.collection.objects.link(tri_prism)
    tri_prism.location = location

    bpy.context.view_layer.objects.active = tri_prism
    tri_prism.select_set(True)

    bm = bmesh.new()
    verts = [
        bm.verts.new((0.2*0.0254,-0.15*0.0254,-0.075*0.0254)),
        bm.verts.new((0.2*0.0254,(-0.15-0.4)*0.0254,-0.075*0.0254)),
        bm.verts.new((0.2*0.0254,-0.15*0.0254,0.075*0.0254)),
        bm.verts.new((-0.2*0.0254,-0.15*0.0254,-0.075*0.0254)),
        bm.verts.new((-0.2*0.0254,(-0.15-0.4)*0.0254,-0.075*0.0254)),
        bm.verts.new((-0.2*0.0254,-0.15*0.0254,0.075*0.0254)),
    ]

    faces = [
        (0, 1, 2),
        (3, 4, 5),
        (0, 1, 4, 3),
        (1, 2, 5, 4),
        (2, 0, 3, 5),
    ]

    for face in faces:
        bm.faces.new([verts[i] for i in face])

    bm.to_mesh(mesh)
    bm.free()

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')


bpy.ops.mesh.primitive_cube_add(size=1, location=((0.8+0.075)*0.0254,1.15*0.0254,0))
cube = bpy.context.object
cube.name = "arm_right"
cube.scale[0] = 0.15*0.0254
cube.scale[1] = 2*0.0254
cube.scale[2] = 0.15*0.0254

bpy.ops.mesh.primitive_cube_add(size=1, location=((-0.8-0.2)*0.0254,1.15*0.0254,-0.0375*0.0254))
cube = bpy.context.object
cube.name = "arm_left"
cube.scale[0] = 0.4*0.0254
cube.scale[1] = 2*0.0254
cube.scale[2] = 0.075*0.0254

for y in [1,5,9,13,17,21,25,29,33,37,41]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=((-0.8-0.2)*0.0254,(y/21+0.15)*0.0254,0.0375*0.0254))
    cube = bpy.context.object
    cube.name = f"ladder_{y}"
    cube.scale[0] = 0.4*0.0254
    cube.scale[1] = (2/21)*0.0254
    cube.scale[2] = 0.075*0.0254

create_triangular_prism((2.01*0.0254,0,0))
create_triangular_prism((-2.01*0.0254,0,0))

