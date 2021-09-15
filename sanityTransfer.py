import glob
import maya.cmds as cmds
import os
import shutil


def make_dir(path):
    """
    input a path to check if it exists, if not, it creates all the path
    :return: path string
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_file_info(*args):
    """"@brief get asset name and texture files from current opened file
    @return asset name (string), textures names (list)
    """
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
    return asset_name, texture_files_reformat, file_path


# get files form transfer folder


# move files to work source image folder

# replace texture path in texture files

# replace 1001 convention to udim

# mod path
mod_path = "W:/transfer/00_mod_publish"
mod_library = "W:/transfer/00_mod_publish"
mod_work = "W:/transfer/00_mod_publish"
# lookdev path
lookdev_path = "W:/transfer/02_lookdev_publish/"
lookdev_library = "W:/transfer/02_lookdev_publish/"
lookdev_work = "W:/transfer/02_lookdev_publish/"
# rig path
rig_path_transfer = "W:/transfer/03_rig_publish/"
rig_path_library = "W:/transfer/03_rig_publish/"
rig_path_work = "W:/transfer/03_rig_publish/"

# stich head work folder

sth_work_path = "T:/SH3D/- Work -/"
sel = cmds.ls(type="aiImage")
print(sel)

asset_name, texture_file_list, file_path = get_file_info()
# create directory on destination folder
if not os.path.exists(lookdev_path + asset_name):
    cmds.sysFile(lookdev_path + asset_name, makeDir=True)
asset_dir = lookdev_path + asset_name

# __________________lookDev______________________________
# move texture files to destination folder used in opened file
for t in texture_file_list:
    shutil.copy(t, asset_dir)
cmds.sysFile(file_path, copy=lookdev_path + asset_name)
for s in sel:
    file_path = cmds.getAttr("{}.{}".format(s, "filename"))
    print("current file path: %s", file_path)
    file_name = os.path.basename(file_path)
    print("file name: %s", file_name)
    raw_name, extension = os.path.splitext(file_name)
    print(raw_name, extension)

# ________________________rig_______________________________

# ________________________mod_______________________________
