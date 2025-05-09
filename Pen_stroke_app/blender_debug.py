#run this code inside blender UI to visualize the geometry and camera position generated from the csv file

import bpy
import csv
import bmesh
from mathutils import Vector

# === CSV paths relative to this .blend file ===
build_csv  = bpy.path.abspath('//build.csv')
camera_csv = bpy.path.abspath('//camera.csv')

# === Clear existing scene ===
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# === Use metric units ===
scene = bpy.context.scene
scene.unit_settings.system       = 'METRIC'
scene.unit_settings.scale_length = 1.0

# === Read build.csv and group footprints ===
groups, heights = {}, {}
with open(build_csv, newline='') as f:
    for row in csv.DictReader(f):
        id_str = row['ID']
        x, y   = float(row['X(m)']), float(row['Y(m)'])
        h      = float(row['h'])
        groups.setdefault(id_str, []).append((x, y))
        heights[id_str] = h

# === Create extruded meshes for each footprint ===
for id_str, pts in groups.items():
    if len(pts) < 3: continue
    verts2d = [Vector((x, y, 0)) for x, y in pts]
    if verts2d[0] != verts2d[-1]:
        verts2d.append(verts2d[0])

    mesh = bpy.data.meshes.new(f"fp_{id_str}")
    obj  = bpy.data.objects.new(f"bld_{id_str}", mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    bm_vs = [bm.verts.new(v) for v in verts2d]
    bmesh.ops.contextual_create(bm, geom=bm_vs)
    bm.faces.ensure_lookup_table()

    extr = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
    evs  = [v for v in extr['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=evs, vec=(0, 0, heights[id_str]))

    bm.to_mesh(mesh)
    bm.free()

# === Apply white material to buildings ===
mat = bpy.data.materials.new("Mat_Build")
mat.use_nodes = True
p = mat.node_tree.nodes["Principled BSDF"]
p.inputs["Base Color"].default_value = (0.9, 0.9, 0.9, 1)
p.inputs["Roughness"].default_value = 0.8
for o in scene.objects:
    if o.type == 'MESH' and not o.data.materials:
        o.data.materials.append(mat)

# === Add a large ground plane ===
bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"
gmat = bpy.data.materials.new("Mat_Ground")
gmat.use_nodes = True
gp = gmat.node_tree.nodes["Principled BSDF"]
gp.inputs["Base Color"].default_value = (0.3, 0.3, 0.3, 1)
gp.inputs["Roughness"].default_value = 1.0
ground.data.materials.append(gmat)

# === Place camera markers ===
with open(camera_csv, newline='') as f:
    for i, row in enumerate(csv.DictReader(f), start=1):
        x, y = float(row['x']), float(row['y'])
        z    = 1.6
        bpy.ops.object.empty_add(type='ARROWS', location=(x, y, z))
        e = bpy.context.active_object
        e.name = f"Cam_{i}"
        e.empty_display_size = 1.0

# === Position the viewport camera for overview ===
cam = bpy.data.objects.get("Camera")
if cam:
    cam.location = (0, -150, 100)
    cam.rotation_euler = (1.1, 0, 0)

print("✅ Debug visualization set up—inspect extrusions and camera markers in the viewport.")
