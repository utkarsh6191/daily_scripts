# Developed by : Utkarsh Agnihotri
# Use : Creates a UI which allows you to switch spaces between body and world
#       while maintaining the position of the control.
# Instruction:
# copy paste script in script editor or open it in script editor
# now you can run the script or create a shelf button
# it works on the selected object
# for chLampchen, it works on Lamp_spline_pole_CTRL and Lamp_head_CTRL


from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import pymel.core as pm


def maya_main_window():
    maya_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class TestDialogue(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialogue, self).__init__(parent)

        self.setWindowTitle("chLampchen01 UI")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.ctrl_name = QtWidgets.QLabel("___Select control for space switching___")
        self.followBody_btn = QtWidgets.QPushButton("Follow Body")
        self.followWorld_btn = QtWidgets.QPushButton("Follow World")
        self.reset_btn = QtWidgets.QPushButton("Reset Control")

    def create_layouts(self):
        # layout for buttons
        box_layout_button = QtWidgets.QVBoxLayout()
        box_layout_button.addStretch()
        box_layout_button.addWidget(self.ctrl_name)
        box_layout_button.addWidget(self.followBody_btn)
        box_layout_button.addWidget(self.followWorld_btn)
        box_layout_button.addWidget(self.reset_btn)

        # arrange layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(box_layout_button)

    def create_connections(self):
        self.followBody_btn.clicked.connect(self.follow_head_to_body)
        self.followWorld_btn.clicked.connect(self.follow_head_to_world)
        self.reset_btn.clicked.connect(self.reset_control)

    def update_force_visibility_translate(self, checked):
        self.translate_cb.setVisible(checked)
        self.translateX_cb.setVisible(checked)
        self.translateY_cb.setVisible(checked)
        self.translateZ_cb.setVisible(checked)

    def update_force_visibility_rotate(self, checked):
        self.rotate_cb.setVisible(checked)
        self.rotateX_cb.setVisible(checked)
        self.rotateY_cb.setVisible(checked)
        self.rotateZ_cb.setVisible(checked)

    def follow_head_to_body(self):
        sel = pm.ls(sl=1)[0]
        ctrl_off = sel + "_matchSpace_OFF"
        ctrl = sel
        pos = pm.xform(ctrl_off, ws=1, t=1, q=1)
        rot = pm.xform(ctrl_off, ws=1, ro=1, q=1)
        pm.setAttr(ctrl + ".followBody", 1)
        pm.setKeyframe(ctrl + ".followBody")
        pm.xform(ctrl_off, ws=1, t=pos)
        pm.xform(ctrl_off, ws=1, ro=rot)

    def follow_head_to_world(self):
        sel = pm.ls(sl=1)[0]
        ctrl_off = sel + "_matchSpace_OFF"
        ctrl = sel
        pos = pm.xform(ctrl_off, ws=1, t=1, q=1)
        rot = pm.xform(ctrl_off, ws=1, ro=1, q=1)
        pm.setAttr(ctrl + ".followBody", 0, k=1)
        pm.setKeyframe(ctrl + ".followBody")
        pm.xform(ctrl_off, ws=1, t=pos)
        pm.xform(ctrl_off, ws=1, ro=rot)

    def reset_control(self):
        sel = pm.ls(sl=1)[0]
        ctrl_off = sel + "_matchSpace_OFF"
        ctrl = sel
        axis = ["x", "y", "z"]
        transform = ["t", "r", "s"]
        ctrl_hi = [ctrl, ctrl_off]

        for c in ctrl_hi:
            for t in transform:
                for a in axis:
                    print a
                    if not pm.getAttr(c + '.' + t + a, lock=1):
                        if t in ["t", "r"]:
                            print("in if %s", a)
                            pm.setAttr(c + '.' + t + a, 0)
                        else:
                            print("in else %s", a)
                            pm.setAttr(c + '.' + t + a, 1)


if __name__ == "__main__":

    try:
        test_dialogue.close()
        test_dialogue.deleteLater()
    except:
        pass
    test_dialogue = TestDialogue()
    test_dialogue.show()
