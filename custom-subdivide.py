bl_info = {
    "name": "Custom Subdivide a:b with Optional Grid Fill (EN)",
    "author": "KomiyaJapan",
    "version": (1, 3),
    "blender": (4, 3, 2),
    "location": "Right-click menu (Edit Mode)",
    "description": "Subdivide selected edges at an a:b ratio, with optional creation of internal grid edges",
    "category": "Mesh",
}

import bpy
import bmesh
from bpy.props import FloatProperty, BoolProperty

class MESH_OT_custom_subdivide_ab(bpy.types.Operator):
    """Subdivide selected edges at an a:b ratio, with optional internal edge creation"""
    bl_idname = "mesh.custom_subdivide_ab"
    bl_label = "Custom Subdivide (a:b) with Optional Grid Fill"
    bl_options = {'REGISTER', 'UNDO'}
    
    ratio_a: FloatProperty(
        name="A",
        description="Value for ratio A",
        default=1.0,
        min=0.0,
    )
    
    ratio_b: FloatProperty(
        name="B",
        description="Value for ratio B",
        default=1.0,
        min=0.0,
    )
    
    use_grid_fill: BoolProperty(
        name="Create Internal Edges",
        description="Enable to create internal grid edges",
        default=True,
    )
    
    # Example: additional parameter (currently unused)
    smooth: FloatProperty(
        name="Smooth",
        description="Smoothing amount during subdivision (currently unused)",
        default=0.0,
        min=0.0,
        max=1.0,
    )
    
    def execute(self, context):
        # Prevent division by zero
        if self.ratio_a + self.ratio_b == 0:
            self.report({'WARNING'}, "The sum of A and B must be non-zero")
            return {'CANCELLED'}
        
        # Calculate the effective ratio
        effective_ratio = self.ratio_a / (self.ratio_a + self.ratio_b)
        
        obj = context.edit_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "You must be in edit mode on a mesh object")
            return {'CANCELLED'}
        
        bm = bmesh.from_edit_mesh(obj.data)
        # Only process selected edges
        edges = [e for e in bm.edges if e.select]
        if not edges:
            self.report({'WARNING'}, "No selected edges found")
            return {'CANCELLED'}
        
        # Apply subdivision on each selected edge using the calculated ratio
        edge_percents = {e: effective_ratio for e in edges}
        bmesh.ops.subdivide_edges(
            bm,
            edges=edges,
            cuts=1,
            edge_percents=edge_percents,
            use_grid_fill=self.use_grid_fill,
        )
        
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Subdivision Ratio (A:B)")
        col.prop(self, "ratio_a")
        col.prop(self, "ratio_b")
        layout.prop(self, "use_grid_fill")
        # Uncomment if additional parameters are needed
        # layout.prop(self, "smooth")

def menu_func(self, context):
    self.layout.operator(MESH_OT_custom_subdivide_ab.bl_idname, text="Custom Subdivide (a:b) with Optional Grid Fill")

def register():
    bpy.utils.register_class(MESH_OT_custom_subdivide_ab)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_custom_subdivide_ab)

if __name__ == "__main__":
    register()
