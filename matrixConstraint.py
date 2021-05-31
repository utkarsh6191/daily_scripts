import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMaya as om

sel = pm.ls(sl=1)

ctrl = sel[0]
# todo: cleaning transform values of control without freezing transform and keeping the pivots

print(pm.matrixUtil(ctrl, q=1, matrix=1, os=1))

# todo: transfer transform values to offset parent matrix

# todo: zero out transform values to remove additional transform

# todo: mulitply world matrix of control and inverse world matrix of the parent of joint

# todo: connect sum to offset parent matrix

# todo: zero out transform and joint orient to remove additional transform
