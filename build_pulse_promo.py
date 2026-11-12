import bpy
import bmesh
import math
import os

bpy.ops.wm.read_homefile(use_empty=True)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 216
scene.render.use_motion_blur = True

eevee = scene.eevee
eevee.use_raytracing = True
eevee.taa_render_samples = 16
eevee.use_fast_gi = True
eevee.fast_gi_quality = 0.8
eevee.gi_diffuse_bounces = 3
if hasattr(eevee, 'ray_tracing_options'):
    eevee.ray_tracing_options.screen_trace_quality = 0.5
    eevee.ray_tracing_options.trace_max_roughness = 0.7

scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - High Contrast'

world = bpy.data.worlds.new('PulseStudioWorld')
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get('Background')
if bg_node:
    bg_node.inputs['Color'].default_value = (0.012, 0.012, 0.016, 1.0)
    bg_node.inputs['Strength'].default_value = 0.5

font_file = '/home/akidin/.local/share/fonts/Outfit-Bold.ttf'
outfit_font = bpy.data.fonts.load(font_file) if os.path.exists(font_file) else None

def create_metal_mat(name, color=(0.92, 0.93, 0.96, 1.0), metallic=0.85, roughness=0.15):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = color
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Roughness'].default_value = roughness
    b.inputs['Coat Weight'].default_value = 0.8
    b.inputs['Coat Roughness'].default_value = 0.06
    return mat

def create_emission_mat(name, color=(1.0, 1.0, 1.0, 1.0), strength=20.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1.0)
    b.inputs['Emission Color'].default_value = color
    b.inputs['Emission Strength'].default_value = strength
    return mat

mat_platinum = create_metal_mat('Mat_Platinum', (0.92, 0.93, 0.96, 1.0), 0.88, 0.14)
mat_obsidian = create_metal_mat('Mat_Obsidian', (0.02, 0.02, 0.025, 1.0), 0.4, 0.18)
mat_pulse_glow = create_emission_mat('Mat_PulseGlow', (1.0, 1.0, 1.0, 1.0), 22.0)
mat_floor = create_metal_mat('Mat_Floor', (0.018, 0.018, 0.022, 1.0), 0.4, 0.22)

ui_texture_path = '/home/akidin/Documents/games and apps/msg app/pulse_ui_render.png'
mat_screen = bpy.data.materials.new('Mat_ScreenUI')
mat_screen.use_nodes = True
s_nodes = mat_screen.node_tree.nodes
s_links = mat_screen.node_tree.links
s_bsdf = s_nodes.get('Principled BSDF')
s_bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
s_bsdf.inputs['Roughness'].default_value = 0.1
s_bsdf.inputs['Coat Weight'].default_value = 1.0
s_bsdf.inputs['Coat Roughness'].default_value = 0.03
s_bsdf.inputs['Emission Strength'].default_value = 1.8

if os.path.exists(ui_texture_path):
    tex_img = s_nodes.new('ShaderNodeTexImage')
    tex_img.image = bpy.data.images.load(ui_texture_path)
    s_links.new(tex_img.outputs['Color'], s_bsdf.inputs['Base Color'])
    s_links.new(tex_img.outputs['Color'], s_bsdf.inputs['Emission Color'])

bpy.ops.mesh.primitive_plane_add(size=120.0, location=(0.0, 0.0, -2.5))
floor = bpy.context.view_layer.objects.active
floor.name = 'StudioFloor'
floor.data.materials.append(mat_floor)

cam_target = bpy.data.objects.new('CamTarget', None)
cam_target.empty_display_type = 'SPHERE'
cam_target.empty_display_size = 0.2
bpy.context.collection.objects.link(cam_target)

