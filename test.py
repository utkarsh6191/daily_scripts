import pymel.core as pm
import maya.cmds as cmds

"""sel = pm.ls(sl=1)
print sel
ctrl = sel[0]
print ctrl

#pm.addAttr(ctrl,ln ="DYNAMIC",at="enum",en ="CONTROL:",ch =1, k=0)
pm.addAttr(ctrl,ln= "simulationMethod",at= "enum",en= "Off:Static:Dynamic Follicles:All follicles:", k=1)
pm.addAttr(ctrl, ln= "mass" ,at ="double" ,dv= 1 , k=1)
pm.addAttr(ctrl,ln= "friction",at ="double" ,dv= 0.5 , k=1)
pm.addAttr(ctrl, ln= "gravity",at= "double",dv= 0.98, k=1 )
pm.addAttr(ctrl,ln ="bounce",at ="double" ,dv= 0, k=1 )
pm.addAttr(ctrl,ln= "stiffness",at="double",dv= .15, k=1)
pm.addAttr(ctrl,ln= "twistResistance",at="double",dv= 0, k=1)
pm.addAttr(ctrl,ln= "turbulenceStrength",at="double",dv= 0, k=1)
pm.addAttr(ctrl,ln= "turbulenceFrequency",at="double",dv= 0.2, k=1)
pm.addAttr(ctrl,ln= "turbulenceSpeed",at="double",dv= 0.2, k=1)
pm.addAttr(ctrl,ln= "noise",at="double",dv= 0, k=1)

hairsys = sel[1:]

for h in hairsys:
    hShape = pm.listRelatives(h, s=1)[0]
    pm.connectAttr(ctrl + ".simulationMethod",hShape+".simulationMethod"  )
    pm.connectAttr(ctrl + ".mass", hShape+".mass" )
    pm.connectAttr(ctrl + ".friction", hShape+".friction" )
    pm.connectAttr(ctrl + ".gravity",hShape+".gravity" )
    pm.connectAttr(ctrl + ".bounce", hShape+".bounce" )
    pm.connectAttr(ctrl + ".stiffness", hShape+".stiffness" )
    pm.connectAttr(ctrl + ".twistResistance",hShape+".twistResistance" )
    pm.connectAttr(ctrl + ".turbulenceStrength", hShape+".turbulenceStrength" )
    pm.connectAttr(ctrl + ".turbulenceFrequency", hShape + ".turbulenceFrequency")
    pm.connectAttr(ctrl + ".turbulenceSpeed", hShape+".turbulenceSpeed" )
    pm.connectAttr(ctrl + ".noise", hShape + ".noise")
"""


def createOffset(target, name):
    pm.select(clear=1)
    ctrl_parent = pm.listRelatives(target, p=1)
    offset_grp = pm.group(target, n=target[0] + name)
    pm.xform(offset_grp, cp=1)

    return offset_grp


def snap(obj, target):
    prntConst = pm.parentConstraint(target, obj, mo=0)

    pm.delete(prntConst)


def jntsOnCrv(curve=None, segments=5):
    # creates an oriented joint chain that follows a selected curve
    if segments < 2:
        return
    if not curve:
        curve = cmds.ls(sl=1, o=1)[0]

    # use pointOnCurve(pp=0->2) to find world coordinates on the curve
    jnts = []
    a = 0.0
    # find the max U value. It's equal to the number of spans on the curve
    u = cmds.getAttr(curve + ".spans")
    # these have to be float values!
    i = u / (float(segments) - 1.0)
    cmds.select(cl=1)
    # c will be used to check for computational errors because on some numbers we end at segments - 1
    c = 0
    while a <= u:
        jnt = cmds.joint(p=cmds.pointOnCurve(curve, pr=a))
        pm.parent(jnt, w=1)
        jnts.append(jnt)
        a += i
        c += 1

    # in some cases (segments=10,12,19) we end at one joint before the end. This fixes this problem.
    if c != segments:
        jnts.append(cmds.joint(p=cmds.pointOnCurve(curve, pr=u)))

    return jnts


