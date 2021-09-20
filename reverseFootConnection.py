import pymel.core as pm

# sel = pm.ls(selection = 1)
ctrl = 'foot_IK_R_001_CTRL'
ball_loc = 'ball_R_001_LOCT'
toe_loc = 'toe_R_001_LOCT'
heel_loc ='heel_R_001_LOCT'

rightHeelRotClamp = pm.shadingNode('clamp', asUtility = True, n=ctrl + 'rightHeelRotClamp')

rightFoot_bendToStraightClamp = pm.shadingNode('clamp', asUtility = True, n=ctrl +'rightFoot_bendToStraightClamp')

rightball_zeroToBendClamp= pm.shadingNode('clamp', asUtility = True, n=ctrl +'rightball_zeroToBendClamp')

rightFoot_bendToStraightPercent = pm.shadingNode('setRange', asUtility = True, n=ctrl +'rightFoot_bendToStraightPercent')

rightBall_zeroToBendPercent = pm.shadingNode('setRange', asUtility = True, n=ctrl +'rightBall_zeroToBendPercent')

rightFoot_invertPercentage  = pm.shadingNode('plusMinusAverage', asUtility = True, n=ctrl +'rightFoot_invertPercentage')

right_ball_percent_mult= pm.shadingNode('multiplyDivide', asUtility = True, n=ctrl +'right_ball_percent_mult')

right_ball_roll_mult = pm.shadingNode('multiplyDivide', asUtility = True, n=ctrl +'right_ball_roll_mult')

l_foot_roll_mult = pm.shadingNode('multiplyDivide', asUtility = True, n=ctrl +'l_foot_roll_mult')

#heel

pm.connectAttr("{}.{}".format(ctrl,'Roll'),rightHeelRotClamp+'.inputR', f=1)
pm.connectAttr(rightHeelRotClamp+'.outputR', heel_loc+'.rotateX', f=1)
pm.setAttr(rightHeelRotClamp+'.minR', -90)

#toe

pm.connectAttr("{}.{}".format(ctrl,'Roll'),rightFoot_bendToStraightClamp+'.inputR', f=1)
pm.connectAttr("{}.{}".format(ctrl,'toeStraightAngle'),rightFoot_bendToStraightClamp+'.maxR', f=1)
pm.connectAttr("{}.{}".format(ctrl,'bendLimitAngle'),rightFoot_bendToStraightClamp+'.minR', f=1)

pm.connectAttr(rightFoot_bendToStraightClamp+'.inputR',rightFoot_bendToStraightPercent+'.valueX', f=1)
pm.connectAttr(rightFoot_bendToStraightClamp+'.maxR',rightFoot_bendToStraightPercent+'.oldMaxX', f=1)
pm.connectAttr(rightFoot_bendToStraightClamp+'.minR',rightFoot_bendToStraightPercent+'.oldMinX', f=1)

pm.connectAttr(rightFoot_bendToStraightPercent+'.outValueX',l_foot_roll_mult+'.input1X', f=1)
pm.connectAttr(rightFoot_bendToStraightClamp+'.inputR',l_foot_roll_mult+'.input2X', f=1)
pm.connectAttr(l_foot_roll_mult+'.outputX',toe_loc+'.rotateX', f=1)
pm.setAttr(rightFoot_bendToStraightPercent+".maxX" ,1)
#ball

pm.setAttr(rightFoot_invertPercentage+".operation", 2)

pm.connectAttr(ctrl+'.Roll',rightball_zeroToBendClamp+'.inputR', f=1)
pm.connectAttr(ctrl+'.bendLimitAngle',rightball_zeroToBendClamp+'.maxR', f=1)
pm.connectAttr(ctrl+'.bendLimitAngle',rightball_zeroToBendClamp+'.maxR', f=1)

pm.connectAttr(rightball_zeroToBendClamp+'.inputR',rightBall_zeroToBendPercent+'.valueX', f=1)
pm.connectAttr(rightball_zeroToBendClamp+'.maxR',rightBall_zeroToBendPercent+'.oldMaxX', f=1)
pm.connectAttr(rightball_zeroToBendClamp+'.minR',rightBall_zeroToBendPercent+'.oldMinX', f=1)

pm.setAttr(rightFoot_invertPercentage+'.input1D[0]',1)
pm.setAttr(rightFoot_invertPercentage+'.input1D[1]',1)
pm.connectAttr(rightFoot_bendToStraightPercent+'.outValueX',rightFoot_invertPercentage+'.input1D[1]', f=1)

pm.connectAttr(rightFoot_invertPercentage+'.output1D',right_ball_percent_mult+'.input1X', f=1)
pm.connectAttr(rightBall_zeroToBendPercent+'.outValueX',right_ball_percent_mult+'.input2X', f=1)


pm.connectAttr(right_ball_percent_mult+'.outputX',right_ball_roll_mult+'.input1X', f=1)
pm.connectAttr(ctrl+'.Roll',right_ball_roll_mult+'.input2X', f=1)

pm.setAttr(rightBall_zeroToBendPercent+".maxX" ,1)

pm.connectAttr(rightHeelRotClamp+'.outputR',heel_loc+'.rotateX', f=1)
pm.connectAttr(l_foot_roll_mult+'.outputX',toe_loc+'.rotateX', f=1)
pm.connectAttr(right_ball_roll_mult+'.outputX',ball_loc+'.rotateX', f=1)