cam_data = bpy.data.cameras.new('MainCamera')
cam_data.lens = 38.0
cam_data.dof.use_dof = True
cam_data.dof.focus_object = cam_target
cam_data.dof.aperture_fstop = 3.5
cam_obj = bpy.data.objects.new('PromoCamera', cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

track_c = cam_obj.constraints.new(type='TRACK_TO')
track_c.target = cam_target
track_c.track_axis = 'TRACK_NEGATIVE_Z'
track_c.up_axis = 'UP_Y'

light_top_data = bpy.data.lights.new('TopSoftbox', type='AREA')
light_top_data.energy = 1400.0
light_top_data.size = 10.0
light_top_data.size_y = 8.0
light_top_data.color = (0.96, 0.98, 1.0)
light_top = bpy.data.objects.new('TopSoftbox', light_top_data)
light_top.location = (0.0, -2.0, 7.0)
light_top.rotation_euler = (math.radians(20.0), 0.0, 0.0)
bpy.context.collection.objects.link(light_top)

light_key_data = bpy.data.lights.new('KeyArea', type='AREA')
light_key_data.energy = 1100.0
light_key_data.size = 6.0
light_key_data.size_y = 4.0
light_key_data.color = (0.95, 0.98, 1.0)
light_key = bpy.data.objects.new('KeyArea', light_key_data)
light_key.location = (6.0, -6.0, 4.0)
light_key.rotation_euler = (math.radians(45.0), 0.0, math.radians(35.0))
bpy.context.collection.objects.link(light_key)

light_rim_data = bpy.data.lights.new('RimArea', type='AREA')
light_rim_data.energy = 1300.0
light_rim_data.size = 10.0
light_rim_data.size_y = 2.0
light_rim_data.color = (0.92, 0.96, 1.0)
light_rim = bpy.data.objects.new('RimArea', light_rim_data)
light_rim.location = (-7.0, 4.0, 4.0)
light_rim.rotation_euler = (math.radians(-40.0), 0.0, math.radians(-125.0))
bpy.context.collection.objects.link(light_rim)

light_accent_data = bpy.data.lights.new('AccentPoint', type='POINT')
light_accent_data.energy = 300.0
light_accent_data.shadow_soft_size = 0.4
light_accent_data.color = (0.9, 0.96, 1.0)
light_accent = bpy.data.objects.new('AccentPoint', light_accent_data)
light_accent.location = (0.0, -3.0, 0.5)
bpy.context.collection.objects.link(light_accent)

light_accent.keyframe_insert(data_path='location', frame=1)
light_accent.location = (2.5, -4.0, 0.8)
light_accent.keyframe_insert(data_path='location', frame=70)
light_accent.location = (0.0, -2.0, 0.4)
light_accent.keyframe_insert(data_path='location', frame=130)
light_accent.location = (0.0, -3.0, 0.2)
light_accent.keyframe_insert(data_path='location', frame=216)

def make_3d_text(name, body, location, size=1.0, extrude=0.09, bevel=0.015, mat=mat_platinum):
    c = bpy.data.curves.new(type='FONT', name=f'{name}_Curve')
    c.body = body
    if outfit_font:
        c.font = outfit_font
    c.extrude = extrude
    c.bevel_depth = bevel
    c.bevel_resolution = 4
    c.align_x = 'CENTER'
    c.align_y = 'CENTER'
    c.size = size
    obj = bpy.data.objects.new(name, c)
    obj.location = location
    obj.rotation_euler = (math.radians(90.0), 0.0, 0.0)
    obj.data.materials.append(mat)
    bpy.context.collection.objects.link(obj)
    return obj

txt_fast = make_3d_text('Txt_FAST', 'FAST.', (0.0, 0.0, 0.0), size=1.5, extrude=0.12, bevel=0.018)
txt_fast.scale = (0.0, 0.0, 0.0)
txt_fast.keyframe_insert(data_path='scale', frame=1)
txt_fast.scale = (1.0, 1.0, 1.0)
txt_fast.keyframe_insert(data_path='scale', frame=10)
txt_fast.location = (0.0, 0.0, 0.0)
txt_fast.keyframe_insert(data_path='location', frame=10)
txt_fast.location = (0.0, 0.3, 0.0)
txt_fast.keyframe_insert(data_path='location', frame=34)
txt_fast.scale = (1.0, 1.0, 1.0)
txt_fast.keyframe_insert(data_path='scale', frame=34)
txt_fast.scale = (0.0, 0.0, 0.0)
txt_fast.keyframe_insert(data_path='scale', frame=40)

txt_private = make_3d_text('Txt_PRIVATE', 'PRIVATE.', (1.4, 0.0, 0.0), size=0.95, extrude=0.09, bevel=0.014)
txt_private.rotation_euler = (math.radians(90.0), math.radians(0.0), math.radians(-12.0))
txt_private.scale = (0.0, 0.0, 0.0)
txt_private.keyframe_insert(data_path='scale', frame=42)
txt_private.scale = (1.0, 1.0, 1.0)
txt_private.keyframe_insert(data_path='scale', frame=52)
txt_private.scale = (1.0, 1.0, 1.0)
txt_private.keyframe_insert(data_path='scale', frame=80)
txt_private.scale = (0.0, 0.0, 0.0)
txt_private.keyframe_insert(data_path='scale', frame=86)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.0, 0.0, 0.0))
ui_slab = bpy.context.view_layer.objects.active
ui_slab.name = 'UI_Slab_Device'
ui_slab.scale = (3.2, 0.1, 2.0)
bpy.ops.object.transform_apply(scale=True)

