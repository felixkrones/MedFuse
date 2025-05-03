#!/usr/bin/python

# import thread
import time
from PIL import Image
import glob
from tqdm import tqdm
import os
import pandas as pd

print('starting')
data_dir_input = '/data/wolf6245/src/mm_study/data/a_raw/MIMIC/MIMIC-CXR-JPG'
data_dir_output = "/data/wolf6245/src/MedFuse/mimic4extract/data/resized"
os.makedirs(data_dir_output, exist_ok=True)

paths_all = glob.glob(f'{data_dir_input}/files/**/*.jpg', recursive = True)
print('all', len(paths_all))

paths_done = glob.glob(f'{data_dir_output}/**/*.jpg', recursive = True)
print('done', len(paths_done))

# Filter
df_label = pd.read_parquet("/data/wolf6245/src/mm_study/data/f_modelling/03_model_input/data-2024-12-19-01-23-23/(3) Chronic ischaemic heart disease/y_fusion_label_not_gt.parquet")
subjects_to_use = df_label['subject_id'].unique()
paths_all = [p for p in paths_all if int(p.split('/')[11][1:]) in subjects_to_use]
print('filtered', len(paths_all))


done_files = [os.path.basename(path) for path in paths_done]

paths = [path for path in paths_all if os.path.basename(path) not in done_files ]
print('left', len(paths))

def resize_images(path):
    basewidth = 512
    filename = path.split('/')[-1]
    img = Image.open(path)

    wpercent = (basewidth/float(img.size[0]))
    
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize))
    
    img.save(f'{data_dir_output}/{filename}')


from multiprocessing.dummy import Pool as ThreadPool

threads = 10

for i in tqdm(range(0, len(paths), threads)):
    paths_subset = paths[i: i+threads]
    pool = ThreadPool(len(paths_subset))
    pool.map(resize_images, paths_subset)
    pool.close()
    pool.join()
