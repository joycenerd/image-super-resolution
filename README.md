# image-super-resolution
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

### [Report](./docs/REPORT.pdf)

by [Zhi-Yi Chin](https:joycenerd.github.io/)

This repository is implementation of homework4 for IOC5008 Selected Topics in Visual Recognition using Deep Learning course in 2021 fall semester at National Yang Ming Chiao Tung University.

In this homework, we participate in super resolution challenge on [CodaLab](https:codalab.lisn.upsaclay.fr/competitions/622?secret_key=4e06d660-cd84-429c-971b-79d15f78d400). In this challenge, we perform image super resolution on the dataset provided by the TA. There are 291 high-resolution images in the training set. There are 14 low-resolution images, which is generated by performing bicubic and shrinking the original image by 1/3 in the testing set. Also, in this challenge, pretrained model is not allowed. We apply [super-resolution feedback network](https:arxiv.org/pdf/1903.09814.pdf) (SRFBN) to solve this task.


## Getting the code

You can download a copy of all the files in this repository by cloning this repository:

```
git clone https://github.com/joycenerd/image-super-resolution.git
```

## Requirements

You need to have [Anaconda](https:www.anaconda.com/) or Miniconda already installed in your environment. To install requirements:

### 1. Create a conda environment
```
conda create -n srfbn python=3.7
conda activate srfbn
```

### 2. Install Dependencies
```
conda insall scikit-image
conda install pytorch==1.4.0 torchvision==0.5.0 cudatoolkit=10.1 -c pytorch
conda install tqdm
conda install pandas
pip install opencv-python
pip install gdown
pip install scipy==1.2.2
```

## Dataset

You can choose to download the data that we have pre-processed already or you can download the raw data.

