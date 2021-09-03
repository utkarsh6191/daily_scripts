import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import pymel.core as pm


def maya_main_window():
    maya_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class LooKDevDialog(QtWidgets.QDialog):

    def __init__(self, asset_name, texture_list, parent=maya_main_window()):
        super(LooKDevDialog, self).__init__(parent)
        self.asset_name = asset_name
        self.texture_list = texture_list

        self.setWindowTitle("Create constraints")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # input field
        self.name_field = QtWidgets.QLineEdit()
        self.name_field.setMinimumWidth(150)

        self.side_cb = QtWidgets.QComboBox()
        self.side_cb.addItems(["C", "L", "R", "U", "D", "F", "B"])

        self.name_label = QtWidgets.QLabel("Part name")
        self.side_label = QtWidgets.QLabel("Side")
        # buttons
        self.rename_btn = QtWidgets.QPushButton("Rename")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):
        # layout for input field field
        input_field_layout_form = QtWidgets.QGridLayout()
        input_field_layout_form.addWidget(self.name_label, 1, 1)
        input_field_layout_form.addWidget(self.name_field, 1, 2)
        input_field_layout_form.addWidget(self.side_label, 2, 1)
        input_field_layout_form.addWidget(self.side_cb, 2, 2)

        # layout for buttons
        button_layout_hbox = QtWidgets.QHBoxLayout()
        button_layout_hbox.addWidget(self.rename_btn)
        button_layout_hbox.addWidget(self.cancel_btn)

        # arrange layouts
        main_layout = QtWidgets.QFormLayout(self)
        main_layout.addRow("", input_field_layout_form)
        main_layout.addRow("", button_layout_hbox)

    def create_connections(self):
        self.rename_btn.clicked.connect(self.create_node_network)
        self.cancel_btn.clicked.connect(self.close)

    def create_node_network(self):
        # get asset name
        # get texture folder

        # get all the files from folder ending with .exr format
        for content in os.listdir(reform_File_Path):
            if content.endswith('.exr'):
                texture_files.append(content)
        i = 0
        print texture_files

        # texture type
        texture_type = ["DIF", "MTL", "NOR", "OPA", "RGH", "SSS"]
        utility_node_suffixs = ["AIIM", "AICC", "AISF", "SHAD", "RBUM"]

        asset_name = "sunVizor"

        # create ai standard shader
        shader_aistandard = pm.shadingNode("aiStandardSurface", asUtility=True,
                                           n='_'.join([asset_name, "C", "001", utility_node_suffixs[2]]))

        ai_image_node_list = []
        # connect to base color, transmission, subsurface color, subsurface radius
        ai_image_diffuse = pm.shadingNode("aiImage", asUtility=True)
        # connect to metalness
        ai_image_metalness = pm.shadingNode("aiImage", asUtility=True)
        # connect to specular roughness
        ai_image_specular_roughness = pm.shadingNode("aiImage", asUtility=True)
        # connect to transmission
        ai_image_opacity = pm.shadingNode("aiImage", asUtility=True)
        # connect to transmission color
        ai_image_sss = pm.shadingNode("aiImage", asUtility=True)
        # connect to subsurface
        ai_image_normal = pm.shadingNode("aiImage", asUtility=True)

        ai_image_node_list.append(ai_image_diffuse)
        ai_image_node_list.append(ai_image_metalness)
        ai_image_node_list.append(ai_image_normal)
        ai_image_node_list.append(ai_image_opacity)
        ai_image_node_list.append(ai_image_specular_roughness)
        ai_image_node_list.append(ai_image_sss)

        # rename nodes
        i = 0
        for a in ai_image_node_list:
            pm.rename(a, '_'.join([asset_name, texture_type[i], "C", "001", utility_node_suffixs[0]]))
            i = i + 1

        # direct connections
        pm.connectAttr("{}.{}".format(ai_image_metalness, "outColorR"), "{}.{}".format(shader_aistandard, "metalness"),
                       f=1)
        pm.connectAttr("{}.{}".format(ai_image_opacity, "outColorR"), "{}.{}".format(shader_aistandard, "transmission"),
                       f=1)
        pm.connectAttr("{}.{}".format(ai_image_sss, "outColorR"), "{}.{}".format(shader_aistandard, "subsurface"), f=1)

        # correction nodes
        # create color correction node
        # connect to base color
        base_color_correct = pm.shadingNode("aiColorCorrect", asUtility=True,
                                            n='_'.join([asset_name, "C", "001", utility_node_suffixs[1]]))
        # connect to specular roughness
        transmission_color_correct = pm.shadingNode("aiColorCorrect", asUtility=True,
                                                    n='_'.join([asset_name, "C", "002", utility_node_suffixs[1]]))
        # connect to specular roughness
        subssurface_color_correct = pm.shadingNode("aiColorCorrect", asUtility=True,
                                                   n='_'.join([asset_name, "C", "003", utility_node_suffixs[1]]))
        # connect to specular roughness
        specualr_ai_range = pm.shadingNode("aiRange", asUtility=True)
        # connect to normal camera
        normal_bump_2d = pm.shadingNode("bump2d", asUtility=True,
                                        n='_'.join([asset_name, "C", "001", utility_node_suffixs[-1]]))

        # diffuse
        pm.connectAttr("{}.{}".format(ai_image_diffuse, "outColor"),
                       "{}.{}".format(base_color_correct, "input"), f=1)
        pm.connectAttr("{}.{}".format(ai_image_diffuse, "outColor"),
                       "{}.{}".format(transmission_color_correct, "input"), f=1)
        pm.connectAttr("{}.{}".format(ai_image_diffuse, "outColor"),
                       "{}.{}".format(subssurface_color_correct, "input"), f=1)

        pm.connectAttr("{}.{}".format(base_color_correct, "outColor"),
                       "{}.{}".format(shader_aistandard, "baseColor"), f=1)
        pm.connectAttr("{}.{}".format(transmission_color_correct, "outColor"),
                       "{}.{}".format(shader_aistandard, "transmissionColor"), f=1)
        pm.connectAttr("{}.{}".format(subssurface_color_correct, "outColor"),
                       "{}.{}".format(shader_aistandard, "subsurfaceColor"), f=1)
        pm.connectAttr("{}.{}".format(subssurface_color_correct, "outColor"),
                       "{}.{}".format(shader_aistandard, "subsurfaceRadius"), f=1)

        # normal
        pm.connectAttr("{}.{}".format(ai_image_normal, "outColorR"),
                       "{}.{}".format(normal_bump_2d, "bumpValue"), f=1)
        pm.connectAttr("{}.{}".format(normal_bump_2d, "outNormal"),
                       "{}.{}".format(shader_aistandard, "normalCamera"), f=1)

        # specular roughness
        pm.connectAttr("{}.{}".format(ai_image_specular_roughness, "outColor"),
                       "{}.{}".format(specualr_ai_range, "input"), f=1)
        pm.connectAttr("{}.{}".format(specualr_ai_range, "outColorR"),
                       "{}.{}".format(shader_aistandard, "specularRoughness"),
                       f=1)


if __name__ == "__main__":

    try:
        lookdev_dialogue.close()
        lookdev_dialogue.deleteLater()
    except:
        pass
    lookdev_dialogue = LooKDevDialog()
    lookdev_dialogue.show()
