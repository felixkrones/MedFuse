CUDA_VISIBLE_DEVICES=0 CUDA_LAUNCH_BLOCKING=1 python fusion_main.py \
--dim 256 --dropout 0.3 --layers 2 \
--vision-backbone resnet34 \
--mode train \
--epochs 30 --batch_size 16 --lr 0.00007 \
--vision_num_classes 14 --num_classes 6 \
--data_pairs paired_ehr_cxr \
--fusion_type lstm \
--load_state_cxr checkpoints/cxr_rad_full/best_checkpoint.pth.tar \
--load_state_ehr checkpoints/felix/phenotyping/uni_ehr_full/best_checkpoint.pth.tar \
--save_dir checkpoints/felix/phenotyping/medFuse/fold_1 \
--ehr_data_dir mimic4extract/data/folds/fold_1 \
--cxr_data_dir mimic4extract/data/folds/fold_1 \
--image_split_file mimic4extract/data/folds/fold_1/mimic-cxr-ehr-split.csv


CUDA_VISIBLE_DEVICES=0 CUDA_LAUNCH_BLOCKING=1 python fusion_main.py \
--dim 256 --dropout 0.3 --layers 2 \
--vision-backbone resnet34 \
--mode train \
--epochs 30 --batch_size 16 --lr 0.00007 \
--vision_num_classes 14 --num_classes 6 \
--data_pairs paired_ehr_cxr \
--fusion_type lstm \
--load_state_cxr checkpoints/cxr_rad_full/best_checkpoint.pth.tar \
--load_state_ehr checkpoints/felix/phenotyping/uni_ehr_full/best_checkpoint.pth.tar \
--save_dir checkpoints/felix/phenotyping/medFuse/fold_2 \
--ehr_data_dir mimic4extract/data/folds/fold_2 \
--cxr_data_dir mimic4extract/data/folds/fold_2 \
--image_split_file mimic4extract/data/folds/fold_2/mimic-cxr-ehr-split.csv


CUDA_VISIBLE_DEVICES=0 CUDA_LAUNCH_BLOCKING=1 python fusion_main.py \
--dim 256 --dropout 0.3 --layers 2 \
--vision-backbone resnet34 \
--mode train \
--epochs 30 --batch_size 16 --lr 0.00007 \
--vision_num_classes 14 --num_classes 6 \
--data_pairs paired_ehr_cxr \
--fusion_type lstm \
--load_state_cxr checkpoints/cxr_rad_full/best_checkpoint.pth.tar \
--load_state_ehr checkpoints/felix/phenotyping/uni_ehr_full/best_checkpoint.pth.tar \
--save_dir checkpoints/felix/phenotyping/medFuse/fold_3 \
--ehr_data_dir mimic4extract/data/folds/fold_3 \
--cxr_data_dir mimic4extract/data/folds/fold_3 \
--image_split_file mimic4extract/data/folds/fold_3/mimic-cxr-ehr-split.csv



CUDA_VISIBLE_DEVICES=0 CUDA_LAUNCH_BLOCKING=1 python fusion_main.py \
--dim 256 --dropout 0.3 --layers 2 \
--vision-backbone resnet34 \
--mode train \
--epochs 30 --batch_size 16 --lr 0.00007 \
--vision_num_classes 14 --num_classes 6 \
--data_pairs paired_ehr_cxr \
--fusion_type lstm \
--load_state_cxr checkpoints/cxr_rad_full/best_checkpoint.pth.tar \
--load_state_ehr checkpoints/felix/phenotyping/uni_ehr_full/best_checkpoint.pth.tar \
--save_dir checkpoints/felix/phenotyping/medFuse/fold_4 \
--ehr_data_dir mimic4extract/data/folds/fold_4 \
--cxr_data_dir mimic4extract/data/folds/fold_4 \
--image_split_file mimic4extract/data/folds/fold_4/mimic-cxr-ehr-split.csv