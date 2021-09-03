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
        self.number_sp.setValue(9)
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
        input_field_layout_form.addWidget(self.connected_cb, 2, 3)

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
        main_layout.addRow("Deform:", checkbox_layout_hbox)
        main_layout.addRow("Front Axis:", rb_axis_layout_hbox)
        main_layout.addRow("Level:", rb_layout_hbox)
        main_layout.addRow("Name:", button_layout_hbox)

    def create_connections(self):
        self.name_field.editingFinished.connect(self.chain_name)
        self.number_sp.valueChanged.connect(self.control_count)

        self.create_btn.clicked.connect(self.spline_ik_chain)
        self.cancel_btn.clicked.connect(self.close)

    def spline_ik_chain(self):
        """if (pm.selectPref(tso=True, q=True) == 0):
            pm.selectPref(tso=True)
        print(pm.ls(orderedSelection=True))"""

        # select curve
        sel = pm.ls(sl=1)
        # pm.polySelectConstraint(dis =1)

        name = self.chain_name()
        count = self.control_count()

        self.create_spline_chain(sel)
        if self.stretch_cb.isChecked():
            print("stretch checked")

    def chain_name(self):
        name = self.name_field.text()
        return name

    def control_count(self):
        return self.number_sp.value()

    def createOffset(self, target, suffix):

        pm.select(clear=1)
        ctrl_parent = pm.listRelatives(target, p=1)
        offset_grp = pm.group(target, n=target[0] + suffix)
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
        crv = crv

        # joint lists
        jntList = []

        uVal = 1.0 / (segments)

        # wordUp object
        upObj_loc = pm.spaceLocator(n="worldUpObject_LOCT")
        pm.select(clear=1)
        i = 0

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
            jnt = pm.joint()
            jntList.append(jnt)

            jnt_name = name + '_ctrl' + '_C_' + '{:03}'.format(i) + '_JOIN'
            pm.rename(jnt, jnt_name)
            pm.select(clear=1)

            # create motion path node
            mpath_node_name = jnt + "_MPATH"
            mPath_node = pm.shadingNode("motionPath", asUtility=True, n=mpath_node_name)
            pm.setAttr(mPath_node + ".follow", 1)
            pm.setAttr(mPath_node + ".frontAxis", motionpath_front_axis)

            # set worldobject to stop fliping
            pm.setAttr(mPath_node + ".worldUpType", 1)
            pm.connectAttr(upObj_loc + ".worldMatrix[0]", mPath_node + ".worldUpMatrix")

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
        return jntList

    def create_spline_chain(self, sel):

        # clear selection to avoid parenting
        pm.select(clear=1)
        # name field output
        name = self.name_field.text()
        # control field output
        segments = self.number_sp.value()

        # create groups
        if not pm.objExists("rig_C_001_GRUP"):
            rig_grup = pm.group(n="rig_C_001_GRUP")

        if not pm.objExists("bodyDeform_C_001_GRUP"):
            bodyDef_grup = pm.group(n="bodyDeform_C_001_GRUP")

        rig_grup = "rig_C_001_GRUP"
        bodyDef_grup = "bodyDeform_C_001_GRUP"

        jntList = []
        jntPosList = []
        bodydeform_obj = []

        i = 0
        # create joints on vertex
        for s in sel:
            # get position of vertex
            pos = pm.xform(s, ws=1, q=1, t=1)

            # create joint
            jnt = pm.joint()

            jnt_name = name + '_C_' + '{:03}'.format(i) + '_JOIN'
            pm.rename(jnt, jnt_name)
            pm.parent(jnt, w=1)

            pm.xform(jnt, ws=1, t=pos)

            jntPosList.append(pos)
            jntList.append(jnt)
            i = i + 1

        # create joint chain
        selection_length = len(jntList) - 1
        i = 0

        for i in range(selection_length):
            pm.parent(jntList[i], jntList[i + 1])
            i = i + 1

        pm.reroot(jntList[0])

        # orient chain
        pm.joint(jntList[0], e=1, oj="xyz", ch=1)
        pm.joint(jntList[-1], e=1, oj="none")

        crv = pm.curve(p=jntPosList, d=3, n=name + '_C_' + '{:03}'.format(1) + '_NRCV')

        # rebuilt curve
        pm.rebuildCurve(crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=1, kt=0, s=4, d=3, tol=0.01)

        # ____________________________________create splineIK curve_______________________________________________

        # create control joints on curve
        pm.select(cl=1)

        ctrlJnts = self.create_joint_on_curve(name, crv, segments)
        ctrljntPosList = []

        for c in ctrlJnts:
            # get position of vertex
            pos = pm.xform(c, ws=1, q=1, t=1)

            # jnt pos
            ctrljntPosList.append(pos)

        # splineIkCrv = pm.curve(p=ctrljntPosList, d=3)
        # pm.rename(splineIkCrv, name + '_C_' + '{:03}'.format(i) + '_NRCV')
        # pm.delete(crv)

        # create splineIK handle
        ikHdl = pm.ikHandle(n='ikh', sj=str(jntList[0]), ee=str(jntList[-1]),
                            sol='ikSplineSolver', ccv=False, pcv=False, c=crv)[0]
        pm.rename(ikHdl, name + '_C_' + '{:03}'.format(i) + '_KHDL')

        pm.select(ctrlJnts, crv)
        pm.skinCluster(ctrlJnts, crv, tsb=1)

        # create controls on joints
        ctrl_list = []
        aim_list = []
        follow_list = []
        offset_grp_list = []
        pm.select(clear=1)
        i = 0
        # create controls with offset group
        for c in ctrlJnts:
            ctrl = pm.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)

            # self.snap(ctrl[0], c)

            offset_grp = self.createOffset(ctrl, '_C_' + '{:03}'.format(i) + '_GRUP')
            follow_grp = self.createOffset(ctrl, '_follow_C_' + '{:03}'.format(i) + '_GRUP')
            aim_grp = self.createOffset(ctrl, '_aim_C_' + '{:03}'.format(i) + '_GRUP')

            pm.delete(pm.parentConstraint(c, offset_grp))
            ctrl_list.append(ctrl)
            aim_list.append(aim_grp)
            offset_grp_list.append(offset_grp)
            follow_list.append(follow_grp)
            i = i + 1

        i = 0
        # constraint the joints to controls
        for i in range(len(ctrlJnts)):
            pm.parentConstraint(ctrl_list[i], ctrlJnts[i], mo=1)
            i += 1

        primary_controls = []
        secondary_controls = []
        tertiary_controls = []
        if segments > 2:
            middle_control = segments / 2
            primary_controls = ctrl_list[0::4]
            secondary_controls = ctrl_list[2::4]
            tertiary_controls = ctrl_list[0::2]

            print primary_controls
            print secondary_controls
            print tertiary_controls
            print ctrl_list

        if self.connected_cb.isChecked():
            pm.pointConstraint(ctrl_list[0], ctrl_list[-1], follow_list[4], mo=1)
            pm.pointConstraint(ctrl_list[0], ctrl_list[4], follow_list[2], mo=1)
            pm.pointConstraint(ctrl_list[4], ctrl_list[-1], follow_list[6], mo=1)

            pm.pointConstraint(ctrl_list[0], ctrl_list[2], follow_list[1], mo=1)
            pm.pointConstraint(ctrl_list[2], ctrl_list[4], follow_list[3], mo=1)
            pm.pointConstraint(ctrl_list[4], ctrl_list[6], follow_list[5], mo=1)
            pm.pointConstraint(ctrl_list[6], ctrl_list[8], follow_list[7], mo=1)

            pm.aimConstraint(ctrl_list[4], aim_list[2], mo=1, weight=1, aimVector=[0, -1, 0], upVector=[0, 1, 0],
                             worldUpType="objectrotation", worldUpVector=[0, 1, 0], worldUpObject=str(ctrl_list[0][0]))
            pm.aimConstraint(ctrl_list[4], aim_list[6], mo=1, weight=1, aimVector=[0, 1, 0], upVector=[0, 1, 0],
                             worldUpType="objectrotation", worldUpVector=[0, 1, 0], worldUpObject=str(ctrl_list[-1][0]))

            pm.aimConstraint(ctrl_list[2], aim_list[1], mo=1, weight=1, aimVector=[0, -1, 0], upVector=[0, 1, 0],
                             worldUpType="objectrotation", worldUpVector=[0, 1, 0], worldUpObject=str(ctrl_list[0][0]))
            pm.aimConstraint(ctrl_list[2], aim_list[3], mo=1, weight=1, aimVector=[0, -1, 0], upVector=[0, 1, 0],
                             worldUpType="objectrotation", worldUpVector=[0, 1, 0], worldUpObject=str(ctrl_list[4][0]))
            pm.aimConstraint(ctrl_list[6], aim_list[5], mo=1, weight=1, aimVector=[0, 1, 0], upVector=[0, 1, 0],
                             worldUpType="objectrotation", worldUpVector=[0, 1, 0], worldUpObject=str(ctrl_list[4][0]))
            pm.aimConstraint(ctrl_list[6], aim_list[7], mo=1, weight=1, aimVector=[0, 1, 0], upVector=[0, 1, 0],
                             worldUpType="objectrotation", worldUpVector=[0, 1, 0], worldUpObject=str(ctrl_list[-1][0]))

        root_ctrl = pm.group(n=name + '_C_001_CTRL', c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01,
                             s=8, ch=0)
        root_ctrl_grup = self.createOffset(root_ctrl, "_offset")

        # create sine deformer
        if self.sine_cb.isChecked():
            # create sine deformer
            sineCrv = pm.duplicate(splineIkCrv)
            pm.rename(sineCrv, 'sineCrv')

            pm.select(sineCrv)

            sineDef = pm.nonLinear(type='sine')

            # add attributes to control
            pm.addAttr(root_ctrl, ln="sine", at="enum", en="control:", k=1)
            pm.addAttr(root_ctrl, ln="sineSwitch", at="bool", k=1)
            pm.addAttr(root_ctrl, ln="sineAmplitude", at="double", dv=0, k=1)
            pm.addAttr(root_ctrl, ln="sineWaveLength", at="double", dv=2, k=1)
            pm.addAttr(root_ctrl, ln="sineHighBound", at="double", min=0, max=10, dv=1, k=1)
            pm.addAttr(root_ctrl, ln="sineLowBound", at="double", min=-10, max=0, dv=-1, k=1)
            pm.addAttr(root_ctrl, ln="sineDropOff", at="double", min=-1, max=1, dv=0, k=1)

            # create blendshape
            # bshp = pm.blendShape(sineCrv, waveCrv, splineIkCrv)
            bshp = pm.blendShape(sineCrv, splineIkCrv)

            # connect atrribute to deformer
            pm.connectAttr(str(root_ctrl[0]) + ".sineSwitch", bshp[0] + ".sineCrv")

            pm.connectAttr(str(root_ctrl[0]) + '.sineAmplitude', str(sineDef[0]) + '.amplitude')
            pm.connectAttr(str(root_ctrl[0]) + '.sineHighBound', str(sineDef[0]) + '.highBound')
            pm.connectAttr(str(root_ctrl[0]) + '.sineLowBound', str(sineDef[0]) + '.lowBound')
            pm.connectAttr(str(root_ctrl[0]) + '.sineWaveLength', str(sineDef[0]) + '.wavelength')
            pm.connectAttr(str(root_ctrl[0]) + '.sineSwitch', str(sineDef[0]) + '.offset')

            bodydeform_obj.append(sineDef)
            bodydeform_obj.append(sineCrv)

        # create wave deformer
        if self.wave_cb.isChecked():
            # create wave deformer
            waveCrv = pm.duplicate(splineIkCrv)
            pm.rename(waveCrv, 'waveCrv')
            pm.select(waveCrv)

            waveDef = pm.nonLinear(type="wave")

            pm.addAttr(root_ctrl, ln="wave", at="enum", en="control:", k=1)
            pm.addAttr(root_ctrl, ln="waveSwitch", at="bool", k=1)
            pm.addAttr(root_ctrl, ln="waveAmplitude", at="double", dv=0, k=1)
            pm.addAttr(root_ctrl, ln="waveWaveLength", at="double", dv=2, k=1)
            pm.addAttr(root_ctrl, ln="waveOffset", at="double", min=-10, max=10, dv=0, k=1)
            pm.addAttr(root_ctrl, ln="waveDropOffPosition", at="double", min=-1, max=1, dv=0, k=1)
            pm.addAttr(root_ctrl, ln="waveMinRadius", at="double", min=0, max=10, dv=0, k=1)
            pm.addAttr(root_ctrl, ln="waveMaxRadius", at="double", min=0, max=10, dv=0, k=1)

            bshp = pm.blendShape(waveCrv, splineIkCrv)

            pm.connectAttr(str(root_ctrl[0]) + ".waveSwitch", bshp[0] + ".waveCrv")
            pm.connectAttr(str(root_ctrl[0]) + '.waveAmplitude', str(waveDef[0]) + '.amplitude')
            pm.connectAttr(str(root_ctrl[0]) + '.waveDropOffPosition', str(waveDef[0]) + '.dropoffPosition')
            pm.connectAttr(str(root_ctrl[0]) + '.waveMaxRadius', str(waveDef[0]) + '.maxRadius')
            pm.connectAttr(str(root_ctrl[0]) + '.waveMinRadius', str(waveDef[0]) + '.minRadius')
            pm.connectAttr(str(root_ctrl[0]) + '.waveOffset', str(waveDef[0]) + '.offset')
            pm.connectAttr(str(root_ctrl[0]) + '.waveWaveLength', str(waveDef[0]) + '.wavelength')

            bodydeform_obj.append(waveCrv)
            bodydeform_obj.append(waveDef)

        pm.parent(offset_grp_list, root_ctrl[0])
        bodydeform_obj.append(jntList[0])
        bodydeform_obj.append(ctrlJnts)
        bodydeform_obj.append(ikHdl)
        bodydeform_obj.append(splineIkCrv)

        pm.parent(bodydeform_obj, bodyDef_grup)

        pm.parent(bodyDef_grup, rig_grup)
        pm.parent(root_ctrl_grup, rig_grup)


if __name__ == "__main__":

    try:
        test_dialogue.close()
        test_dialogue.deleteLater()
    except:
        pass
    test_dialogue = TestDialogue()
    test_dialogue.show()
