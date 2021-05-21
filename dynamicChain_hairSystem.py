# create dynamic splinIK setup
import pymel.core as pm

# select joint chains
sel = pm.ls(sl=1)

for s in sel:
    # get list of children
    hi = pm.listRelatives(s, ad=1, type="joint")
    hi.reverse()
    print hi
    jnt_pos_list = []

    # get list of joint positions
    for h in hi:
        pos = pm.xform(h, ws=1, q=1, t=1)
        jnt_pos_list.append(pos)
    # create curve along the joints chain
    print jnt_pos_list
    crv = pm.curve(p=jnt_pos_list, d=3, n=str(sel[0]) + "_crv")

    # select curve
    pm.select(crv)
    # create dynamic curve suing hair system
    pm.mel.eval('MakeCurvesDynamic')
    # get list of connections to created curve
    # gives follicle connected to the curve
    foll = pm.listConnections(crv)[0]
    print foll
    # gives follicle shape in the connection
    foll_shape = pm.listRelatives(foll)[0]
    print foll_shape
    # show list of connection, dynamic curve is at the end of the string
    foll_connections = pm.listConnections(foll_shape)
    print foll_connections
    # # get dynamic curve created for splineIK setup
    dyn_crv = foll_connections[-1]

    # create splineIk handle
    ikHdl = pm.ikHandle(n='ikh', sj=str(hi[0]), ee=str(hi[-1]), sol='ikSplineSolver', ccv=False, pcv=False, c=dyn_crv)[
        0]
    pm.rename(ikHdl, str(sel[0]) + "_KHDL")

    # get parent of follice
    foll_parent = pm.listRelatives(foll, p=1)
    print foll_parent

    sel_parent = pm.listRelatives(s, p=1)
    print sel_parent
    pm.parent(foll_parent, sel_parent)

    cube_control = pm.curve(d=1, p=[(1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (1, -1, -1),
                               (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (-1, -1, -1), (-1, -1, 1),
                               (-1, 1, 1), (-1, -1, 1), (1, -1, 1)],
                       k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    pm.rename(cube_control, s+ "_CTRL")
    ctrl_drv_off= pm.group(cube_control,n= s+ "drv_CTRL")
    ctrl_off = pm.group(ctrl_drv_off,n=s + "drv_CTRL")

    pm.delete(pm.parentConstraint(sel_parent,ctrl_off))
    pm.parentConstraint(cube_control,sel_parent)

