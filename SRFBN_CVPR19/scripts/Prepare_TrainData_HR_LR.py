# -*- coding: utf-8 -*-
# @Time    : 2019-05-21 19:55
# @Author  : LeeHW
# @File    : Prepare_data.py
# @Software: PyCharm
from glob import glob
from flags import *
import os
from scipy import misc
import numpy as np
import datetime
import imageio
from multiprocessing.dummy import Pool as ThreadPool
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--save-dir', type=str, default='/eva_data/zchin/srfbn_data',
                    help='save directory of images after pre-processing')
parser.add_argument('--dataroot', type=str, default='/eva_data/zchin/vrdl_hw4_data', help='raw hr training images')
parser.add_argument('--mode', type=str, default='train', help='all_train, train or val')
args = parser.parse_args()

starttime = datetime.datetime.now()

if not os.path.isdir(args.save_dir):
    os.makedirs(args.save_dir)
save_HR_path = os.path.join(args.save_dir, args.mode, 'HR_x3')
save_LR_path = os.path.join(args.save_dir, args.mode, 'LR_x3')
os.makedirs(save_HR_path, exist_ok=True)
os.makedirs(save_LR_path, exist_ok=True)

train_HR_dir = os.path.join(args.dataroot, args.mode)
file_list = sorted(glob(os.path.join(train_HR_dir, '*.png')))
# print(file_list)
HR_size = [100, 0.8, 0.7, 0.6, 0.5]


def save_HR_LR(img, size, path, idx):
    HR_img = misc.imresize(img, size, interp='bicubic')
    HR_img = modcrop(HR_img, 3)
    rot180_img = misc.imrotate(HR_img, 180)
    x4_img = misc.imresize(HR_img, 1 / 3, interp='bicubic')
    x4_rot180_img = misc.imresize(rot180_img, 1 / 3, interp='bicubic')

    img_path = path.split('/')[-1].split('.')[0] + '_rot0_' + 'ds' + str(idx) + '.png'
    rot180img_path = path.split('/')[-1].split('.')[0] + '_rot180_' + 'ds' + str(idx) + '.png'
    x4_img_path = path.split('/')[-1].split('.')[0] + '_rot0_' + 'ds' + str(idx) + '.png'
    x4_rot180img_path = path.split('/')[-1].split('.')[0] + '_rot180_' + 'ds' + str(idx) + '.png'

    misc.imsave(save_HR_path + '/' + img_path, HR_img)
    misc.imsave(save_HR_path + '/' + rot180img_path, rot180_img)
    misc.imsave(save_LR_path + '/' + x4_img_path, x4_img)
    misc.imsave(save_LR_path + '/' + x4_rot180img_path, x4_rot180_img)


def modcrop(image, scale=3):
    if len(image.shape) == 3:
        h, w, _ = image.shape
        h = h - np.mod(h, scale)
        w = w - np.mod(w, scale)
        image = image[0:h, 0:w, :]
    else:
        h, w = image.shape
        h = h - np.mod(h, scale)
        w = w - np.mod(w, scale)
        image = image[0:h, 0:w]
    return image


def main(path):
    print('Processing-----{}/0800'.format(path.split('/')[-1].split('.')[0]))
    img = imageio.imread(path)
    idx = 0
    for size in HR_size:
        save_HR_LR(img, size, path, idx)
        idx += 1


items = file_list
pool = ThreadPool()
pool.map(main, items)
pool.close()
pool.join()
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)
