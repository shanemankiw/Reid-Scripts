import os
import fnmatch
import PIL.Image as Image
import random

in_dir = '/home/amurtiger/191126crop/'
train_folder = '/home/amurtiger/WJHscripts/tigerData20191202/bbox_train/'
test_folder = '/home/amurtiger/WJHscripts/tigerData20191202/bbox_test/'

def start_output(frame_mapping, pic_id, clip_num):
    if frame_mapping == []:
        return
    sorted_mapping = sorted(frame_mapping, key=lambda s: s['key'])
    sorted_mapping = sorted_mapping
    if len(sorted_mapping) < 8:
        length = len(sorted_mapping)
        for i in range(8 - length):
            sorted_mapping.append({'key':0, 'path':sorted_mapping[length - 1]['path']})
    for frame_num, file_dict in enumerate(sorted_mapping):
        file_path = file_dict['path']
        if int(pic_id)%2 == 0:
            if not os.path.exists(os.path.join(train_folder, str(pic_id).zfill(4))):
                os.makedirs(os.path.join(train_folder, str(pic_id).zfill(4)))
            new_pic_name = str(pic_id).zfill(4) + 'C' + str(clip_num%6 + 1) + 'T' + str(clip_num).zfill(4) + 'F' + str(frame_num + 1).zfill(3) + '.jpg'
            target_dir = os.path.join(train_folder, str(pic_id).zfill(4), new_pic_name)
        else:
            if not os.path.exists(os.path.join(test_folder, str(pic_id).zfill(4))):
                os.makedirs(os.path.join(test_folder, str(pic_id).zfill(4)))
            new_pic_name = str(pic_id).zfill(4) + 'C' + str(clip_num%6 + 1) + 'T' + str(clip_num).zfill(4) + 'F' + str(frame_num + 1).zfill(3) + '.jpg'
            target_dir = os.path.join(test_folder, str(pic_id).zfill(4), new_pic_name)
        
        image = Image.open(file_path)
        if image.width > image.height:
            image = image.rotate(90, expand=1)
        image = image.resize((128, 256), Image.BICUBIC)
        image.save(target_dir, quality=95)
        print('Image saved to ' + str(target_dir))
        
        #cmd = 'cp {} {}'.format(file_path, target_dir)


def get_things(root_dir):
    '''
    获取in_dir中所有的图片路径
    '''
    things = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, '*.jpg'):
            things.append(os.path.join(root, filename))
    
    return things

if __name__ == '__main__':
    file_names = sorted(get_things(in_dir))
    frame_num = 1
    clip_num = 0
    id_tmp = 0
    clip_tmp = 'start'
    frame_tmp = 9999
    frame_mapping = []
    for file_path in file_names:
        #traj_tmp = 0
        pic_name = os.path.split(file_path)[1]
        pic_name = os.path.splitext(pic_name)[0]
        pic_id, clip_idx, _ , traj_idx, frame_idx = pic_name.split('_')
        clip_idx = int(clip_idx)
        if len(traj_idx) != 5:
            #traj_idx = int(traj_idx)
            frame_idx = int(frame_idx)
        else:
            frame_idx = int(traj_idx)
        if id_tmp != pic_id:
            start_output(frame_mapping, pic_id, clip_num)
            frame_mapping = []
            
            id_tmp = pic_id
            clip_tmp = clip_idx
            frame_tmp = frame_idx
            clip_num = 1
            frame_num = 1
            
        elif clip_tmp != clip_idx:
            start_output(frame_mapping, pic_id, clip_num)
            frame_mapping = []
            clip_num += 1
            clip_tmp = clip_idx
            frame_tmp = frame_idx
            frame_num = 1
        elif frame_tmp != frame_idx:
            frame_num += 1
            frame_mapping.append({'key':int(frame_idx), 'path':file_path})
            frame_tmp = frame_idx
        
        #subprocess.call(cmd, shell=True)
        #new_pic_name = get_MARS_name(pic_name)
        
