import bpy
import csv
import os
import bmesh
from mathutils import Vector

# === File paths ===
blend_dir = os.path.dirname(bpy.data.filepath)
build_csv = os.path.join(blend_dir, "app_output_form/build.csv")
camera_csv = os.path.join(blend_dir, "app_output_form/camera.csv")
output_dir = os.path.join(blend_dir, "panorama_input")
os.makedirs(output_dir, exist_ok=True)

# === Clear existing scene ===
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# === Set units to metric ===
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# === Load and parse build.csv ===
groups = {}
heights = {}
with open(build_csv, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id_str = row['ID']
        x = float(row['X(m)'])
        y = float(row['Y(m)'])
        h = float(row['h'])
        groups.setdefault(id_str, []).append((x, y))
        heights[id_str] = h

# === Generate extruded geometry ===
for id_str, points in groups.items():
    if id_str not in heights or len(points) < 3:
        continue
    verts = [Vector((x, y, 0)) for x, y in points]
    if verts[0] != verts[-1]:
        verts.append(verts[0])
    mesh_data = bpy.data.meshes.new(f"building_{id_str}")
    mesh_obj  = bpy.data.objects.new(f"building_{id_str}", mesh_data)
    bpy.context.collection.objects.link(mesh_obj)
    bm = bmesh.new()
    bm_verts = [bm.verts.new(v) for v in verts]
    bmesh.ops.contextual_create(bm, geom=bm_verts)
    bm.faces.ensure_lookup_table()
    if not bm.faces:
        bm.free()
        continue
    result = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
    verts_ex = [v for v in result['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts_ex, vec=(0, 0, heights[id_str]))
    bm.to_mesh(mesh_data)
    bm.free()

# === Apply light-blue material to all massing ===
blue_mat = bpy.data.materials.new(name="LightBlue")
blue_mat.use_nodes = True
bsdf = blue_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0, 0.1, 0.2, 1)
bsdf.inputs["Roughness"].default_value = 0.8
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and not obj.data.materials:
        obj.data.materials.append(blue_mat)

# === Add a large dark-gray ground plane ===
bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "GroundPlane"
ground_mat = bpy.data.materials.new(name="DarkGray")
ground_mat.use_nodes = True
g_bsdf = ground_mat.node_tree.nodes["Principled BSDF"]
g_bsdf.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1)
g_bsdf.inputs["Roughness"].default_value = 1.0
ground.data.materials.append(ground_mat)

# === Setup deep-blue 'Nishita' sky ===
scene.render.engine = 'CYCLES'
world = scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()
bg = nodes.new("ShaderNodeBackground")
sky = nodes.new("ShaderNodeTexSky")
out = nodes.new("ShaderNodeOutputWorld")
sky.sky_type      = 'NISHITA'
sky.sun_elevation = 1.2
sky.sun_rotation  = 2.0
sky.turbidity     = 2
bg.inputs['Strength'].default_value = 0.8
links.new(sky.outputs['Color'], bg.inputs['Color'])
links.new(bg.outputs['Background'], out.inputs['Surface'])

# === Add a slightly weaker sun lamp ===
sun = bpy.data.lights.new(name="Sun", type='SUN')
sun.energy = 3.0
sun.angle  = 0.03
sun_obj = bpy.data.objects.new(name="Sun", object_data=sun)
bpy.context.collection.objects.link(sun_obj)
sun_obj.location = (0, 0, 100)
sun_obj.rotation_euler = (1.1, 0.3, 0.8)

# === Create panoramic camera ===
cam_data = bpy.data.cameras.new(name='PanoCam')
cam_data.type = 'PANO'
cam_data.panorama_type = 'EQUIRECTANGULAR'
cam_data.clip_start = 0.1
cam_data.clip_end   = 1000
cam_obj  = bpy.data.objects.new('PanoCam', cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# === Render settings ===
scene.render.resolution_x = 4096 # Bring this down to make sure it runs quick (ratio should be 2:1)
scene.render.resolution_y = 2048 # Bring this down to make sure it runs quick (ratio should be 2:1)
scene.render.image_settings.file_format = 'JPEG'
scene.cycles.samples     = 128
scene.cycles.use_denoising= True
scene.cycles.max_bounces  = 8
scene.cycles.min_bounces  = 3

# === Render a panorama for each camera position ===
with open(camera_csv, newline='') as csvfile:
    for i, row in enumerate(csv.DictReader(csvfile)):
        x, y = float(row['x']), float(row['y'])
        cam_obj.location = (x, y, 2.5)
        cam_obj.rotation_euler = (1.5708, 0, 0)
        scene.render.filepath  = os.path.join(output_dir, f"panorama_{i+1}.jpg")
        bpy.ops.render.render(write_still=True)
        print(f"✅ Saved: panorama_{i+1}.jpg")

print("🎉 All done — new renders have replaced the old files.")
