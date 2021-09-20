import maya.api.OpenMaya as om
import pymel.core as pm

TRANSFORM_NODETYPES = ["transform", "joint"]

def has_non_default_locked_attributes(node):
    locked_attributes = []
    for attribute in ["translate", "rotate", "scale", "jointOrient"]:
        default_value = 1 if attribute == "scale" else 0
        for axis in "XYZ":
            if pm.attributeQuery(attribute + axis, node=node, exists=True):
                attribute_name = "{}.{}{}".format(node, attribute, axis)
                current_value = pm.getAttr(attribute_name)
                if pm.getAttr(attribute_name, lock=True) and current_value != default_value:
                    return True
def reset_transforms(node):
    for attribute in ["translate", "rotate", "scale", "jointOrient"]:
        value = 1 if attribute == "scale" else 0
        for axis in "XYZ":
            if pm.attributeQuery(attribute + axis, node=node, exists=True):
                attribute_name = "{}.{}{}".format(node, attribute, axis)
                if not pm.getAttr(attribute_name, lock=True):
                    pm.setAttr(attribute_name, value)
def bake_transform_to_offset_parent_matrix(node):
    if pm.nodeType(node) not in TRANSFORM_NODETYPES:
        raise ValueError("Node {} is not a transform node".format(node))

    if has_non_default_locked_attributes(node):
        raise RuntimeError("Node {} has at least one non default locked attribute(s)".format(node))

    local_matrix = om.MMatrix(pm.xform(node, q=True, m=True, ws=False))
    offset_parent_matrix = om.MMatrix(pm.getAttr(node + ".offsetParentMatrix"))
    baked_matrix = local_matrix * offset_parent_matrix
    pm.setAttr(node + ".offsetParentMatrix", baked_matrix, type="matrix")

    reset_transforms(node)
def bake_transform_to_offset_parent_matrix_selection(node):
    for node in node:
        bake_transform_to_offset_parent_matrix(node)

sel = pm.ls(sl =1)

crv = "curve6"
for s in sel:
    crv = pm.duplicate(crv)[0]
    pm.delete(pm.parentConstraint(s,crv, mo =0))
    bake_transform_to_offset_parent_matrix(crv)
    pm.connectAttr("{}.{}".format(crv, 'rotate.rotateX'),"{}.{}".format(s, 'rotate.rotateX'), f =1)
    pm.connectAttr("{}.{}".format(crv, 'rotate.rotateY'),"{}.{}".format(s, 'rotate.rotateY'), f=1)
    pm.connectAttr("{}.{}".format(crv, 'rotate.rotateZ'),"{}.{}".format(s, 'rotate.rotateZ'), f=1)
    ctrl_name = s.replace('JNT','CTRL')
    pm.rename(crv,ctrl_name)

sel = pm.ls(sl =1)
for s in sel:
    bind_jnt_name = s.replace('CTRL_R', 'R')
    bind_jnt = pm.ls(bind_jnt_name)
    pm.parentConstraint(s,bind_jnt,mo=1)