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
from test_deform import pairwise_reg_similarity
from find_hierarch import cluster_CC
import nibabel as nib
from DDR_Coarse_STN import bilinearResampleSphereSurfImg, get_latlon_img,get_bi_inter
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
import pickle



"""================================Pairwise registration and make dendrogram_'+lobe+'================================"""
'''pairwise registration and similarity matrix'''

# TODO: if need to reload from the break point, restart from a %10=0 number before where it ended
# when everything done, concatenate all the results pickles
# with open('main9_process/simi_score_process.pkl', 'rb') as file:
#     loaded_tuples = pickle.load(file)


# # order: test_losses_mse_1, test_losses_gcc_1, test_DICE_1, test_MI_1
# frontal_scores, parietal_scores, temporal_scores = pairwise_reg_similarity(
#     move_root='../Data_files/UKB/Subjects_IDs_UKB_moving_LR_part',target_root='../Data_files/UKB/Subjects_IDs_HCP_templates_target_part',test_mode=False, continue_run=False,continue_idx=0)



'''================================load partial similarity results and concatenate================================'''
# 0-150870
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/main5_levelstep/main9_process/simi_score_process.pkl', 'rb') as file:
    loaded_tuples_0 = pickle.load(file)
# 150871-405821
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/main5_levelstep/main9_process/simi_score_process_1.pkl', 'rb') as file:
    loaded_tuples_1 = pickle.load(file)
# 0-157999
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp_split/main9_process/main9_process/simi_score_final_part.pkl', 'rb') as file:
    loaded_tuples_2 = pickle.load(file)
# 0-97600
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp_split/main9_process/main9_process/simi_score_process_part1_0.pkl', 'rb') as file:
    loaded_tuples_3 = pickle.load(file)
# 97601-157999
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp_split/main9_process/main9_process/simi_score_final_part1.pkl', 'rb') as file:
    loaded_tuples_4 = pickle.load(file)
# 0-97620
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp_split/main9_process/main9_process/simi_score_process_part2_0.pkl', 'rb') as file:
    loaded_tuples_5 = pickle.load(file)
# 97621-97920
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp_split/main9_process/main9_process/simi_score_process_part2_1.pkl', 'rb') as file:
    loaded_tuples_6 = pickle.load(file)
# 97921-158020
# 975645
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp_split/main9_process/main9_process/simi_score_process_part2.pkl', 'rb') as file:
    loaded_tuples_7 = pickle.load(file)


gcc_ukb_frontal_part0 = np.concatenate((np.asarray(loaded_tuples_0[0][1][0:150871]),
                                        np.asarray(loaded_tuples_1[0][1][0:254951])))


gcc_ukb_frontal = np.concatenate((np.asarray(loaded_tuples_2[0][1][:]),
                                  np.asarray(loaded_tuples_3[0][1][0:97601]),
                                  np.asarray(loaded_tuples_4[0][1][97601:]),
                                  np.asarray(loaded_tuples_5[0][1][0:97621]),
                                  np.asarray(loaded_tuples_6[0][1][97621:97921]),
                                  np.asarray(loaded_tuples_7[0][1][97921:158021])))






