# blender-deform-test
![rundeformtool](https://github.com/readyplayerme/blender-deform-test/assets/104501614/9cda11be-eccf-442a-9144-380e180017ce)

This tool can be used to test animations on skinned avatars in Blender.

For more info see the [Deformation Test Tool documentation](https://www.notion.so/wolf3d/Deformation-Test-Tool-6f27bf8f69724289932359a9261b58b1)

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
python -m pip install git+https://github.com/readyplayerme/blender-deform-test