bm = bmesh.new()
bm.from_mesh(ui_slab.data)
uv_layer = bm.loops.layers.uv.verify()
for f in bm.faces:
    if f.normal.y < -0.9:
        f.material_index = 1
        for loop in f.loops:
            x, y, z = loop.vert.co
            loop[uv_layer].uv = ((x + 1.6) / 3.2, (z + 1.0) / 2.0)
    else:
        f.material_index = 0
bm.to_mesh(ui_slab.data)
bm.free()

ui_slab.data.materials.append(mat_obsidian)
ui_slab.data.materials.append(mat_screen)

mod_c = ui_slab.modifiers.new('Bevel', type='BEVEL')
mod_c.width = 0.08
mod_c.segments = 8

ui_slab.scale = (0.0, 0.0, 0.0)
ui_slab.keyframe_insert(data_path='scale', frame=42)
ui_slab.scale = (1.0, 1.0, 1.0)
ui_slab.keyframe_insert(data_path='scale', frame=52)
ui_slab.rotation_euler = (math.radians(-3.0), math.radians(14.0), math.radians(-1.5))
ui_slab.keyframe_insert(data_path='rotation_euler', frame=52)
ui_slab.rotation_euler = (math.radians(-1.5), math.radians(9.0), math.radians(-0.5))
ui_slab.keyframe_insert(data_path='rotation_euler', frame=80)
ui_slab.scale = (1.0, 1.0, 1.0)
ui_slab.keyframe_insert(data_path='scale', frame=80)
ui_slab.scale = (0.0, 0.0, 0.0)
ui_slab.keyframe_insert(data_path='scale', frame=86)

txt_realtime = make_3d_text('Txt_REALTIME', 'REAL-TIME.', (0.0, 0.0, 0.4), size=1.3, extrude=0.11, bevel=0.016)
txt_realtime.scale = (0.0, 0.0, 0.0)
txt_realtime.keyframe_insert(data_path='scale', frame=88)
txt_realtime.scale = (1.0, 1.0, 1.0)
txt_realtime.keyframe_insert(data_path='scale', frame=98)
txt_realtime.scale = (1.0, 1.0, 1.0)
txt_realtime.keyframe_insert(data_path='scale', frame=122)
txt_realtime.scale = (0.0, 0.0, 0.0)
txt_realtime.keyframe_insert(data_path='scale', frame=128)

c_pulse = bpy.data.curves.new('SoloPulseLine', type='CURVE')
c_pulse.dimensions = '3D'
c_pulse.bevel_depth = 0.045
c_pulse.bevel_resolution = 4
sp = c_pulse.splines.new('POLY')
raw_points = [
    (-8.0, 0.0),
    (-6.0, 0.0),
    (-3.5, 8.0),
    (1.5, -8.0),
    (4.0, 0.0),
    (8.0, 0.0)
]
sp.points.add(len(raw_points) - 1)
scale_p = 0.28
for i, pt in enumerate(raw_points):
    sp.points[i].co = (pt[0] * scale_p, 0.0, pt[1] * scale_p * 0.45, 1.0)

obj_pulse_dynamic = bpy.data.objects.new('PulseWaveDynamic', c_pulse)
obj_pulse_dynamic.location = (0.0, 0.0, -0.4)
obj_pulse_dynamic.rotation_euler = (0.0, 0.0, 0.0)
obj_pulse_dynamic.data.materials.append(mat_pulse_glow)
bpy.context.collection.objects.link(obj_pulse_dynamic)

c_pulse.bevel_factor_end = 0.0
c_pulse.keyframe_insert(data_path='bevel_factor_end', frame=98)
c_pulse.bevel_factor_end = 1.0
c_pulse.keyframe_insert(data_path='bevel_factor_end', frame=122)
obj_pulse_dynamic.scale = (1.0, 1.0, 1.0)
obj_pulse_dynamic.keyframe_insert(data_path='scale', frame=122)
obj_pulse_dynamic.scale = (0.0, 0.0, 0.0)
obj_pulse_dynamic.keyframe_insert(data_path='scale', frame=128)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.8))
badge_cube = bpy.context.view_layer.objects.active
badge_cube.name = 'PulseBadgeContainer'
badge_cube.scale = (2.2, 0.22, 2.2)
bpy.ops.object.transform_apply(scale=True)
mod_badge = badge_cube.modifiers.new('SquircleBevel', type='BEVEL')
mod_badge.width = 0.36
mod_badge.segments = 14
badge_cube.data.materials.append(mat_obsidian)

