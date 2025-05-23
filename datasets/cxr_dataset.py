import os
import numpy as np
from PIL import Image
import pandas as pd 

import torch
from torch.utils.data import Dataset
# import 
import glob
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import os


class MIMICCXR(Dataset):
    def __init__(self, paths, args, transform=None, split='train'):
        self.data_dir = args.cxr_data_dir
        self.args = args
        self.CLASSES  = ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema',
       'Enlarged Cardiomediastinum', 'Fracture', 'Lung Lesion',
       'Lung Opacity', 'No Finding', 'Pleural Effusion', 'Pleural Other',
       'Pneumonia', 'Pneumothorax', 'Support Devices']
        self.filenames_to_path = {path.split('/')[-1].split('.')[0]: path for path in paths}
        print(f"Found {len(self.filenames_to_path)} images")

        metadata = pd.read_csv(f'/data/wolf6245/src/mm_study/data/a_raw/MIMIC/MIMIC-CXR-JPG/cxr_jpg/metadata.csv.gz')
        labels = pd.read_csv(f'/data/wolf6245/src/mm_study/data/a_raw/MIMIC/MIMIC-CXR-JPG/cxr_jpg/chexpert.csv.gz')
        labels[self.CLASSES] = labels[self.CLASSES].fillna(0)
        labels = labels.replace(-1.0, 0.0)
        
        splits = pd.read_csv(args.image_split_file)


        metadata_with_labels = metadata.merge(labels[self.CLASSES+['study_id'] ], how='inner', on='study_id')


        self.filesnames_to_labels = dict(zip(metadata_with_labels['dicom_id'].values, metadata_with_labels[self.CLASSES].values))
        self.filenames_loaded = splits.loc[splits.split==split]['dicom_id'].values
        self.transform = transform
        self.filenames_loaded = [filename  for filename in self.filenames_loaded if filename in self.filesnames_to_labels]

    def __getitem__(self, index):
        if isinstance(index, str):
            img = Image.open(self.filenames_to_path[index]).convert('RGB')
            labels = torch.tensor(self.filesnames_to_labels[index]).float()

            if self.transform is not None:
                img = self.transform(img)
            return img, labels
        
        filename = self.filenames_loaded[index]
        
        img = Image.open(self.filenames_to_path[filename]).convert('RGB')

        labels = torch.tensor(self.filesnames_to_labels[filename]).float()

        if self.transform is not None:
            img = self.transform(img)
        return img, labels
    
    def __len__(self):
        return len(self.filenames_loaded)


def get_transforms(args):
    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    train_transforms = []
    train_transforms.append(transforms.Resize(256))
    train_transforms.append(transforms.RandomHorizontalFlip())
    train_transforms.append(transforms.RandomAffine(degrees=45, scale=(.85, 1.15), shear=0, translate=(0.15, 0.15)))
    train_transforms.append(transforms.CenterCrop(224))
    train_transforms.append(transforms.ToTensor())
    train_transforms.append(normalize)      


    test_transforms = []
    test_transforms.append(transforms.Resize(args.resize))


    test_transforms.append(transforms.CenterCrop(args.crop))

    test_transforms.append(transforms.ToTensor())
    test_transforms.append(normalize)


    return train_transforms, test_transforms

def get_cxr_datasets(args):
    train_transforms, test_transforms = get_transforms(args)

    data_dir = args.cxr_data_dir
    
    # filepath = f'{args.cxr_data_dir}/paths.npy'
    # if os.path.exists(filepath):
    #     paths = np.load(filepath)
    # else:
    if 'folds' in data_dir:
        data_dir_aux = data_dir.split('folds')[0]
    else:
        data_dir_aux = data_dir
    print(f"Loading data from {data_dir} and images from {data_dir_aux}resized")
    paths = glob.glob(f'{data_dir_aux}/resized/**/*.jpg', recursive = True)
    print(f"Found {len(paths)} images.")
    # np.save(filepath, paths)
    
    dataset_train = MIMICCXR(paths, args, split='train', transform=transforms.Compose(train_transforms))
    dataset_validate = MIMICCXR(paths, args, split='validate', transform=transforms.Compose(test_transforms),)
    dataset_test = MIMICCXR(paths, args, split='test', transform=transforms.Compose(test_transforms),)

    return dataset_train, dataset_validate, dataset_test

