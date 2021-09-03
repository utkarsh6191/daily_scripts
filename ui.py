"""import pymel.core as pm
import numpy as np
import pymel.core as pm
import maya.OpenMayaUI as omui
from maya import OpenMaya

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
"""


def maya_main_window():
    maya_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class RenameSelection(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(RenameSelection, self).__init__(parent)

        self.setWindowTitle("Create SplineIK chain")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # input field
        self.name_field = QtWidgets.QLineEdit()
        self.name_field.setMinimumWidth(150)

        self.side_cb = QtWidgets.QComboBox()
        self.side_cb.addItems(["C", "L", "R", "U", "D", "F", "B"])

        self.name_label = QtWidgets.QLabel("Part name")
        self.side_label = QtWidgets.QLabel("Side")
        # buttons
        self.rename_btn = QtWidgets.QPushButton("Rename")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):
        # layout for input field field
        input_field_layout_form = QtWidgets.QGridLayout()
        input_field_layout_form.addWidget(self.name_label, 1, 1)
        input_field_layout_form.addWidget(self.name_field, 1, 2)
        input_field_layout_form.addWidget(self.side_label, 2, 1)
        input_field_layout_form.addWidget(self.side_cb, 2, 2)

        # layout for buttons
        button_layout_hbox = QtWidgets.QHBoxLayout()
        button_layout_hbox.addWidget(self.rename_btn)
        button_layout_hbox.addWidget(self.cancel_btn)

        # arrange layouts
        main_layout = QtWidgets.QFormLayout(self)
        main_layout.addRow("", input_field_layout_form)
        main_layout.addRow("", button_layout_hbox)

    def create_connections(self):
        self.rename_btn.clicked.connect(self.rename_selection)
        self.cancel_btn.clicked.connect(self.close)

    def rename_selection(self):
        sel = pm.ls(sl=1)

        name = self.name_field.text()
        for count in range(self.side_cb.count()):
            side = self.side_cb.itemText(count)

        pm.rename(sel, name + '_' + self.side_cb.currentText() + '_' + "DONE")


if __name__ == "__main__":

    try:
        test_dialogue.close()
        test_dialogue.deleteLater()
    except:
        pass
    test_dialogue = RenameSelection()
    test_dialogue.show()
