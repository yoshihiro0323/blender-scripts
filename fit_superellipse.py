import bpy
import bmesh
import numpy as np
import math
import sys
import site

user_site = "/Users/yourname/.local/lib/python3.11/site-packages"
if user_site not in sys.path:
    site.addsitedir(user_site)

try:
    from scipy.optimize import minimize
except ImportError:
    raise ImportError("SciPy is required. Please install it in Blender's Python environment.")

class OBJECT_OT_FitSuperellipse(bpy.types.Operator):
    """Fit a superellipse to selected vertices in the XY plane."""
    bl_idname = "object.fit_superellipse"
    bl_label = "Fit Superellipse"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object is not a mesh.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in bm.verts if v.select]
        if len(selected_verts) < 3:
            self.report({'ERROR'}, "Select at least 3 vertices.")
            return {'CANCELLED'}

        points = np.array([[v.co.x, v.co.y] for v in selected_verts])
        a0 = np.max(np.abs(points[:, 0]))
        b0 = np.max(np.abs(points[:, 1]))
        n0 = 2.0
        initial_params = [a0, b0, n0]

        def error_func(params):
            a, b, n = params
            if a <= 0 or b <= 0 or n <= 0:
                return 1e6
            diff = (np.abs(points[:, 0] / a) ** n + np.abs(points[:, 1] / b) ** n) - 1
            return np.sum(diff ** 2)

        res = minimize(error_func, initial_params, method='Nelder-Mead')
        a_fit, b_fit, n_fit = res.x
        msg = ("Superellipse Fit Results:\n"
               f"a = {a_fit:.3f}\n"
               f"b = {b_fit:.3f}\n"
               f"n = {n_fit:.3f}")
        self.report({'INFO'}, msg)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_FitSuperellipse.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_FitSuperellipse)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_FitSuperellipse)

if __name__ == "__main__":
    register()
