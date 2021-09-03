import glob
import maya.cmds as cmds
import os

# get files form transfer folder


# move files to work source image folder

# replace texture path in texture files

# replace 1001 convetion to udim

sel = cmds.ls(type="aiImage")
print(sel)

for s in sel:
    file_path = cmds.getAttr("{}.{}".format(s, "filename"))
    print file_path
    file_name = os.path.basename(file_path)
    print file_name
    file_name_component = '.'.split(file_name)
    print file_name_component


def get_file_info(*args):
    # get file path
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name, extension = os.path.splitext(filename)

    # get file directory
    dir_name = os.path.dirname(filepath)
    # get subdirectories
    subdir = os.listdir(dir_name)
    # find texture folder
    texture = subdir.index("textures")
    # texture folder path
    texture_path = '/'.join([dir_name, subdir[texture]])

    # subdir in texture folder path
    texture_file_subdir = os.listdir(texture_path)
    # latest texture folder
    texture_file_path = '/'.join([texture_path, texture_file_subdir[-1]])
    # find .exr files
    texture_files = glob.glob('/'.join([texture_file_path, "*.exr"]))
    texture_files_reformat = []
    # reformat name
    for t in texture_files:
        t_new = '/'.join(t.split('\\'))
        texture_files_reformat.append(t_new)

    for t in texture_files_reformat:
        print(t)
    # asset name
    asset_name = '_'.join(filename.split('_')[1:2])
    return asset_name, texture_files_reformat
