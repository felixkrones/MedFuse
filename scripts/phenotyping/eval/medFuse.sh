CUDA_VISIBLE_DEVICES=0 CUDA_LAUNCH_BLOCKING=1 python fusion_main.py \
--dim 256 --dropout 0.3 --layers 2 \
--vision-backbone resnet34 \
--mode eval \
--epochs 30 --batch_size 16 \
--vision_num_classes 14 --num_classes 6 \
--data_pairs paired_ehr_cxr \
--fusion_type lstm \
--save_dir checkpoints/felix/phenotyping_eval/medFuse \
--load_state checkpoints/felix/phenotyping/medFuse/best_checkpoint.pth.tar