sel = pm.ls(sl=1, fl=1)
number_of_controls = 9
level = 3
# clear selection to avoid parenting
pm.select(clear=1)

if (pm.objExists("rig_C_001_GRUP") == False):
    rig_grup = pm.group(n="rig_C_001_GRUP")

if (pm.objExists("bodyDeform_C_001_GRUP") == False):
    bodyDef_grup = pm.group(n="bodyDeform_C_001_GRUP")

rig_grup = "rig_C_001_GRUP"
bodyDef_grup = "bodyDeform_C_001_GRUP"

jntList = []
jntPosList = []
bodydeform_obj = []

# create joints on vrtx
for s in sel:
    # get position of vertex
    pos = pm.xform(s, ws=1, q=1, t=1)

    # create joint
    jnt = pm.joint()
    pm.parent(jnt, w=1)
    pm.xform(jnt, ws=1, t=pos)

    jntPosList.append(pos)
    jntList.append(jnt)

# create joint chain
selectionLength = len(jntList) - 1
i = 0

for i in range(selectionLength):
    pm.parent(jntList[i], jntList[i + 1])
    i = i + 1

pm.reroot(jntList[0])

# orient chain
pm.joint(jntList[0], e=1, oj="xyz", ch=1)
pm.joint(jntList[-1], e=1, oj="none")

crv = pm.curve(p=jntPosList, d=3)
# create splineIK curve

pm.select(cl=1)
segments = 9
ctrlJnts = jntsOnCrv(str(crv), segments)

ctrljntPosList = []

for c in ctrlJnts:
    # get position of vertex
    pos = pm.xform(c, ws=1, q=1, t=1)

    # jnt pos
    ctrljntPosList.append(pos)

splineIkCrv = pm.curve(p=ctrljntPosList, d=3, n='splineIkCrv')
pm.delete(crv)

ikHdl = pm.ikHandle(n='ikh', sj=str(jntList[0]), ee=str(jntList[-1]), sol='ikSplineSolver', ccv=False, pcv=False,
                    c=splineIkCrv)[0]

pm.select(ctrlJnts, splineIkCrv)
pm.skinCluster(ctrlJnts, splineIkCrv, tsb=1)

# create controls on joints
ctrl_list = []
aim_list = []
follow_list = []
offset_grp_list = []
pm.select(clear=1)

# create controls with offset group
for c in ctrlJnts:
    ctrl = pm.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)

    snap(ctrl, c)

    offset_grp = createOffset(ctrl, "_offset")
    follow_grp = createOffset(ctrl, "_follow")
    aim_grp = createOffset(ctrl, "_aim")

    ctrl_list.append(ctrl)
    aim_list.append(aim_grp)
    offset_grp_list.append(offset_grp)
    follow_list.append(follow_grp)

i = 0
# constraint the joints to controls
for i in range(len(ctrlJnts)):
    pm.parentConstraint(ctrl_list[i], ctrlJnts[i], mo=1)
    i += 1

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

root_ctrl = pm.circle(n="root_ctrl", c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=0)
root_ctrl_grup = createOffset(root_ctrl, "_offset")

# create sine deformer
sineCrv = pm.duplicate(splineIkCrv)
pm.rename(sineCrv, 'sineCrv')

pm.select(sineCrv)

# pm.nonLinear(type= 'sine',lowBound=1, highBound =1,amplitude= 0, wavelength= 2,dropoff= 0, offset= 0)
sineDef = pm.nonLinear(type='sine')

