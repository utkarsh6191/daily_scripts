import pymel.core as pm

"""
for geo in myGeos:
    target_shape_orig = pm.listRelatives(geo, s=1)[1]
    pm.transferAttributes('st1_prStoryBook01_mod_mod_base_v008a:' + geo, target_shape_orig, transferPositions=0,
                          transferNormals=0, transferUVs=2, transferColors=0, sampleSpace=5, targetUvSpace="map1",
                          searchMethod=3, flipUVs=0, colorBorders=1)
    pm.delete(target_shape_orig, ch=1)
"""

sel = pm.ls(sl=1)

for s in sel:
    # get joint skinned to the mesh
    bind_joint = pm.listHistory(s, type="joint")
    print bind_joint
    # get skin cluster
    source_skinClstr = pm.listHistory(s, type="skinCluster")[0]
    print source_skinClstr
    # get deformer sets
    s_shape = pm.listRelatives(s, s=1)[-1]
    print s_shape
    # print s_shape
    # deformer_set = pm.listSets(type =2, object = s_shape)[-1]
    # print deformer_set
    # get reference or duplicate mesh
    # s_ref = "st1_prCaravansTajTej01_mod_mod_base_v005:"+ s
    # pm.sets(deformer_set, add = s_ref)
    # bind duplicate mesh to the joints
    destination_skinClstr = pm.skinCluster(bind_joint, s_ref, tsb=True, bm=0, sm=0, nw=1)

    # copy skin weights
    pm.copySkinWeights(ss=source_skinClstr, ds=destination_skinClstr, noMirror=True)
