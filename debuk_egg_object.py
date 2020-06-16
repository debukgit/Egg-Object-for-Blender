
bl_info = {
    "name": "Egg Object",
    "description": "Creates an Egg",
    "author": "Debuk",
    "version": (1, 2, 0),
    'license': 'GPL v3',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Object"
}

import bpy, math, bmesh

from mathutils import Vector
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty
)
import random

cracksWidth = 0.1

def generate_Egg(radialScale, height, ringFaces, heightFaces):

    verts = []
    edges = []
    faces = []

    heightFElements= heightFaces
    radialFElements = ringFaces

    for j in range(heightFElements+1):
        for i in range(radialFElements):
            u = (2 * math.pi) * (i / (radialFElements))
            v = (math.pi) * (j / (heightFElements))
            x = ((radialScale * 0.52 ) + 0.2 * v) * math.cos(u) * math.sin(v) * height * 0.5
            y = ((radialScale * 0.52 ) + 0.2 * v) * math.sin(u) * math.sin(v) * height * 0.5
            z = height * 0.5 * math.cos(v)
            verts.append(Vector((x , y , z)))
    for j in range(heightFElements):
        for i in range( radialFElements):
            a = i % radialFElements
            b = (i + 1)  % radialFElements
            r1 = radialFElements*j
            r2 = radialFElements*(j+1)
            faces.append([r1 + a, r2 + a, r2 + b, r1 + b])
    return verts, edges, faces


def generate_Egg_Headed(radialScale, height, ringFaces, heightFaces, headedStart):

    verts = []
    edges = []
    faces = []

    heightFElements= heightFaces
    radialFElements = ringFaces



    for j in range(heightFElements+1):
        for i in range(radialFElements):

            u = (2 * math.pi) * (i / (radialFElements))
            v = (headedStart* math.pi) + ((math.pi) * (j / (heightFElements)) * (1-headedStart))
            if j==0:
                v -= random.random() * (cracksWidth)
            x = ((radialScale * 0.52 ) + 0.2 * v) * math.cos(u) * math.sin(v) * height * 0.5
            y = ((radialScale * 0.52 ) + 0.2 * v) * math.sin(u) * math.sin(v) * height * 0.5
            z = height * 0.5 * math.cos(v)
            verts.append(Vector((x , y , z)))
    for j in range(heightFElements):
        for i in range( radialFElements):
            a = i % radialFElements
            b = (i + 1)  % radialFElements
            r1 = radialFElements*j
            r2 = radialFElements*(j+1)
            faces.append([r1 + a, r2 + a, r2 + b, r1 + b])
    return verts, edges, faces


class Add_Egg_Menu(bpy.types.Menu):
    bl_label = "Essentials"
    bl_idname = "OBJECT_MT_Add_Egg_Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.add_egg")


class Add_Egg(bpy.types.Operator):
    """Create Egg"""
    bl_idname = "mesh.add_egg"
    bl_label = "Egg"
    bl_options = {'UNDO', 'REGISTER'}

    ringFaces: IntProperty(
        name="RingFaces",
        description="RingFaces of the Egg",
        default=16,
        min=4,
        soft_min=4,
        soft_max=300,
        step=1
    )

    heightFaces: IntProperty(
        name="HeightFaces ",
        description="HeightFaces of the Egg",
        default=20,
        min = 4,
        soft_min=4,
        soft_max=300,
        step=1
    )

    height: FloatProperty(
        name = "Height ",
        description = "Height of the Egg",
        default = 1.0,
        min = 0.01,
        soft_min = 0.01,
        step = 1
    )

    radialScale: FloatProperty(
        name = "RadialScale",
        description = "RadialScale of the Egg",
        default = 1.0,
        min = 0.01,
        soft_min = 0.01,
        step = 1
    )

    shadeSmooth: BoolProperty(
        name="Shade Smooth",
        description="",
        default=True,
    )

    optimizePoles: BoolProperty(
        name="Optimize Poles",
        description="",
        default=True,
    )

    isCracked: BoolProperty(
        name="Cracked",
        description="",
        default=False,
    )

    hasThickness: BoolProperty(
        name="Thickness",
        description="",
        default=False,
    )

    headedStart: FloatProperty(
        name = " Headed Start ",
        description = "Percentage of the egg being headed",
        default = cracksWidth,
        min = cracksWidth,
        soft_min = cracksWidth,
        max=1.0,
        soft_max=1.0,
        step = 0.1
    )

    def draw(self, context):
        layout = self.layout

        faceBox = layout.box()
        faceBox.label(text = "Faces")
        faceBox.prop(context.object, "headedStart")
        faceBox.prop(self, "ringFaces")
        faceBox.prop(self, "heightFaces")
        faceBox.prop(self, "optimizePoles")
        faceBox.prop(self, "shadeSmooth")

        sizebox = layout.box()
        sizebox.label(text = "Size")
        sizebox.prop(self, "height")
        sizebox.prop(self, "radialScale")

        breakbox = layout.box()
        breakbox.label(text = "Break the egg")
        breakbox.prop(self, "isCracked")
        col = breakbox.box()
        col.prop(self, "hasThickness")
        col.prop(self, "headedStart")

        if self.isCracked:
            col.enabled = True
        else:
            col.enabled = False
            self.hasThickness = False

    def execute(self, context):


        if self.isCracked:
            verts, edges, faces = generate_Egg_Headed(
                radialScale=self.radialScale,
                height=self.height,
                ringFaces=self.ringFaces,
                heightFaces=self.heightFaces,
                headedStart= self.headedStart
            )
        else:
            verts, edges, faces = generate_Egg(
                radialScale=self.radialScale,
                height=self.height,
                ringFaces=self.ringFaces,
                heightFaces=self.heightFaces,
            )
        mesh = bpy.data.meshes.new("Egg")
        mesh.from_pydata(verts, edges, faces)
        if self.shadeSmooth:
            for f in mesh.polygons:
                f.use_smooth = True

        # Normal calculation
        self.calcNormals(mesh)
        # Uvs
        self.generate_UVs(
            mesh,
            ringFaces=self.ringFaces,
            heightFaces=self.heightFaces
        )

        mesh.update()

        eggObj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(eggObj)
        bpy.context.view_layer.objects.active = eggObj

        bpy.ops.object.mode_set(mode='EDIT')
        if self.optimizePoles:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')

        if self.isCracked and self.hasThickness:
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.data.use_auto_smooth = True

        return {'FINISHED'}

    def generate_UVs(self, mesh, ringFaces,heightFaces):

        uvlayer = mesh.uv_layers.new()
        mesh.uv_layers.active = uvlayer

        for face in mesh.polygons:
            for idx, (vert_idx, loop_idx) in enumerate(zip(face.vertices, face.loop_indices)):
                x = vert_idx % (ringFaces)
                y = vert_idx // (ringFaces)
                if (x==0) and (idx > 1):
                    x=ringFaces
                uvlayer.data[loop_idx].uv = (x / (ringFaces)  , 1.0 - (y /(heightFaces)))

    def calcNormals(self, mesh):
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.clear()
        mesh.update()
        bm.free()


def egg_menu(self, context):
    lay_out = self.layout
    lay_out.menu(Add_Egg_Menu.bl_idname)

def register():
    bpy.types.VIEW3D_MT_mesh_add.append(egg_menu)
    bpy.utils.register_class(Add_Egg_Menu)
    bpy.utils.register_class(Add_Egg)


def unregister():
    bpy.utils.unregister_class(Add_Egg_Menu)
    bpy.utils.unregister_class(Add_Egg)
    bpy.types.VIEW3D_MT_mesh_add.remove(egg_menu)


