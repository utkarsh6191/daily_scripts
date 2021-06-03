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
        self.prntConst_rb.setChecked(True)
        self.rotate_cb = QtWidgets.QCheckBox("Rotate")
        self.prntConst_rb.setChecked(True)

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
        form_layout_const.addWidget(self.pntConst_rb, 1, 2)
        form_layout_const.addWidget(self.orntConst_rb, 2, 1)
        form_layout_const.addWidget(self.scaleConst_rb, 2, 2)

        # layout for constraint method
        box_layout_type = QtWidgets.QHBoxLayout()
        box_layout_type.addWidget(self.default_rb)
        box_layout_type.addWidget(self.matrix_rb)

        # layout for translate checkbox
        box_transform = QtWidgets.QHBoxLayout()
        box_transform.addWidget(self.translate_cb)
        box_transform.addWidget(self.rotate_cb)

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
        main_layout.addLayout(box_layout_type)
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

    def update_force_visibility_rotate(self, checked):
        self.rotate_cb.setVisible(checked)

    def create_constraint(self):

        sel = pm.ls(sl=1)
        source = sel[0]
        target = sel[1]

        if self.prntConst_rb.isChecked():
            self.create_parent_constraint(source, target)

        elif self.pntConst_rb.isChecked():
            self.create_point_constraint(source, target)
        elif self.orntConst_rb.isChecked():
            self.create_orient_constraint(source, target)
        else:
            self.create_scale_constraint(source, target)

    def create_parent_constraint(self, source, target):
        if self.maintainOffset_cb.isChecked():
            pm.parentConstraint(source, target, mo=1)
        else:
            pm.parentConstraint(source, target, mo=0)

    def create_point_constraint(self, source, target):
        if self.maintainOffset_cb.isChecked():
            pm.pointConstraint(source, target, mo=1)
        else:
            pm.pointConstraint(source, target, mo=0)

    def create_orient_constraint(self, source, target):
        if self.maintainOffset_cb.isChecked():
            pm.orientConstraint(source, target, mo=1)
        else:
            pm.orientConstraint(source, target, mo=0)

    def create_scale_constraint(self, source, target):
        if self.maintainOffset_cb.isChecked():
            pm.scaleConstraint(source, target, mo=1)
        else:
            pm.scaleConstraint(source, target, mo=0)


        """parentConstraint -mo -weight 1;

        parentConstraint -weight 1;

        parentConstraint -skipTranslate x -skipTranslate y -skipTranslate z -weight 1;

        parentConstraint -skipRotate x -skipRotate y -skipRotate z -weight 1;

        parentConstraint -skipTranslate y -skipTranslate z -skipRotate y -skipRotate z -weight 1;

        doCreateParentConstraintArgList 1 { "0","0","0","1","1","0","1","1","1","","1" };
        parentConstraint -skipTranslate y -skipTranslate z -skipRotate y -skipRotate z -weight 1;"""


if __name__ == "__main__":

    try:
        test_dialogue.close()
        test_dialogue.deleteLater()
    except:
        pass
    test_dialogue = TestDialogue()
    test_dialogue.show()
