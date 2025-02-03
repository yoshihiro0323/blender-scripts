import bpy
import math
from bpy.props import FloatProperty, IntProperty

class MESH_OT_add_superellipse(bpy.types.Operator):
    bl_idname = "mesh.add_superellipse"
    bl_label = "Add SuperEllipse"
    bl_options = {'REGISTER', 'UNDO'}

    a: FloatProperty(
        name="a",
        description="Radius in x-direction",
        default=1.0,
        min=0.0,
        unit='LENGTH'
    )
    b: FloatProperty(
        name="b",
        description="Radius in y-direction",
        default=1.0,
        min=0.0,
        unit='LENGTH'
    )
    n: FloatProperty(
        name="n",
        description="Exponent controlling the shape (2 for ellipse, higher for squarer shape)",
        default=2.0,
        min=0.1
    )
    segments: IntProperty(
        name="Segments",
        description="Number of vertices",
        default=32,
        min=4
    )

    def execute(self, context):
        verts = []
        for i in range(self.segments):
            theta = (2 * math.pi * i) / self.segments
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
            x = self.a * (abs(cos_theta) ** (2 / self.n)) * (1 if cos_theta >= 0 else -1)
            y = self.b * (abs(sin_theta) ** (2 / self.n)) * (1 if sin_theta >= 0 else -1)
            verts.append((x, y, 0))
        faces = [list(range(self.segments))]
        mesh = bpy.data.meshes.new("SuperEllipse")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        obj = bpy.data.objects.new("SuperEllipse", mesh)
        context.collection.objects.link(obj)
        context.view_layer.objects.active = obj
        obj.select_set(True)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MESH_OT_add_superellipse.bl_idname, text="SuperEllipse", icon='MESH_CIRCLE')

def register():
    bpy.utils.register_class(MESH_OT_add_superellipse)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_add_superellipse)

if __name__ == "__main__":
    register()