### Option#1: Download the data that have been pre-processed
1. Download the data from the Google drive link: [srfbn_data.zip](https://drive.google.com/file/d/1Ro8H_Q0oKF3oju38hHxyt6kXEiOy45Cn/view?usp=sharing)  
2. After decompress the zip file, the data folder structure should look like this:
```
srfbn_data
├── train
│   ├── HR_x3
│   │   ├── 100075_rot0_ds0.png
│   │   ├── 100075_rot0_ds1.png
│   │   ├── ......
│   └── LR_x3
│       ├── 100075_rot0_ds0.png
│       ├── 100075_rot0_ds1.png
│       └── ......
└── val
    ├── HR_x3
    │   ├── 106020_rot0_ds0.png
    │   ├── 106020_rot0_ds1.png
    │   ├── ......
    └── LR_x3
        ├── 106020_rot0_ds0.png
        ├── 106020_rot0_ds1.png
        ├── ......
```

### Option#2: Download the raw data
1. Download the data from the Google drive link: [datasets.zip](https://drive.google.com/file/d/1GL_Rh1N-WjrvF_-YOKOyvq0zrV6TF4hb/view?usp=sharing)
2. After decompress the zip file, the data folder structure should look like this: 
```
datasets
├── testing_lr_images
│   └── testing_lr_images
│       ├── 00.png
│       ├── 01.png
│       └── ......
└── training_hr_images
    └── training_hr_images
        ├── 100075.png
        ├── 100080.png
        └── ......
```

### Data pre-processing

**Note: If you download the data by following option#1 you can skip this step. You still need to download the raw data to access testing data**

If your raw data folder structure is different, you will need to modify [`train_val_split.py`](./train_val_split.py) and [`Prepare_TrainData_HR_LR.py`](./SRFBN_CVPR19/scripts/Prepare_TrainData_HR_LR.py)before executing the code.

#### 1. train valid split
In default we split the whole training set to 80% for training and 20% for validation.
```
python train_val_split.py --dataroot <data_dir>/datasets --ratio 0.2 --savedir <data_dir>/vrdl_hw4_data
```
  * input: the downloaded raw data path
  * output: new data dir name `vrdl_hw4_data`, inside this directory there will be 4 subfolders folders `all_train`, `train`, `val` and `test`

#### 2. Generate LR and HR images for training
Also perform offline data augmentation: scale the image to [0.8,0.7,0.6,0.5] and rotate the image 180 degrees.
```
cd SRFBN_CRPR19/scripts
python Prepare_TrainData_HR_LR.py --save-dir <data_dir>/srfbn_data --dataroot <data_dir>/vrdl_hw4_data --mode <train_or_val>
```
  * input: ouput data path from train valid split
  * output: `srfbn_data/` with 2 subdirectories `train/` and `val/`

## Training

You should have Graphics card to train the model. For your reference, we trained on a single NVIDIA RTX 1080Ti.

### Get LR patch size
Find the smallest size of LR image as the patch size. You can split this step if all your LR images are larger than 60x60.
```
cd utils
python get_patch_size.py --img-dir <data_dir>/srfbn_data/train/LR_x3
```
  * input: training LR image path
  * output: patch size will print on the screen

**Modify LR_size in [`train_SRFBN_custom.json`](SRFBN_CVPR19/options/train/train_SRFBN_custom.json) to the output.**

If you are using our data, then set LR_size to 13. If your LR images are larger than 60x60, you can check the SRFBN paper for the best patch size according to each scale.

### Modify the configuration file
Please modify [`train_SRFBN_custom.json`](SRFBN_CVPR19/options/train/train_SRFBN_custom.json) for your own need according to [`SRFBN_CVPR19/options/train/README.md`](SRFBN_CVPR19/options/train/README.md). You must modify `scale`, `save_dir`(where to save the training results), `dataroot_HR`, `dataroot_LR`, `LR_size`.

If you are training SRFBN-L model, set the following param in `networks`:
* `"num_features": 64`
* `"num_groups": 6`

If you are training SRFBN-S model:
* `"num_features": 32`
* `"num_groups": 3`


### Train the model
```
cd SRFBN_CVPR19
python train.py -opt options/train/train_SRFBN_custom.json
```
  * input: training configuration file
  * output: checkpoints, validation PSNR results, network summary save in `save_dir` you state in the config file

## Validation and Testing

### Modify the configuration file
Please modify [`test_SRFBN_custom.json`](SRFBN_CVPR19/options/test/test_SRFBN_custom.json) for your own need according to [`SRFBN_CVPR19/options/test/README.md`](SRFBN_CVPR19/options/test/README.md). You must modify `scale`, `save_dir`(where to save the predicted SR images) and `pretrained_path`(model you've trained).

Add the following block into `"datasets"` and modify `dataroot_HR` and `dataroot_LR`:

For **validation**:
```json=
"test_set1": {
    "mode": "LRHR",
    "dataroot_HR": "/eva_data/zchin/srfbn_data/val/HR_x3",
    "dataroot_LR": "/eva_data/zchin/srfbn_data/val/LR_x3",
    "data_type": "img"
}
```
For **testing**:
```json=
"test_set1": {
    "mode": "LR",
    "dataroot_LR": "/eva_data/zchin/vrdl_hw4_data/test",
    "data_type": "img"
}
```

### Test the model
```
python test.py -opt options/test/test_SRFBN_custom.json
```
  * input: testing configuration file
  * output: 
    * predicted SR images
    * PSNR/SSIM will print on the screen (only for validation)

## Submit the results
1. `cd` to the folder where the predicted SR images are saved
1. compress the files: `zip -D submission.zip *` 
3. upload the result to CodaLab to get the testing score

## Results and Models
| **model**             | **PSNR (dB)** |**Download**|
|:---------------------:|:-------------:|:----------:|
| SRFBN-S (G=3,m=32)  | 28.1438       |[model](https://drive.google.com/file/d/1L9AYB9V0j2IyuGCmv3YsfiJh4CK55a_1/view?usp=sharing)
| SRFBN-L (G=6,m=64)  | 29.3645       |[model](https://drive.google.com/file/d/1HxE6KOtY4W0iUjUQRyJXCg4Tv44Ga2j0/view?usp=sharing)


## Inference
**Note we use SRFBN-L as our model which yields the best results**

To reproduce our best results, do the following steps:
1. [Getting the code](#getting-the-code)
2. [Install the dependencies](#requirements)
3. [Download the data](#dataset): please download the data by following both **option#1** and **option#2** but you don't need to do data-preprocessing in **option#2**
4. [Download trained model](#results-and-models)
5. [Modify config file](#modify-the-configuration-file) 
6. [Testing](#test-the-model)
8. [Submit the results](#submit-the-results)

## FAQ
If any problem occurs when you are using this project, you can first check out [faq.md](docs/faq.md) to see if there are solutions to your problem.

## GitHub Acknowledgement
We thank the authors of these repositories:
* [Paper99/SRFBN_CVPR19](https://github.com/Paper99/SRFBN_CVPR19)

## Citation
If you find our work useful in your project, please cite:

```bibtex
@misc{
    title = {image-super-resolution},
    author = {Zhi-Yi Chin},
    url = {https:github.com/joycenerd/image-super-resolution},
    year = {2022}
}
```

## Contributing

If you'd like to contribute, or have any suggestions, you can contact us at [joycenerd.cs09@nycu.edu.tw](mailto:joycenerd.cs09@nycu.edu.tw) or open an issue on this GitHub repository.

All contributions welcome! All content in this repository is licensed under the MIT license.
