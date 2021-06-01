from PySide2 import QtCore
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

        self.setWindowTitle("testDialoge")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.matrix_rb = QtWidgets.QRadioButton("matrix")
        self.default_rb = QtWidgets.QRadioButton("default")

        self.prntConst_rb = QtWidgets.QRadioButton("Parent")
        self.prntConst_rb.setChecked(True)
        self.pntConst_rb = QtWidgets.QRadioButton("Point")
        self.orntConst_rb = QtWidgets.QRadioButton("Orient")
        self.scaleConst_rb = QtWidgets.QRadioButton("Scale")

        self.maintainOffset_cb = QtWidgets.QCheckBox("maintain offset")
        self.axisX_cb = QtWidgets.QCheckBox("X")
        self.axisY_cb = QtWidgets.QCheckBox("Y")
        self.axisZ_cb = QtWidgets.QCheckBox("Z")

        self.create_btn = QtWidgets.QPushButton("Create")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):
        # layout for constraint type
        form_layout = QtWidgets.QGridLayout()
        form_layout.addWidget(self.prntConst_rb, 1, 1)
        form_layout.addWidget(self.pntConst_rb, 1, 2)
        form_layout.addWidget(self.orntConst_rb, 2, 1)
        form_layout.addWidget(self.scaleConst_rb, 2, 2)
        # layout for constraint method
        box_layout1 = QtWidgets.QHBoxLayout()
        box_layout1.addWidget(self.default_rb)
        box_layout1.addWidget(self.matrix_rb)
        # layout for constraint method
        box_layout2 = QtWidgets.QHBoxLayout()
        box_layout2.addWidget(self.axisX_cb)
        box_layout2.addWidget(self.axisY_cb)
        box_layout2.addWidget(self.axisZ_cb)
        # layout for buttons
        box_layout3 = QtWidgets.QHBoxLayout()
        box_layout3.addStretch()
        box_layout3.addWidget(self.maintainOffset_cb)
        box_layout3.addWidget(self.create_btn)
        box_layout3.addWidget(self.cancel_btn)
        # arrange layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(box_layout1)
        main_layout.addLayout(box_layout2)
        main_layout.addLayout(box_layout3)

    def create_connections(self):
        self.cancel_btn.clicked.connect(self.close)

        self.create_btn.clicked.connect(self.createConstraint)

    def createConstraint_default(self):

        maintainOffset_chk = self.maintainOffset_cb.isChecked()

        prntConst_rb_chk = self.prntConst_rb.toggled()
        pntConst_rb_chk = self.pntConst_rb.toggled()
        scaleConst_rb_chk = self.scaleConst_rb.toggled()

        sel = pm.ls(sl=1)
        source = sel[0]
        target = sel[1]

        if maintainOffset_chk:
            if prntConst_rb_chk:
                pm.parentConstraint(source, target, mo=1)
            if prntConst_rb_chk:
                pm.pointConstraint(source, target, mo=1)
            if prntConst_rb_chk:
                pm.scaleConstraint(source, target, mo=1)

        else:
            if prntConst_rb_chk:
                pm.parentConstraint(source, target, mo=0)
            if pntConst_rb_chk:
                pm.parentConstraint(source, target, mo=0)
            if scaleConst_rb_chk:
                pm.parentConstraint(source, target, mo=0)

    def createConstraint(self):
        self.createConstraint_default()

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
