import pandas as pd

import numpy as np


ehr_data_dir = '/data/wolf6245/src/MedFuse/mimic4extract/data/phenotyping'
split_file = "/data/wolf6245/src/mm_study/data/a_raw/MIMIC/MIMIC-CXR-JPG/cxr_jpg/split.csv.gz"
cxr_data_dir = '/data/wolf6245/src/MedFuse/mimic4extract/data'

cxr_splits = pd.read_csv(split_file)#f'{cxr_data_dir}/mimic-cxr-2.0.0-split.csv')
print(f'before update {cxr_splits.split.value_counts()}')

ehr_split_val = pd.read_csv(f'{ehr_data_dir}/val_listfile.csv')
ehr_split_test = pd.read_csv(f'{ehr_data_dir}/test_listfile.csv')

val_subject_ids = [stay.split('_')[0] for stay in ehr_split_val.stay.values]
test_subject_ids = [stay.split('_')[0] for stay in ehr_split_test.stay.values]


cxr_splits.loc[:, 'split'] = 'train'
cxr_splits.loc[cxr_splits.subject_id.isin(val_subject_ids), 'split'] = 'validate'
cxr_splits.loc[cxr_splits.subject_id.isin(test_subject_ids), 'split'] = 'test'

print(f'after update {cxr_splits.split.value_counts()}')

cxr_splits.to_csv(f'{cxr_data_dir}/mimic-cxr-ehr-split.csv', index=False)

