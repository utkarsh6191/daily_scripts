import pymel.core as pm

sel = pm.ls(sl=1)
selShape = pm.listRelatives(sel, s=1)
pm.colorEditor()

if pm.colorEditor(query=True, result=True):
    values = pm.colorEditor(query=True, rgb=True)
    for s in sel:
        pm.setAttr("{}.{}".format(s, "overrideEnabled"), 1)
        pm.setAttr("{}.{}".format(s, "overrideRGBColors"), 1)
        pm.setAttr("{}.{}".format(s, "overrideColorRGB"), values)
    for s in selShape:
        pm.setAttr("{}.{}".format(s, "overrideEnabled"), 1)
        pm.setAttr("{}.{}".format(s, "overrideRGBColors"), 1)
        pm.setAttr("{}.{}".format(s, "overrideColorRGB"), values)
        """s.overrideEnabled.set(1)
        s.overrideRGBColors.set(1)
        s.overrideColorRGB.set(values)"""
else:
    print 'Editor was dismissed'
