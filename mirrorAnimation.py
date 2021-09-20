import maya.OpenMaya as om
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import pymel.core as pm
import maya.mel as mel


def maya_main_window():
    maya_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class MirrorAnimation(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(MirrorAnimation, self).__init__(parent)

        self.setWindowTitle("Mirror Animation")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.heading_lbl = QtWidgets.QLabel("Select Controls")
        self.mirror_animation_btn = QtWidgets.QPushButton("Mirror Animation")
        self.mirror_animation_on_selection_btn = QtWidgets.QPushButton("Mirror Selected Range")
        self.flip_pose_btn = QtWidgets.QPushButton("Flip Pose")
        self.mirror_pose_btn = QtWidgets.QPushButton("Mirror Pose")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):

        # layout for buttons
        box_layout_button = QtWidgets.QVBoxLayout()
        box_layout_button.addWidget(self.heading_lbl)
        box_layout_button.addWidget(self.flip_pose_btn)
        box_layout_button.addWidget(self.mirror_pose_btn)
        box_layout_button.addWidget(self.mirror_animation_btn)
        box_layout_button.addWidget(self.mirror_animation_on_selection_btn)
        box_layout_button.addWidget(self.cancel_btn)

        # arrange layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(box_layout_button)

    def create_connections(self):
        self.cancel_btn.clicked.connect(self.close)
        self.mirror_animation_btn.clicked.connect(self.mirror_animation)
        self.mirror_animation_on_selection_btn.clicked.connect(self.mirror_on_selectedRange)
        self.flip_pose_btn.clicked.connect(self.flip_pose)
        self.mirror_pose_btn.clicked.connect(self.mirror_pose)


    def flip_name(self, source):
        """@brief method to flip name.

        finds the side in the name replaces them, L to R and R to L.

        @param source: name of the control (string)
        :return: flipped name (string)
        """
        # split object into components to find the side
        self.object_component = source.split('_')

        # if side is L, replace with R
        if self.object_component[-3] == 'L':
            self.flipped_name = source.replace("_L_", "_R_")
            print("left side found")
            return self.flipped_name

        # if side is R, replace with L
        if self.object_component[-3] == 'R':
            print("right side found")
            self.flipped_name = source.replace("_R_", "_L_")
            return self.flipped_name

    def mirror_animation(self):
        """@brief mirror animation on opposite side of the axis
        """
        sel = pm.ls(sl=1)
        # get time slider range of the scene
        min_timeRange = pm.playbackOptions(q=1, min=1)
        max_timeRange = pm.playbackOptions(q=1, max=1)
        # mirror animation using scale
        pm.scaleKey(str(sel[0]), at=['tx', 'ty', 'tz'], valueScale=-1)

        # copy keys on flipped side
        for s in sel:
            if pm.keyframe(s, q=1, tc=1):
                pm.copyKey(s, time=(min_timeRange, max_timeRange), hierarchy="none", controlPoints=0, shape=1)
                flipped_ctrl = self.flip_name(str(s))
                print flipped_ctrl
                if pm.objExists(flipped_ctrl):
                    pm.pasteKey(flipped_ctrl, option="replace",
                                time=(min_timeRange, max_timeRange), f=(min_timeRange, max_timeRange), copies=1,
                                connect=0)
            else:
                om.MGlobal.displayError("Key doesn't exists on the selection")

    def set_attribute(self, target, trans, rot):

        pm.setAttr("{}.{}".format(target, "rotateX"), self.rot[0])
        pm.setAttr("{}.{}".format(target, "rotateY"), self.rot[1])
        pm.setAttr("{}.{}".format(target, "rotateZ"), self.rot[2])
        pm.setAttr("{}.{}".format(target, "translateX"), self.tran[0])
        pm.setAttr("{}.{}".format(target, "translateY"), self.tran[1])
        pm.setAttr("{}.{}".format(target, "translateZ"), self.tran[2])

    def mirror_pose(self):
        sel = pm.ls(sl=1)
        for s in sel:
            flipped_ctrl = self.flip_name(str(s))
            self.rot = pm.getAttr("{}.{}".format(s, "rotate"))
            self.tran = pm.getAttr("{}.{}".format(s, "translate"))

            self.set_attribute(flipped_ctrl, [self.tran[0], self.tran[1], self.tran[2]],
                               [self.rot[0], self.rot[0], self.rot[0]])

    def flip_pose(self):
        sel = pm.ls(sl=1)
        for s in sel:
            self.rot = pm.getAttr("{}.{}".format(s, "rotate"))
            self.tran = pm.getAttr("{}.{}".format(s, "translate"))

            self.rot[0] *= -1
            self.rot[1] *= -1
            self.rot[2] *= -1
            self.tran[0] *= -1
            self.tran[1] *= -1
            self.tran[2] *= -1
            self.set_attribute(s, [self.tran[0], self.tran[1], self.tran[2]],
                               [self.rot[0], self.rot[0], self.rot[0]])
    def mirror_on_selectedRange(self):

        aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
        timeRange = pm.timeControl(aTimeSlider, q=True, rangeArray=True)
        min_timeRange = timeRange[0]
        max_timeRange = timeRange[1]
        sel = pm.ls(sl=1)

        # mirror animation using scale
        pm.scaleKey(str(sel[0]), at=['tx', 'ty', 'tz'], valueScale=-1)

        # copy keys on flipped side
        for s in sel:
            if pm.keyframe(s, q=1, tc=1):
                pm.copyKey(s, time=(min_timeRange, max_timeRange), hierarchy="none", controlPoints=0, shape=1)
                flipped_ctrl = self.flip_name(str(s))
                print flipped_ctrl
                if pm.objExists(flipped_ctrl):
                    pm.pasteKey(flipped_ctrl, option="replace",
                                time=(min_timeRange, max_timeRange), f=(min_timeRange, max_timeRange), copies=1,
                                connect=0)
            else:
                om.MGlobal.displayError("Key doesn't exists on the selection")
        print timeRange


if __name__ == "__main__":

    try:
        test_dialogue.close()
        test_dialogue.deleteLater()
    except:
        pass
    test_dialogue = MirrorAnimation()
    test_dialogue.show()
