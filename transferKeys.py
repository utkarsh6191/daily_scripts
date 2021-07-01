import pymel.core as pm

# select the ctrls to copy keys
sel = pm.ls("*CTRL")

# get a list of references
refs = pm.listReferences()

reference_namespaces = []

# get list of namespaces from reference
for ref in refs:
    reference_namespaces.append(ref.namespace)

# get time slider range of the scene
min_timeRange = pm.playbackOptions(q=1, min=1)
max_timeRange = pm.playbackOptions(q=1, max=1)

time_value = "{}:{}".format(min_timeRange, max_timeRange)
float_value = "{}:{}".format(min_timeRange, max_timeRange)

for s in sel:
    if pm.keyframe(s, q=1, tc=1):
        pm.copyKey(s, time=(min_timeRange, max_timeRange), hierarchy="none", controlPoints=0, shape=1)
        for reference_namespace in reference_namespaces:
            if pm.objExists(reference_namespace + ":" + s):
                referenced_ctrl = reference_namespace + ":" + s
                pm.pasteKey(referenced_ctrl, option="replace",
                            time=(min_timeRange, max_timeRange), f=(min_timeRange, max_timeRange), copies=1, connect=0)
    else:
        print("Keys don't exist")
