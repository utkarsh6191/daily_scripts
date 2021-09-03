import maya.cmds as cmds


def non_zero_joints(joint):
    trans = ['translate', 'rotate', 'scale']

    axis = ['x', 'y', 'z']

    rotX = cmds.getAttr(joint + '.rotateX')
    rotY = cmds.getAttr(joint + '.rotateY')
    rotZ = cmds.getAttr(joint + '.rotateZ')

    jntOrntX = cmds.getAttr(joint + '.jointOrientX')
    jntOrntY = cmds.getAttr(joint + '.jointOrientY')
    jntOrntZ = cmds.getAttr(joint + '.jointOrientZ')
    print jntOrntY

    if (rotX != 0):
        jntOrntX = rotX + jntOrntX
        cmds.setAttr(joint + '.jointOrientX', jntOrntX)

    if (rotY != 0):
        jntOrntY = rotY + jntOrntY
        cmds.setAttr(joint + '.jointOrientY', jntOrntY)

    if (rotZ != 0):
        jntOrntZ = rotZ + jntOrntZ
        cmds.setAttr(joint + '.jointOrientZ', jntOrntZ)

    cmds.setAttr(joint + '.rotateX', 0)
    cmds.setAttr(joint + '.rotateY', 0)
    cmds.setAttr(joint + '.rotateZ', 0)


sel = cmds.ls(sl=1)
axises = ['X', 'Y', 'Z']

for s in sel:
    constraint_node = cmds.listConnections(s, d=1, type="parentConstraint")
    print s
    print constraint_node
    constraint_joint = cmds.listConnections(constraint_node)[0]
    print constraint_joint
    cmds.delete(constraint_node[0])
    non_zero_joints(constraint_joint)
    for axis in axises:
        cmds.connectAttr("{}.{}".format(s, "rotate" + axis),
                         "{}.{}".format(constraint_joint, "rotate" + axis))
