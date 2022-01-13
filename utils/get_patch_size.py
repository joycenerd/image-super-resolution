import argparse
import os
import cv2
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--img-dir', type=str, default='/eva_data/zchin/srfbn_data/train/LR_x3',
                    help='training LR image dir')
args = parser.parse_args()

if __name__ == '__main__':
    sz_list = []
    for img_path in glob.glob(args.img_dir + '/*'):
        im = cv2.imread(img_path)
        h, w, _ = im.shape
        sz_list.extend([h, w])
    print(f'smallest size: {min(sz_list)}')
