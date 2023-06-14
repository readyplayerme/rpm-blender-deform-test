from . import ui  # noqa: F401
import bpy


bl_info = {
    "name": "Deform Test",
    "author": "RPM Daniel",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Window > Deform Test",
    "description": "Deform Test",
    "warning": "",
    "wiki_url": "",
    "category": "Animation",
}


class OpenDeformTestWindow(bpy.types.Operator):
    bl_idname = "wm.open_deform_test_window"
    bl_label = "Open Deform Test Window"
    bl_icon = 'CONSOLE'
    widget = None

    def execute(self, context):
        if not self.widget:
            self.widget = ui.TestDeformationWindow()
        self.widget.show()
        
        # RUNNING_MODAL tells blender to keep the operator alive, 
        # so self.widget doesn't get garbage collected
        return {'RUNNING_MODAL'}  


def menu_func(self, context):
    # add a menu item to the blender menu
    self.layout.operator(OpenDeformTestWindow.bl_idname)


def register():
    # run on plugin enable
    bpy.utils.register_class(OpenDeformTestWindow)
    bpy.types.TOPBAR_MT_window.append(menu_func)


def unregister():
    # run on plugin disable
    bpy.utils.unregister_class(OpenDeformTestWindow)
    bpy.types.TOPBAR_MT_window.remove(menu_func)

