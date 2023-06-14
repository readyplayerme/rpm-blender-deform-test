"""A Blender add-on creates a PySide2 window with a label, slider, and button.

The label explains slider functionality, the slider sets its value between
current scene's start/end frames. The button loads an animation, links it to
the scene's Armature and adds it to NLA track. Slider signal updates current
Blender frame, timer updates slider value. The window is set to always be on
top and a tool window.
"""

import webbrowser

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QTimer
from ready_player_me import animation_handler


def popup_window(message):
    """Pop-up a window which waits for the user input. OK button by default."""
    msg = QtWidgets.QMessageBox()
    msg.setText(message)
    msg.exec_()


class TestDeformationWindow(QtWidgets.QWidget):
    """Main window which loads an animation and have the animation slider."""

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        # Save pose mode when we open the window so we can restore it when we close it.
        self.pose = animation_handler.get_pose_position()

        self.anim_info = QtWidgets.QLabel("Controls current frame.")
        self.playback_info = QtWidgets.QLabel("Controls animation playback speed.")
        self.animation_keyframes = QtWidgets.QSlider(Qt.Horizontal)  # Slider Widget
        self.playback_speed = QtWidgets.QSlider(Qt.Horizontal)  # Slider Widget
        self.x_ray = QtWidgets.QCheckBox("Enable Armature Xray", self)  # Check box
        self.animation_list = QtWidgets.QListWidget()  # List
        self.setLayout(QtWidgets.QVBoxLayout())

        # Adding documentation
        self.docs_button = QtWidgets.QPushButton("Documentation")
        self.import_animations = QtWidgets.QPushButton("Import animation")
        doc_url = "https://www.notion.so/wolf3d/Deformation-Test-Tool-6f27bf8f69724289932359a9261b58b1?pvs=4"
        self.docs_button.clicked.connect(lambda: webbrowser.open(doc_url, new=1, autoraise=True))
        self.import_animations.clicked.connect(self.import_anims)

        # Bringing in the default animations into a list.
        animations = animation_handler.get_animations_name()
        if animations is not None:
            for animation in animations:
                self.animation_list.addItem(animation.name)

        # Setting up the Animation multiplier min and max value.
        self.playback_speed.setMinimum(2)
        self.playback_speed.setSliderPosition(24)
        self.playback_speed.setMaximum(60)

        # Adding the documentation button
        self.layout().addWidget(self.docs_button)

        # Adding the import animation button
        self.layout().addWidget(self.import_animations)

        # Spawning the list with the animations.
        self.layout().addWidget(self.animation_list)

        # Spawning the slider for animation playback keyframe control.
        self.layout().addWidget(self.anim_info)
        self.layout().addWidget(self.animation_keyframes)

        # Spawning slider for animation playback speed control.
        self.layout().addWidget(self.playback_info)
        self.layout().addWidget(self.playback_speed)

        # Creating a check box to enable X-Ray view for the bones
        self.layout().addWidget(self.x_ray)

        # Adding a timer for the tick sync between slider and animation index
        self.timer = QTimer()

        # Update the silder if the current frame updates.
        self.timer.timeout.connect(self.on_update)

        # When the widget appears for the first time it doesn't have anything selected so we force the 1st entry.
        current_item = self.animation_list.currentItem()
        if current_item is None:
            try:
                animation_handler.link_animation(animations[0].name)
            except TypeError:
                popup_window("Could not load the default animation file.")

            # After a animation is loaded we resize the playback range and slider in the active range
            self.resize_slider()
            self.resize_animation()

        # Adding speed control for the animation to the slider.
        self.playback_speed.valueChanged.connect(self.change_speed)

        # Sync the x_ray with the value in blender
        self.x_ray.stateChanged.connect(self.toggle)

        # Sync the slider with the current frame.
        self.animation_keyframes.valueChanged.connect(self.slider_changed)

        # Link animation on select and resize the slider and teh playback range.
        self.animation_list.itemSelectionChanged.connect(self.link_animation)
        self.animation_list.itemSelectionChanged.connect(self.resize_slider)
        self.animation_list.itemSelectionChanged.connect(self.resize_animation)

    # Overwriting the close events so it does something when it closes.
    def closeEvent(self, event):
        """Overwrite the close events to clean up the scene.

        - clears linked animation.
        - remove animations from the file
        - reset Armature pose
        - stops playback
        - remove the bone see through
        """
        # Clean up animation data.
        animation_handler.stop_playback()
        animation_handler.clear_animation()
        animation_handler.remove_animations()
        animation_handler.reset_pose()
        animation_handler.set_x_view(False)
        animation_handler.set_pose_position(self.pose)

        # proceed with window closing.
        event.accept()

    def import_anims(self):
        """Import all the animations from a .blend file."""
        file_path = QtWidgets.QFileDialog.getOpenFileName(None, "Select File")
        animations = animation_handler.get_animations_name(file_path[0])
        if animations is not None:
            for animation in animations:
                self.animation_list.addItem(animation.name)

    def resize_animation(self):
        """Resize the playable animation so it becomes loopable."""
        start, end = animation_handler.get_anim_framerange_from_blender()
        animation_handler.set_playback_range(start, end)

    def resize_slider(self):
        """Grab the last keyframe to normalize the slider.

        Requires a loaded Action.
        """
        # It happens when the animation has a speed multiplier applied.
        start, end = animation_handler.get_anim_framerange_from_blender()
        self.animation_keyframes.setMinimum(start)
        self.animation_keyframes.setMaximum(end)

    def link_animation(self):
        """Link the selected animation to the Armature."""
        # Debug line
        print("Selected items: ", self.animation_list.currentItem().text())
        animation = self.animation_list.currentItem().text()
        animation_handler.link_animation(animation)

    def toggle(self, state):
        """Sync/change the  Xray view."""
        if state == Qt.Checked:
            animation_handler.set_x_view(True)
            print("Checked")
        else:
            animation_handler.set_x_view(False)
            print("Unchecked")

    def show(self):
        """Tick every 33ms to update the slider from the animation."""
        super().show()
        tick = 1000 // 30
        self.timer.start(tick)

    def on_update(self):
        """Set slider to current frame from blender."""
        index = animation_handler.get_frame_index()
        self.animation_keyframes.setValue(index)

    def slider_changed(self, value):
        """Change the keyframes with the slider."""
        try:
            animation_handler.set_frame_index(value)
        except Exception:
            popup_window("Could not sync Slider with animation.")

        # TODO Get the vizualizer done

    def change_speed(self, value):
        """Change the playback rate of the animation."""
        animation_handler.set_playback_speed(value)


def show():
    main_window = QtWidgets.QApplication.instance().blender_widget
    widget = TestDeformationWindow(parent=main_window, f=Qt.Tool)
    widget.show()