c_logo = bpy.data.curves.new('LogoPulseCurve', type='CURVE')
c_logo.dimensions = '3D'
c_logo.bevel_depth = 0.04
c_logo.bevel_resolution = 4
sp_logo = c_logo.splines.new('POLY')
sp_logo.points.add(len(raw_points) - 1)
scale_logo = 0.11
for i, pt in enumerate(raw_points):
    sp_logo.points[i].co = (pt[0] * scale_logo, 0.0, pt[1] * scale_logo * 0.48, 1.0)

obj_logo_line = bpy.data.objects.new('LogoPulseLine', c_logo)
obj_logo_line.location = (0.0, -0.12, 0.8)
obj_logo_line.rotation_euler = (0.0, 0.0, 0.0)
obj_logo_line.data.materials.append(mat_pulse_glow)
bpy.context.collection.objects.link(obj_logo_line)

txt_hero_brand = make_3d_text('Txt_PULSE_Hero', 'PULSE', (0.0, 0.0, -0.7), size=1.5, extrude=0.14, bevel=0.02, mat=mat_platinum)
txt_tagline = make_3d_text('Txt_Tagline', 'Fast. Private. Real-Time.', (0.0, 0.0, -1.25), size=0.42, extrude=0.035, bevel=0.007, mat=mat_platinum)

hero_group = [badge_cube, obj_logo_line, txt_hero_brand, txt_tagline]
for o in hero_group:
    o.scale = (0.0, 0.0, 0.0)
    o.keyframe_insert(data_path='scale', frame=128)
    o.scale = (1.0, 1.0, 1.0)
    o.keyframe_insert(data_path='scale', frame=146)

txt_hero_brand.location = (0.0, 0.4, -0.7)
txt_hero_brand.keyframe_insert(data_path='location', frame=128)
txt_hero_brand.location = (0.0, 0.0, -0.7)
txt_hero_brand.keyframe_insert(data_path='location', frame=146)

badge_cube.rotation_euler = (0.0, math.radians(-16.0), 0.0)
badge_cube.keyframe_insert(data_path='rotation_euler', frame=130)
badge_cube.rotation_euler = (0.0, 0.0, 0.0)
badge_cube.keyframe_insert(data_path='rotation_euler', frame=154)
badge_cube.rotation_euler = (0.0, math.radians(2.0), 0.0)
badge_cube.keyframe_insert(data_path='rotation_euler', frame=216)

cam_target.location = (0.0, 0.0, 0.0)
cam_target.keyframe_insert(data_path='location', frame=1)
cam_target.location = (0.0, 0.2, 0.0)
cam_target.keyframe_insert(data_path='location', frame=34)
cam_target.location = (0.0, 0.0, 0.0)
cam_target.keyframe_insert(data_path='location', frame=60)
cam_target.location = (0.0, 0.0, 0.0)
cam_target.keyframe_insert(data_path='location', frame=105)
cam_target.location = (0.0, 0.0, -0.15)
cam_target.keyframe_insert(data_path='location', frame=150)
cam_target.location = (0.0, 0.0, -0.15)
cam_target.keyframe_insert(data_path='location', frame=216)

cam_obj.location = (2.5, -9.2, 0.8)
cam_obj.keyframe_insert(data_path='location', frame=1)
cam_obj.location = (0.4, -8.6, 0.5)
cam_obj.keyframe_insert(data_path='location', frame=34)
cam_obj.location = (-0.6, -8.8, 0.7)
cam_obj.keyframe_insert(data_path='location', frame=60)
cam_obj.location = (-0.3, -8.6, 0.7)
cam_obj.keyframe_insert(data_path='location', frame=84)
cam_obj.location = (0.0, -9.5, 0.6)
cam_obj.keyframe_insert(data_path='location', frame=105)
cam_obj.location = (0.0, -8.8, -0.1)
cam_obj.keyframe_insert(data_path='location', frame=150)
cam_obj.location = (0.0, -8.5, -0.1)
cam_obj.keyframe_insert(data_path='location', frame=216)

output_blend = '/home/akidin/Documents/games and apps/msg app/pulse_promo.blend'
bpy.ops.wm.save_as_mainfile(filepath=output_blend)
print(f'Saved blender project to {output_blend}')