pm.addAttr(root_ctrl, ln="sine", at="enum", en="control:", k=1)
pm.addAttr(root_ctrl, ln="sineSwitch", at="bool", k=1)
pm.addAttr(root_ctrl, ln="sineAmplitude", at="double", dv=0, k=1)
pm.addAttr(root_ctrl, ln="sineWaveLength", at="double", dv=2, k=1)
pm.addAttr(root_ctrl, ln="sineHighBound", at="double", min=0, max=10, dv=1, k=1)
pm.addAttr(root_ctrl, ln="sineLowBound", at="double", min=-10, max=0, dv=-1, k=1)
pm.addAttr(root_ctrl, ln="sineDropOff", at="double", min=-1, max=1, dv=0, k=1)

# create wave deformer
waveCrv = pm.duplicate(splineIkCrv)
pm.rename(waveCrv, 'waveCrv')
pm.select(waveCrv)
# pm.nonLinear(type= "wave",minRadius =0,maxRadius= 1,amplitude= 0,wavelength =0,dropoff= 0,offset=0)
waveDef = pm.nonLinear(type="wave")

pm.addAttr(root_ctrl, ln="wave", at="enum", en="control:", k=1)
pm.addAttr(root_ctrl, ln="waveSwitch", at="bool", k=1)
pm.addAttr(root_ctrl, ln="waveAmplitude", at="double", dv=0, k=1)
pm.addAttr(root_ctrl, ln="waveWaveLength", at="double", dv=2, k=1)
pm.addAttr(root_ctrl, ln="waveOffset", at="double", min=-10, max=10, dv=0, k=1)
pm.addAttr(root_ctrl, ln="waveDropOffPosition", at="double", min=-1, max=1, dv=0, k=1)
pm.addAttr(root_ctrl, ln="waveMinRadius", at="double", min=0, max=10, dv=0, k=1)
pm.addAttr(root_ctrl, ln="waveMaxRadius", at="double", min=0, max=10, dv=0, k=1)

bshp = pm.blendShape(sineCrv, waveCrv, splineIkCrv)

pm.connectAttr(str(root_ctrl[0]) + ".sineSwitch", bshp[0] + ".sineCrv")
pm.connectAttr(str(root_ctrl[0]) + ".waveSwitch", bshp[0] + ".waveCrv")

pm.connectAttr(str(root_ctrl[0]) + '.sineAmplitude', str(sineDef[0]) + '.amplitude')
pm.connectAttr(str(root_ctrl[0]) + '.sineHighBound', str(sineDef[0]) + '.highBound')
pm.connectAttr(str(root_ctrl[0]) + '.sineLowBound', str(sineDef[0]) + '.lowBound')
pm.connectAttr(str(root_ctrl[0]) + '.sineWaveLength', str(sineDef[0]) + '.wavelength')
pm.connectAttr(str(root_ctrl[0]) + '.sineSwitch', str(sineDef[0]) + '.offset')

pm.connectAttr(str(root_ctrl[0]) + '.waveAmplitude', str(waveDef[0]) + '.amplitude')
pm.connectAttr(str(root_ctrl[0]) + '.waveDropOffPosition', str(waveDef[0]) + '.dropoffPosition')
pm.connectAttr(str(root_ctrl[0]) + '.waveMaxRadius', str(waveDef[0]) + '.maxRadius')
pm.connectAttr(str(root_ctrl[0]) + '.waveMinRadius', str(waveDef[0]) + '.minRadius')
pm.connectAttr(str(root_ctrl[0]) + '.waveOffset', str(waveDef[0]) + '.offset')
pm.connectAttr(str(root_ctrl[0]) + '.waveWaveLength', str(waveDef[0]) + '.wavelength')

pm.parent(offset_grp_list, root_ctrl[0])
bodydeform_obj.append(jntList)
bodydeform_obj.append(ctrlJnts)
bodydeform_obj.append(ikHdl)
bodydeform_obj.append(splineIkCrv)
bodydeform_obj.append(sineCrv)
bodydeform_obj.append(waveCrv)
bodydeform_obj.append(waveDef)
bodydeform_obj.append(sineDef)

pm.parent(bodydeform_obj, bodyDef_grup)

pm.parent(bodyDef_grup, rig_grup)
pm.parent(root_ctrl_grup, rig_grup)
