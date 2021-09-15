import pymel.core as pm
import maya.OpenMaya as om

sel = pm.ls(sl=1)
min_timeRange = pm.playbackOptions(q=1, min=1)
max_timeRange = pm.playbackOptions(q=1, max=1)
# mirror animation using scale
pm.scaleKey(str(sel[0]), at=['tx', 'ty', 'tz'], valueScale=-1)


def flip_name(source):
    # split object into components to find the side
    object_component = source.split('_')

    # if side is L, replace with R
    if object_component[-3] == 'L':
        flipped_name = source.replace("_L_", "_R_")
        print("left side found")
        return flipped_name

    # if side is R, replace with L
    if object_component[-3] == 'R':
        print("right side found")
        flipped_name = source.replace("_R_", "_L_")
        return flipped_name


# get selection
"""sel = cmds.ls(sl=1)"""
# get keys

# get time slider range of the scene


# mirror on selection
# mirror on opposite side
# select the ctrls to copy keys

# copy keys on flipped side
for s in sel:
    if pm.keyframe(s, q=1, tc=1):
        pm.copyKey(s, time=(min_timeRange, max_timeRange), hierarchy="none", controlPoints=0, shape=1)
        flipped_ctrl = flip_name(str(s))
        print flipped_ctrl
        if pm.objExists(flipped_ctrl):
            pm.pasteKey(flipped_ctrl, option="replace",
                        time=(min_timeRange, max_timeRange), f=(min_timeRange, max_timeRange), copies=1, connect=0)
    else:
        om.MGlobal.displayError("Key doesn't exists on the selection")
