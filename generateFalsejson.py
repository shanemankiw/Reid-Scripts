import json
import os
import fnmatch
from PIL import Image as Image
from glob import glob
#from pathlib import Path
import shutil

def get_pic_name(srcfile):
    (useless, ext) = os.path.splitext(srcfile)
    (useless, srcname) = os.path.split(useless)
    (useless, clip_name) = os.path.split(useless)
    (useless, identity) = os.path.split(useless)

    if identity == '-1':
        identity = 'noID'

    newName = identity + '_' + clip_name + '_' + srcname + '.jpg'
    return newName


def mycopyfile(srcfile, dstfolder):
    if not os.path.exists(dstfolder):
        os.makedirs(dstfolder)
    #src = Image.open(srcfile)
    newName = get_pic_name(srcfile)
    shutil.copyfile(srcfile, dstfolder + newName)
    #src.save(dstfolder + newName, quality=95, subsampling=0)

    print('saved {} to {}'.format(newName, dstfolder))
   
def outputJson(filelist, dir_folder):
        info = {'images': [], 'categories': []}
        for filename in filelist:
            newName = get_pic_name(str(filename))
            info['images'].append(
            {'file_name': newName, 
            'height': 1080,
            'id': os.path.splitext(newName)[0],
            'width': 1920})
        info['categories'].append({'id': 1, 'name':'tiger'})

        infoData = json.dumps(info, indent=4, separators=(',', ':'))

        #dir_folder = os.path.join(target_dir + '//' + line + '//')
        if not os.path.exists(dir_folder):
            os.makedirs(dir_folder)

        fileout = open(os.path.join(dir_folder, 'reidPics.json'),'w')
        fileout.write(infoData)

def transferImages(filelist, picfolder):
    for filepath in filelist:
        mycopyfile(str(filepath), picfolder)

def get_things(root_dir):
    things = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, '*.jpg'):
            things.append(os.path.join(root, filename))
    
    return things
    


if __name__ == '__main__':


    root_dir = './reIDpics'

    json_dir = './wjhResult'
 
    picfolder = './wjhResult/allPics/'

    filelist = get_things(root_dir)
    
    
    #transferImages(filelist, picfolder)
    outputJson(filelist, json_dir)

