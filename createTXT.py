import os
from glob import glob
import fnmatch


def get_things(root_dir):
    things = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, '*.jpg'):
            things.append(os.path.join(root, filename))
    
    return things

if __name__ == '__main__':
    train_folder = './MARS1202/bbox_train/'
    test_folder = './MARS1202/bbox_test/'
    train_pics = get_things(train_folder)
    test_pics = get_things(test_folder)

    train = open("./MARS1202/train_name.txt",'w') 
    for train_pic in train_pics:
        train_pic = os.path.split(train_pic)[1]
        train.write(str(train_pic) + '\n')
    train.close()
    
    test = open("./MARS1202/test_name.txt",'w') 
    for test_pic in test_pics:
        test_pic = os.path.split(test_pic)[1]
        test.write(str(test_pic) + '\n')
    test.close()

    