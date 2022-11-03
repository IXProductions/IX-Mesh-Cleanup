# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Mesh Cleanup",
    "author" : "IX_Productions", 
    "description" : "Cleans and Upscales Your Meshes",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews


addon_keymaps = {}
_icons = None
class SNA_OT_Upscaler_60D4D(bpy.types.Operator):
    bl_idname = "sna.upscaler_60d4d"
    bl_label = "Upscaler"
    bl_description = "Upscale"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        bpy.ops.object.shade_smooth()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.tris_convert_to_quads()
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.select_all()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        bpy.ops.mesh.select_non_manifold()
        bpy.ops.mesh.edges_select_sharp()
        bpy.ops.transform.edge_crease(value=1, snap=False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].levels = 2
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].offset_type = 'PERCENT'
        bpy.context.object.modifiers["Bevel"].width_pct = 26.1274
        bpy.context.object.modifiers["Bevel"].segments = 3
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SNA_PT_IX_MESH_CLEANUP_304F3(bpy.types.Panel):
    bl_label = 'IX Mesh Cleanup'
    bl_idname = 'SNA_PT_IX_MESH_CLEANUP_304F3'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Mesh Cleanup'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.upscaler_60d4d', text='Cleanup Mesh', icon_value=75, emboss=True, depress=False)
        layout.label(text='Will only work on selected objects', icon_value=1)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_OT_Upscaler_60D4D)
    bpy.utils.register_class(SNA_PT_IX_MESH_CLEANUP_304F3)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_OT_Upscaler_60D4D)
    bpy.utils.unregister_class(SNA_PT_IX_MESH_CLEANUP_304F3)
