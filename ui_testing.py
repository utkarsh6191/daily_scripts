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

        self.setWindowTitle("Create constraints")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.matrix_rb = QtWidgets.QRadioButton("matrix")
        self.default_rb = QtWidgets.QRadioButton("default")

        self.prntConst_rb = QtWidgets.QRadioButton("Parent")
        self.prntConst_rb.setIcon(QtGui.QIcon(":parentConstraint.png"))
        self.prntConst_rb.setChecked(True)
        self.translate_cb = QtWidgets.QCheckBox("Translate")
        self.translate_cb.setChecked(True)
        self.translateX_cb = QtWidgets.QCheckBox("X")
        self.translateX_cb.setChecked(True)
        self.translateY_cb = QtWidgets.QCheckBox("Y")
        self.translateY_cb.setChecked(True)
        self.translateZ_cb = QtWidgets.QCheckBox("Z")
        self.translateZ_cb.setChecked(True)
        self.rotate_cb = QtWidgets.QCheckBox("Rotate")
        self.rotate_cb.setChecked(True)
        self.rotateX_cb = QtWidgets.QCheckBox("X")
        self.rotateX_cb.setChecked(True)
        self.rotateY_cb = QtWidgets.QCheckBox("Y")
        self.rotateY_cb.setChecked(True)
        self.rotateZ_cb = QtWidgets.QCheckBox("Z")
        self.rotateZ_cb.setChecked(True)

        self.pntConst_rb = QtWidgets.QRadioButton("Point")
        self.pntConst_rb.setIcon(QtGui.QIcon(":posConstraint.png"))

        self.orntConst_rb = QtWidgets.QRadioButton("Orient")
        self.orntConst_rb.setIcon(QtGui.QIcon(":orientConstraint.png"))

        self.scaleConst_rb = QtWidgets.QRadioButton("Scale")
        self.scaleConst_rb.setIcon(QtGui.QIcon(":scaleConstraint.png"))

        self.maintainOffset_cb = QtWidgets.QCheckBox("maintain offset")
        self.maintainOffset_cb.setChecked(True)
        self.axisX_cb = QtWidgets.QCheckBox("X")
        self.axisX_cb.setChecked(True)
        self.axisY_cb = QtWidgets.QCheckBox("Y")
        self.axisY_cb.setChecked(True)
        self.axisZ_cb = QtWidgets.QCheckBox("Z")
        self.axisZ_cb.setChecked(True)

        self.create_btn = QtWidgets.QPushButton("Create")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):
        # layout for constraint type
        form_layout_const = QtWidgets.QGridLayout()
        form_layout_const.addWidget(self.prntConst_rb, 1, 1)
        form_layout_const.alignment()
        form_layout_const.addWidget(self.pntConst_rb, 1, 2)
        form_layout_const.addWidget(self.orntConst_rb, 2, 1)
        form_layout_const.addWidget(self.scaleConst_rb, 2, 2)

        # layout for constraint method
        box_layout_type = QtWidgets.QHBoxLayout()
        box_layout_type.addWidget(self.default_rb)
        box_layout_type.addWidget(self.matrix_rb)

        # layout for translate checkbox
        box_translate = QtWidgets.QHBoxLayout()
        box_translate.addWidget(self.translate_cb)
        box_translate.addWidget(self.translateX_cb)
        box_translate.addWidget(self.translateY_cb)
        box_translate.addWidget(self.translateZ_cb)

        # layout for rotate checkbox
        box_rotate = QtWidgets.QHBoxLayout()
        box_rotate.addWidget(self.rotate_cb)
        box_rotate.addWidget(self.rotateX_cb)
        box_rotate.addWidget(self.rotateY_cb)
        box_rotate.addWidget(self.rotateZ_cb)

        # layout for constraint method
        box_layout_axis = QtWidgets.QHBoxLayout()
        box_layout_axis.addWidget(self.axisX_cb)
        box_layout_axis.addWidget(self.axisY_cb)
        box_layout_axis.addWidget(self.axisZ_cb)

        # layout for buttons
        box_layout_button = QtWidgets.QHBoxLayout()
        box_layout_button.addStretch()
        box_layout_button.addWidget(self.maintainOffset_cb)
        box_layout_button.addWidget(self.create_btn)
        box_layout_button.addWidget(self.cancel_btn)

        # arrange layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout_const)
        main_layout.addLayout(box_translate)
        main_layout.addLayout(box_rotate)
        main_layout.addLayout(box_layout_axis)
        main_layout.addLayout(box_layout_type)
        main_layout.addLayout(box_layout_button)

    def create_connections(self):
        self.prntConst_rb.toggled.connect(self.update_force_visibility_translate)
        self.prntConst_rb.toggled.connect(self.update_force_visibility_rotate)
        self.cancel_btn.clicked.connect(self.close)
        self.create_btn.clicked.connect(self.create_constraint)

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

    def create_constraint(self):

        sel = pm.ls(sl=1)
        source = sel[0]
        target = sel[1]

        if self.prntConst_rb.isChecked():
            skipped_axes_translate, skipped_axes_rotate = self.check_parentConstraint_axes()

            self.create_parent_constraint(source, target, skipped_axes_translate, skipped_axes_rotate)
        elif self.pntConst_rb.isChecked():
            skipped_axes = self.check_axes()
            self.create_point_constraint(source, target, skipped_axes)
        elif self.orntConst_rb.isChecked():
            skipped_axes = self.check_axes()
            self.create_orient_constraint(source, target, skipped_axes)
        else:
            skipped_axes = self.check_axes()
            self.create_scale_constraint(source, target, skipped_axes)

    def check_axes(self):
        axes_type = ["x", "y", "z"]
        skipped_axes = []

        if self.axisX_cb.isChecked():
            # skips yz
            skipped_axes = [e for e in axes_type if e not in 'x']
            print(skipped_axes)

        if self.axisY_cb.isChecked():
            # skips xz
            skipped_axes = [e for e in axes_type if e not in 'y']
            print(skipped_axes)

        if self.axisZ_cb.isChecked():
            # skips xy
            skipped_axes = [e for e in axes_type if e not in 'z']
            print(skipped_axes)

        if self.axisX_cb.isChecked() and self.axisY_cb.isChecked():
            # skips z
            skipped_axes = [e for e in axes_type if e not in ('x', 'y')]
            print(skipped_axes)
        if self.axisY_cb.isChecked() and self.axisZ_cb.isChecked():
            # skips x
            skipped_axes = [e for e in axes_type if e not in ('y', 'z')]
            print(skipped_axes)
        if self.axisZ_cb.isChecked() and self.axisX_cb.isChecked():
            # skips y
            skipped_axes = [e for e in axes_type if e not in ('x', 'z')]
            print(skipped_axes)

        if self.axisX_cb.isChecked() and self.axisY_cb.isChecked() and self.axisZ_cb.isChecked():
            # skips y
            skipped_axes = "none"
            print(skipped_axes)
        return skipped_axes

    def check_parentConstraint_axes(self):

        axes_type = ["x", "y", "z"]
        skipped_axes = []
        skipped_axes_translate = []
        skipped_axes_rotate = []

        if self.translate_cb.isChecked():
            if self.translateX_cb.isChecked():
                # skips yz
                skipped_axes_translate = [e for e in axes_type if e not in 'x']
                print(skipped_axes_translate)

            if self.translateY_cb.isChecked():
                # skips xz
                skipped_axes_translate = [e for e in axes_type if e not in 'y']
                print(skipped_axes_translate)

            if self.translateZ_cb.isChecked():
                # skips xy
                skipped_axes_translate = [e for e in axes_type if e not in 'z']
                print(skipped_axes_translate)

            if self.translateX_cb.isChecked() and self.translateY_cb.isChecked():
                # skips z
                skipped_axes_translate = [e for e in axes_type if e not in ('x', 'y')]
                print(skipped_axes_translate)
            if self.translateY_cb.isChecked() and self.translateZ_cb.isChecked():
                # skips x
                skipped_axes_translate = [e for e in axes_type if e not in ('y', 'z')]
                print(skipped_axes_translate)
            if self.translateZ_cb.isChecked() and self.translateX_cb.isChecked():
                # skips y
                skipped_axes_translate = [e for e in axes_type if e not in ('x', 'z')]
                print(skipped_axes_translate)

            if self.translateX_cb.isChecked() and self.translateY_cb.isChecked() and self.translateZ_cb.isChecked():
                # skips y
                skipped_axes_translate = "none"
                print(skipped_axes_translate)
        else:
            skipped_axes_translate = axes_type
        if self.rotate_cb.isChecked():
            if self.translateX_cb.isChecked():
                # skips yz
                skipped_axes_rotate = [e for e in axes_type if e not in 'x']
                print(skipped_axes_rotate)

            if self.translateY_cb.isChecked():
                # skips xz
                skipped_axes_rotate = [e for e in axes_type if e not in 'y']
                print(skipped_axes_rotate)

            if self.translateZ_cb.isChecked():
                # skips xy
                skipped_axes_rotate = [e for e in axes_type if e not in 'z']
                print(skipped_axes_rotate)

            if self.translateX_cb.isChecked() and self.translateY_cb.isChecked():
                # skips z
                skipped_axes_rotate = [e for e in axes_type if e not in ('x', 'y')]
                print(skipped_axes_rotate)
            if self.translateY_cb.isChecked() and self.translateZ_cb.isChecked():
                # skips x
                skipped_axes_rotate = [e for e in axes_type if e not in ('y', 'z')]
                print(skipped_axes_rotate)
            if self.translateZ_cb.isChecked() and self.translateX_cb.isChecked():
                # skips y
                skipped_axes_rotate = [e for e in axes_type if e not in ('x', 'z')]
                print(skipped_axes_rotate)

            if self.translateX_cb.isChecked() and self.translateY_cb.isChecked() and self.translateZ_cb.isChecked():
                # skips y
                skipped_axes_rotate = "none"
                print(skipped_axes_rotate)
        else:
            skipped_axes_rotate = axes_type

        return skipped_axes_translate, skipped_axes_rotate

    def create_parent_constraint(self, source, target, skipped_axes_translate, skipped_axes_rotate):
        if self.maintainOffset_cb.isChecked():

            pm.parentConstraint(source, target, st=skipped_axes_translate, sr=skipped_axes_rotate, mo=1)
        else:
            pm.parentConstraint(source, target, st=skipped_axes_translate, sr=skipped_axes_rotate, mo=0)

    def create_point_constraint(self, source, target, skipped_axes):
        if self.maintainOffset_cb.isChecked():
            pm.pointConstraint(source, target, sk=skipped_axes, mo=1)
        else:
            pm.pointConstraint(source, target, sk=skipped_axes, mo=0)

    def create_orient_constraint(self, source, target, skipped_axes):
        if self.maintainOffset_cb.isChecked():
            pm.orientConstraint(source, target, sk=skipped_axes, mo=1)
        else:
            pm.orientConstraint(source, target, sk=skipped_axes, mo=0)

    def create_scale_constraint(self, source, target, skipped_axes):
        if self.maintainOffset_cb.isChecked():
            pm.scaleConstraint(source, target, sk=skipped_axes, mo=1)
        else:
            pm.scaleConstraint(source, target, sk=skipped_axes, mo=0)


if __name__ == "__main__":

    try:
        test_dialogue.close()
        test_dialogue.deleteLater()
    except:
        pass
    test_dialogue = TestDialogue()
    test_dialogue.show()
