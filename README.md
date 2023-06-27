# Blender deform test
![rundeformtool](https://github.com/readyplayerme/blender-deform-test/assets/104501614/9cda11be-eccf-442a-9144-380e180017ce)

This tool can be used to test animations on skinned avatars in Blender.

## Install
This repo can be installed either as a Blender add-on, or through PIP. 

#### Blender add-on (recommended)
Installing as a Blender add-on
- gives the option to disable this tool
- adds a menu button to launch the window

Instructions:
- download latest
- install as a blender add-on, by extracting the whole folder in your blender addons folder
- enable the add-on in blender
- PIP install the dependencies from `requirements.txt`

#### PIP
Installing through PIP
- installs the tool as a Python module
- no option to disable, which means it won't accidentally be disabled
- auto installs the dependencies
- no menu button, but can be launched from the python console

Instructions:
- PIP install the module from github
```
python -m pip install git+https://github.com/readyplayerme/rpm-blender-deform-test
```
## How to use

### Open the tool
<img src="https://github.com/readyplayerme/rpm-blender-deform-test/assets/116070285/d02bd477-d42a-49d5-a089-c7114b668bc3" height="400" />

1. Click 'Window' menu button on topbar
2. Click 'Deformation-Test-Window' button to open the tool

### Use the tool

|  |  |
| ------ | ------------- |
| <img src="https://github.com/readyplayerme/rpm-blender-deform-test/assets/116070285/afa6c18b-3758-48a3-9fc4-13ad04c368dd" height="600" /> | 1. Open this documentation<br>2. Import animations from a .BLEND file<br>3. Select an animation to play<br>4. Slider to move through the animation<br>5. Slider to control animation playback speed<br>6. Enable Skeleton see-through (X-Ray) |


You can play the animation by pressing the play button in the timeline view or pressing spacebar (Blender's default shortcut)
