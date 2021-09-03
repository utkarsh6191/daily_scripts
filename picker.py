import sys

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()

    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class DesignerUI(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(DesignerUI, self).__init__(parent)

        self.setWindowTitle("Designer UI")

        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        f = QtCore.QFile("D:/Downloads/Scripts/Scripts/utkarsh/daily_scripts/startCaravan.ui")
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)

        f.close()

    def create_layout(self):
        self.ui.layout().setContentsMargins(6, 6, 6, 6)

    def create_connections(self):
        self.ui.okButton.clicked.connect(self.do_something)
        self.ui.cancelButton.clicked.connect(self.close)


if __name__ == "__main__":

    try:
        designer_ui.close()  # pylint: disable=E0601
        designer_ui.deleteLater()
    except:
        pass

    designer_ui = DesignerUI()
    designer_ui.show()
