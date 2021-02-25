from .blender_pydeps import PythonRequirements

import bpy

bl_info = {
    "name": "Facial MoCap v2",
    "description": "Facial Motion Capture",
    "author": "jkirsons, Joe Button",
    "version": (1, 0, 0),
    "blender": (2, 91, 0),
    #"wiki_url": "https://github.com/Joeboy/blender-addon-pydeps",
    #"tracker_url": "https://github.com/Joeboy/blender-addon-pydeps/issues",
    "support": "COMMUNITY",
    "category": "Animation"
}


def check_opencv_contrib_python(module_name):
    import cv2
    if not cv2.version.contrib:
        raise Exception("opencv-contrib-python not installed")


python_requirements = PythonRequirements(
[
    ('wheel', __import__),
    ('opencv-python', lambda module_name: __import__('cv2')),
    ('opencv-contrib-python', check_opencv_contrib_python),
    ('numpy', __import__),
]
)

def register():
    print("Checking requirements...")
    python_requirements.install_requirements()
    from .OpenCVAnim import OBJECT_MT_OpenCVPanel
    from .OpenCVAnimOperator import OpenCVAnimOperator
    bpy.utils.register_class(OpenCVAnimOperator)
    bpy.utils.register_tool(OBJECT_MT_OpenCVPanel, separator=True, group=True)

def unregister():
    from .OpenCVAnim import OBJECT_MT_OpenCVPanel
    from .OpenCVAnimOperator import OpenCVAnimOperator
    bpy.utils.unregister_class(OpenCVAnimOperator)
    bpy.utils.unregister_tool(OBJECT_MT_OpenCVPanel)


if __name__ == "__main__":
    register()
