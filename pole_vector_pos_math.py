import maya.cmds as cmds
import maya.OpenMaya as om


def create_loc(pos):
    loc = cmds.spaceLocator()
    cmds.move(pos.x, pos.y, pos.z, loc)


def get_pole_vec_pos(root_pos, mid_pos, end_pos):
    root_joint_vec = om.MVector(root_pos[0], root_pos[1], root_pos[2])
    mid_joint_vec = om.MVector(mid_pos[0], mid_pos[1], mid_pos[2])
    end_joint_vec = om.MVector(end_pos[0], end_pos[1], end_pos[2])

    line = (end_joint_vec - root_joint_vec)
    point = (mid_joint_vec - root_joint_vec)

    scale_value = (line * point) / (line * line)
    proj_vec = line * scale_value + root_joint_vec

    root_to_mid_len = (mid_joint_vec - root_joint_vec).length()
    mid_to_end_len = (end_joint_vec - mid_joint_vec).length()
    total_length = root_to_mid_len + mid_to_end_len

    pole_vec_pos = (mid_joint_vec - proj_vec).normal() * total_length + mid_joint_vec

    create_loc(pole_vec_pos)


sel = cmds.ls(sl=1)

root_joint_pos = cmds.xform(sel[0], q=1, ws=1, t=True)
mid_joint_pos = cmds.xform(sel[1], q=1, ws=1, t=True)
end_joint_pos = cmds.xform(sel[2], q=1, ws=1, t=True)

get_pole_vec_pos(root_joint_pos, mid_joint_pos, end_joint_pos)
