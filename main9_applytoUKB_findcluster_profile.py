"""
Given the subjects of UKB, register them to all the templates and calculate the similarity score
find the highest similarity score

Remember:
1. change subject path in DDR_dataloader_2 in utils
2. change aparc path in test_deform in this folder
3. check the get_lobe_2 in utils

the templates are using the sulcal depth in /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/${lobe}/${node}sulc.MSM_HT_mean.func.gii
@ Yourong Guo
"""


import numpy as np
import os
import pandas as pd
import sys
sys.path.append("..")
from workbenchtools_main5 import deform_resample,deform_dedrift_resample,msm_reg#,modify_sphere
from test_deform_profile import pairwise_reg_similarity
from find_hierarch import cluster_CC
import nibabel as nib
from DDR_Coarse_STN import bilinearResampleSphereSurfImg, get_latlon_img,get_bi_inter
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
import pickle



"""================================Pairwise registration and make dendrogram_'+lobe+'================================"""


# order: test_losses_mse_1, test_losses_gcc_1, test_DICE_1, test_MI_1
frontal_scores, parietal_scores, temporal_scores = pairwise_reg_similarity(
    move_root='../Data_files/UKB/temp_mov',target_root='../Data_files/UKB/temp_tar',test_mode=True, continue_run=False,continue_idx=0, profile=False)

