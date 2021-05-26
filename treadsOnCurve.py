import pymel.core as pm
from maya import cmds, OpenMaya


def getUParam(pnt=[], crv=None):
    point = OpenMaya.MPoint(pnt[0], pnt[1], pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
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


def getDagPath(objectName):
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


# selection curve first and then joints
sel = pm.ls(sl=1)

# curve as first selection
crv = "ropeCurtain_C_001_NRCV"
crv_shape = pm.listRelatives(crv, s=1)[0]

print crv_shape
# wordUp object
upObj_loc = "stitchCurtainRope_C_001_LOCT"

# joint lists
# jntList = sel[1:]
jntList = pm.ls(sl=1)
uValue_list = []
motion_path_list = []
i = 0
# attach joints to curve with out moving them
for j in jntList:
    pos = pm.xform(j, ws=1, q=1, t=1)

    uVal = getUParam(pnt=pos, crv=crv)

    # create motion path node
    mPath_node_name = j + "_MPATH"

    mPath_node = pm.shadingNode("motionPath", asUtility=True, n=mPath_node_name)

    # set parametric length switch off
    pm.setAttr(mPath_node + ".fractionMode", 1)

    # set world object to stop flipping
    pm.setAttr(mPath_node + ".worldUpType", 1)
    pm.connectAttr(upObj_loc + ".worldMatrix[0]", mPath_node + ".worldUpMatrix")

    # connect joint to curve using motion path
    pm.connectAttr(mPath_node + ".rotateOrder", j + ".rotateOrder", f=1)
    pm.connectAttr(mPath_node + ".rotate.rotateX", j + ".rotate.rotateX", f=1)
    pm.connectAttr(mPath_node + ".rotate.rotateY", j + ".rotate.rotateY", f=1)
    pm.connectAttr(mPath_node + ".rotate.rotateZ", j + ".rotate.rotateZ", f=1)

    pm.connectAttr(crv_shape + ".worldSpace[0]", mPath_node + ".geometryPath", f=1)
    pm.connectAttr(mPath_node + ".allCoordinates", j + ".translate", f=1)
    # delete key on u value of motion path
    pm.cutKey(mPath_node + ".u", time=(0, 120))

    # set uvalue
    # pm.setAttr(mPath_node+".u", uVal*i)
    pm.setAttr(mPath_node + ".uValue", uVal)

    uValue_list.append(uVal)
    motion_path_list.append(mPath_node)

    i = i + 1
# __________________________________________
# list motion path node connected to joints
print uValue_list
print motion_path_list
"""motion_path = pm.listConnections(crv, type="motionPath")
print motion_path

uValue_list = []
for m in motion_path:
    # get value of motionpath node
    uValue = pm.getAttr(str(m) + ".uValue")
    uValue_list.append(uValue)
print uValue_list"""
"""
i = 0
for m in motion_path:
    print m
    # itt (inTangent type) and ott (outTangent type) sets the keys to linear
    pm.setDrivenKeyframe(str(m) + ".uValue", currentDriver="stitchCurtainRope_C_001_LOCT" + ".ropeCycle",
                         dv=0, itt="linear", ott="linear", v=uValue_list[i])
    pm.setDrivenKeyframe(str(m) + ".uValue", currentDriver="stitchCurtainRope_C_001_LOCT" + ".ropeCycle",
                         dv=1, itt="linear", ott="linear", v=1 + uValue_list[i])

    # ___________setting keys post infinity and pre  infinity on cycles___________________
    # get animCurveUL node created after setting driven keys
    animCurveUL_node = pm.listConnections(m, type="animCurveUL")[0]

    # set post and pre infinity to cycle
    pm.setAttr(animCurveUL_node.preInfinity, 3)
    pm.setAttr(animCurveUL_node.postInfinity, 3)

    pm.keyframe(animCurveUL_node, option="over", index=0, absolute=1, floatChange=uValue_list[i])
    pm.keyframe(animCurveUL_node, index=0, absolute=1, valueChange=0)
    pm.keyframe(animCurveUL_node, option="over", index=1, absolute=1, floatChange=1 + uValue_list[i])
    # create plusMinus avg node

    uValue_pma = pm.shadingNode("plusMinusAverage", asUtility=1)

    pm.rename(uValue_pma, str(m) + "_pma")
    pm.setAttr(uValue_pma.operation, 2)  # set operation to subtract
    pm.setAttr(uValue_pma.input1D[0], 1)

    #pm.connectAttr(str(animCurveUL_node[0]) +".output", uValue_pma+".input1D[1]", f=1)

    #pm.connectAttr(str(uValue_pma)+".output1D", str(m)+".uValue", f=1)
    i = i + 1

"""
