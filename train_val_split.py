import argparse
import os
import random
import glob
import math
import shutil


parser=argparse.ArgumentParser()
parser.add_argument('--dataroot',type=str,default='/eva_data/zchin/datasets',help='data root dir')
parser.add_argument('--ratio',type=float,default=0.2,help='val data ratio')
parser.add_argument('--savedir',type=str,default='/eva_data/zchin/vrdl_hw4_data',help='save split results and test images')
args=parser.parse_args()


if __name__=='__main__':
    all_train_dir=os.path.join(args.savedir,'all_train')
    train_dir=os.path.join(args.savedir,'train')
    val_dir=os.path.join(args.savedir,'val')
    test_dir=os.path.join(args.savedir,'test')
    if not os.path.isdir(args.savedir):
        os.makedirs(args.savedir)
        os.mkdir(all_train_dir)
        os.mkdir(train_dir)
        os.mkdir(val_dir)
        os.mkdir(test_dir)
    
    # train val split
    raw_train_dir=os.path.join(args.dataroot,'training_hr_images/training_hr_images')
    img_list=glob.glob1(raw_train_dir,'*.png')
    # print(img_list)
    data_sz=len(img_list)
    val_sz=math.floor(data_sz*args.ratio)
    idx=random.sample(range(data_sz),val_sz)

    for i,img_name in enumerate(img_list):
        src_path=os.path.join(raw_train_dir,img_name)
        dest_path=os.path.join(all_train_dir,img_name)
        shutil.copyfile(src_path,dest_path)
        if i in idx:
            dest_path=os.path.join(val_dir,img_name)
        else:
            dest_path=os.path.join(train_dir,img_name)
        shutil.copyfile(src_path,dest_path)
    
    all_train_sz=len(glob.glob1(all_train_dir,'*.png'))
    train_sz=len(glob.glob1(train_dir,'*.png'))
    val_sz=len(glob.glob1(val_dir,'*.png'))
    print(f'all train size: {all_train_sz}\ttrain size: {train_sz}\tval size: {val_sz}')
    

    # move testing image
    raw_test_dir=os.path.join(args.dataroot,'testing_lr_images/testing_lr_images')
    for img_name in glob.glob1(raw_test_dir,'*.png'):
        src_path=os.path.join(raw_test_dir,img_name)
        dest_path=os.path.join(test_dir,img_name)
        shutil.copyfile(src_path,dest_path)
    test_sz=len(glob.glob1(test_dir,'*.png'))
    print(f'test size: {test_sz}')