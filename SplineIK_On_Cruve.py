import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from maya import OpenMaya

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import numpy as np


def maya_main_window():
    maya_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


"""class MyLineEdit(QtWidgets.QLineEdit):
    enter_pressed = QtCore.Signal(str)

    def keyPressEvent(self, e):
        super(MyLineEdit, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit()"""


class TestDialogue(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialogue, self).__init__(parent)

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
        self.name_label = QtWidgets.QLabel("Name")
        self.number_sp = QtWidgets.QSpinBox()
        self.control_label = QtWidgets.QLabel("Control")
        self.number_sp.setFixedWidth(50)
        self.number_sp.setValue(15)
        self.number_sp.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        # radio buttons
        self.secondary_rb = QtWidgets.QRadioButton("Secondary")
        self.tertiary_rb = QtWidgets.QRadioButton("Tertiary")

        # radio buttons axis
        self.axisX_rb = QtWidgets.QRadioButton("x")
        self.axisX_rb.setChecked(True)
        self.axisY_rb = QtWidgets.QRadioButton("y")
        self.axisZ_rb = QtWidgets.QRadioButton("z")

        # check boxes
        self.wave_cb = QtWidgets.QCheckBox("Wave")
        self.sine_cb = QtWidgets.QCheckBox("Sine")
        self.stretch_cb = QtWidgets.QCheckBox("Stretch")
        self.connected_cb = QtWidgets.QCheckBox("Connected")
        self.connected_cb.setChecked(True)

        # buttons
        self.create_btn = QtWidgets.QPushButton("Create")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):
        # layout for input field field
        input_field_layout_form = QtWidgets.QGridLayout()
        input_field_layout_form.addWidget(self.name_label, 1, 1)
        input_field_layout_form.addWidget(self.name_field, 1, 2)
        input_field_layout_form.addWidget(self.control_label, 2, 1)
        input_field_layout_form.addWidget(self.number_sp, 2, 2)

        # layout for levels
        rb_layout_hbox = QtWidgets.QHBoxLayout()
        rb_layout_hbox.addWidget(self.secondary_rb)
        rb_layout_hbox.addWidget(self.tertiary_rb)

        # layout for axis
        rb_axis_layout_hbox = QtWidgets.QHBoxLayout()
        rb_axis_layout_hbox.addWidget(self.axisX_rb)
        rb_axis_layout_hbox.addWidget(self.axisY_rb)
        rb_axis_layout_hbox.addWidget(self.axisZ_rb)

        # layout for buttons
        button_layout_hbox = QtWidgets.QHBoxLayout()
        button_layout_hbox.addWidget(self.create_btn)
        button_layout_hbox.addWidget(self.cancel_btn)

        # layout for checkboxes
        checkbox_layout_hbox = QtWidgets.QHBoxLayout()
        checkbox_layout_hbox.addWidget(self.stretch_cb)
        checkbox_layout_hbox.addWidget(self.wave_cb)
        checkbox_layout_hbox.addWidget(self.sine_cb)

        """# arrange layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(input_field_layout_form)
        main_layout.addLayout(checkbox_layout_hbox)
        main_layout.addLayout(rb_axis_layout_hbox)
        main_layout.addLayout(rb_layout_hbox)
        main_layout.addLayout(button_layout_hbox)"""

        # arrange layouts
        main_layout = QtWidgets.QFormLayout(self)
        main_layout.addRow("", input_field_layout_form)
        main_layout.addRow("Front Axis:", rb_axis_layout_hbox)
        main_layout.addRow("Name:", button_layout_hbox)

    def create_connections(self):
        self.name_field.editingFinished.connect(self.chain_name)
        self.number_sp.valueChanged.connect(self.control_count)

        self.create_btn.clicked.connect(self.spline_ik_chain)
        self.cancel_btn.clicked.connect(self.close)

    def spline_ik_chain(self):
        # select curve
        sel = pm.ls(sl=1)
        if len(sel) > 1:
            i = 1
            for s in sel:
                crv = pm.rebuildCurve(s, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=1, kt=0, s=9, d=3,
                                      tol=0.01)
                counter = i
                self.create_spline_chain(crv, counter)
                i = i + 1
        else:
            counter = 1
            crv = pm.rebuildCurve(sel[0], ch=0, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=1, kt=0, s=9, d=3,
                                  tol=0.01)
            self.create_spline_chain(crv, counter)
        if self.stretch_cb.isChecked():
            print("stretch checked")

    def chain_name(self):
        name = self.name_field.text()
        return name

    def control_count(self):
        return self.number_sp.value()

    def createOffset(self, target, suffix):

        pm.select(clear=1)
        # assuming last naming convention is like name_C_001_TYPE (Leg_C_001_CTRL)
        offset_name = str(target).split('_')
        offset_name[-1] = suffix
        offset_name_joined = '_'.join(offset_name)
        offset_grp = pm.group(target, n=offset_name_joined)
        pm.xform(offset_grp, cp=1)

        return offset_grp

    def snap(self, obj, target):
        prntConst = pm.parentConstraint(target, obj, mo=0)
        pm.delete(prntConst)

    def getUParam(self, pnt=[], crv=None):
        point = OpenMaya.MPoint(pnt[0], pnt[1], pnt[2])
        curveFn = OpenMaya.MFnNurbsCurve(self.getDagPath(crv))
        paramUtill = OpenMaya.MScriptUtil()
        paramPtr = paramUtill.asDoublePtr()
        isOnCurve = curveFn.isPointOnCurve(point)
        if isOnCurve == True:

            curveFn.getParamAtPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)
        else:
            point = curveFn.closestPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)
            curveFn.getParamAtPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)

        param = paramUtill.getDouble(paramPtr)
        return param

    def getDagPath(self, objectName):
        if isinstance(objectName, list) == True:
            oNodeList = []
            for o in objectName:
                selectionList = OpenMaya.MSelectionList()
                selectionList.add(o)
                oNode = OpenMaya.MDagPath()
                selectionList.getDagPath(0, oNode)
                oNodeList.append(oNode)
            return oNodeList
        else:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(objectName)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            return oNode

    def create_joint_on_curve(self, name, crv, segments):

        # control for controlling animation of joints on curve
        # curve
        crv = crv[0]
        # joint lists
        jnt_list = []

        uVal = 1.0 / (segments)

        pm.select(clear=1)
        i = 1

        motionpath_front_axis = 1
        # set front axis
        if self.axisX_rb.isChecked():
            motionpath_front_axis = 1  # x
        elif self.axisY_rb.isChecked():
            motionpath_front_axis = 2  # y
        elif self.axisZ_rb.isChecked():
            motionpath_front_axis = 3  # z

        # attach joints to curve
        # using numpy to distribute the number evenly between 0 to 1
        uval_list = np.linspace(0, 1, segments)

        mpath_node_list = []
        for i in range(segments):
            jnt = pm.joint(n=name + '_ctrl' + '_C_' + '{:03}'.format(i) + '_JOIN', rad=0.02)
            jnt_list.append(jnt)
            pm.select(clear=1)

            # create motion path node
            mpath_node_name = jnt + "_MPATH"
            mPath_node = pm.shadingNode("motionPath", asUtility=True, n=mpath_node_name)
            pm.setAttr(mPath_node + ".follow", 1)
            pm.setAttr(mPath_node + ".frontAxis", motionpath_front_axis)

            # set worldobject to stop fliping
            pm.setAttr(mPath_node + ".worldUpType", 1)
            # pm.connectAttr(upObj_loc + ".worldMatrix[0]", mPath_node + ".worldUpMatrix")

            # connect joint to curve using motion path
            pm.connectAttr(crv + ".worldSpace[0]", mPath_node + ".geometryPath", f=0)
            pm.connectAttr(mPath_node + ".allCoordinates", jnt + ".translate", f=0)
            pm.connectAttr(mPath_node + ".rotateX", jnt + ".rotateX", f=0)

            # delete key on u value of motion path
            pm.cutKey(mPath_node + ".u", time=(0, 120))

            # set u value
            pm.setAttr(mPath_node + ".u", uval_list[i])

            pm.disconnectAttr(jnt + ".translate")
            pm.disconnectAttr(jnt + ".rotate")
            pm.delete(mPath_node)

            i = i + 1
        return jnt_list

    def create_joint_on_cvs(self, sel, heirarchy=True):

        curve_cvs = pm.ls('{0}.cv[:]'.format(sel[0]), fl=True)
        jnt_list = []
        jnt_pos_list = []
        name = self.name_field.text()

        # create joint on cv positions
        i = 1
        for cv in curve_cvs:
            # get position of vertex
            pos = pm.xform(cv, ws=1, q=1, t=1)
            # create joint
            jnt = pm.joint(n=name + '_C_' + '{:03}'.format(i) + '_JOIN', p=pos, rad=0.02)
            pm.parent(jnt, w=1)

            jnt_pos_list.append(pos)
            jnt_list.append(jnt)
            i = i + 1

        i = 0
        if heirarchy:
            for i in range(len(jnt_list) - 1):
                pm.parent(jnt_list[i], jnt_list[i + 1])
                i = i + 1
            pm.reroot(jnt_list[0])

        return [jnt_list, jnt_pos_list]

    def create_spline_chain(self, sel, counter):

        # clear selection to avoid parenting
        pm.select(clear=1)
        # name field output

        control_count = self.number_sp.value()

        name = self.name_field.text() + str(counter)

        # control field output
        segments = self.number_sp.value()

        # create groups
        if not pm.objExists("rig_C_001_GRUP"):
            rig_grup = pm.group(n="rig_C_001_GRUP")

        if not pm.objExists("bodyDeform_C_001_GRUP"):
            body_def_group = pm.group(n="bodyDeform_C_001_GRUP")

        rig_grup = "rig_C_001_GRUP"
        body_def_group = "bodyDeform_C_001_GRUP"

        jnt_return_list = self.create_joint_on_cvs(sel)
        jnt_list = jnt_return_list[0]
        jnt_pos_list = jnt_return_list[1]

        # orient chain
        pm.joint(jnt_list[0], e=1, oj="xyz", secondaryAxisOrient="yup", ch=1)
        pm.joint(jnt_list[-1], e=1, oj="none")

        # rebuilt curve
        crv = pm.rebuildCurve(sel, ch=0, rpo=1, rt=5, end=1, kr=0, kcp=0, kep=1, kt=0, s=control_count, d=3,
                              tol=0.01)
        # ____________________________________create splineIK curve_______________________________________________

        # create control joints on curve
        pm.select(cl=1)
        ctrl_jnts = self.create_joint_on_curve(name, crv, control_count)

        for c in ctrl_jnts:
            pm.setAttr("{}.{}".format(c, "rotateX"), 0)
            pm.setAttr("{}.{}".format(c, "rotateY"), 0)
            pm.setAttr("{}.{}".format(c, "rotateZ"), 0)

        # create splineIK handle
        i = 1
        pm.select(clear=1)

        ik_hdl = pm.ikHandle(n='ikh', sj='{}'.format(jnt_list[0]), ee='{}'.format(jnt_list[-1]), sol='ikSplineSolver',
                             ccv=False, pcv=False, c=crv[0])[0]
        pm.rename(ik_hdl, name + '_C_' + '{:03}'.format(i) + '_KHDL')

        pm.select(ctrl_jnts, crv)
        pm.skinCluster(ctrl_jnts, crv, tsb=1)

        # create controls on joints
        ctrl_list = []
        ctrl_fk_list = []
        ctrl_fk_offset_list = []
        aim_list = []
        follow_list = []
        offset_grp_list = []
        pm.select(clear=1)
        i = 1
        # create controls with offset group
        for c in ctrl_jnts:
            ctrl = pm.circle(n=name + '_ik_C_' + '{:03}'.format(i) + '_CTRL', c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=0.2,
                             d=1, ut=0, tol=0.01, s=4, ch=0)

            pm.setAttr("{}.{}".format(ctrl[0], "rotateX"), 45)
            pm.makeIdentity(ctrl, apply=True, t=1, r=1, s=1, n=0, pn=1)

            fk_ctrl = pm.circle(n=name + '_fk_C_' + '{:03}'.format(i) + '_CTRL', c=(0, 0, 0), nr=(1, 0, 0), sw=360,
                                r=0.1, d=3, ut=0, tol=0.01, s=8, ch=0)

            fk_ctrl_offset = self.createOffset(fk_ctrl[0], 'GRUP')
            offset_grp = self.createOffset(ctrl[0], 'GRUP')

            pm.delete(pm.parentConstraint(c, offset_grp))
            pm.delete(pm.parentConstraint(c, fk_ctrl_offset))
            pm.parent(offset_grp, fk_ctrl)

            ctrl_list.append(ctrl)
            offset_grp_list.append(offset_grp)
            ctrl_fk_offset_list.append(fk_ctrl_offset)
            ctrl_fk_list.append(fk_ctrl)
            i = i + 1

        i = 0
        # constraint the joints to controls
        for i in range(len(ctrl_jnts)):
            pm.parentConstraint(ctrl_list[i], ctrl_jnts[i], mo=1)
            i += 1
        ctrl_fk_list.reverse()
        ctrl_fk_offset_list.reverse()
        for i in range(len(ctrl_fk_list) - 1):
            pm.parent(ctrl_fk_offset_list[i], ctrl_fk_list[i + 1])
            i = i + 1

        spline_deform_grup = self.createOffset(jnt_list[0], "GRUP")

        # pm.parent(jnt_list, spline_deform_grup)
        pm.parent(ik_hdl, spline_deform_grup)
        pm.parent(ctrl_jnts, spline_deform_grup)
        pm.parent(crv, spline_deform_grup)
        pm.parent(spline_deform_grup, body_def_group)


if __name__ == "__main__":

    try:
        test_dialogue.close()
        test_dialogue.deleteLater()
    except:
        pass
    test_dialogue = TestDialogue()
    test_dialogue.show()
