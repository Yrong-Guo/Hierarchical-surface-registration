"""
Given the hierarchy, pairwise merge until the registration done.
A version for generation grid for registration issue

adapted to new CREATE clusters
"""

import numpy as np
import os
import pandas as pd
import sys
sys.path.append("..")
from workbenchtools_main5 import deform_resample,deform_dedrift_resample,msm_reg#,modify_sphere
from test_deform_global import pairwise_reg_similarity
from find_hierarch import cluster_CC
import nibabel as nib
from DDR_Coarse_STN import bilinearResampleSphereSurfImg, get_latlon_img,get_bi_inter
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre





# threshold for parietal 30: 0.357
# get_clusters_with_thre('../dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl',0.357,size=False)

"""================================Pairwise registration and make dendrogram_'+lobe+'================================"""
'''pairwise registration and similarity matrix'''

# similarity_score = np.load('dendrogram_'+lobe+'/cc_'+lobe+'_'+simi_method+'_affine_mask_mtx.npy')  # if you have saved similarity, load here

# order: test_losses_mse_1, test_losses_gcc_1, test_DICE_1, test_MI_1
test_losses_mse, test_losses_gcc, test_DICE = pairwise_reg_similarity(
    move_root='../Data_files/Subjects_IDs_HCP_moving_LR',target_root='../Data_files/Subjects_IDs_HCP_target_LR')

"""=============================================frontal similarity matrix============================================"""


lobe = 'global'

'''similarity score = gcc'''
similarity_score = test_losses_gcc

# make similarity matrix
size = int((-1 + np.sqrt(1 + 4 * 2 * len(similarity_score))) / 2) + 1
similarity_mtx = np.zeros((size, size))
pair_n = 0
for i in range(size):
    for j in range(i + 1, size):
        similarity_mtx[i, j] = similarity_score[pair_n]
        pair_n += 1
similarity_mtx = similarity_mtx + similarity_mtx.T - np.diag(np.diag(similarity_mtx))
similarity_score = 1- similarity_mtx

np.save('dendrogram_'+lobe+'/cc_'+lobe+'_corr_affine_mask_mtx.npy', similarity_score)   #'''save similarity matrix'''


'''similarity score = mse'''
similarity_score = test_losses_mse

# make similarity matrix
size = int((-1 + np.sqrt(1 + 4 * 2 * len(similarity_score))) / 2) + 1
similarity_mtx = np.zeros((size, size))
pair_n = 0
for i in range(size):
    for j in range(i + 1, size):
        similarity_mtx[i, j] = similarity_score[pair_n]
        pair_n += 1
similarity_mtx = similarity_mtx + similarity_mtx.T - np.diag(np.diag(similarity_mtx))
similarity_score = 1- similarity_mtx

np.save('dendrogram_'+lobe+'/cc_'+lobe+'_mse_affine_mask_mtx.npy', similarity_score)   #'''save similarity matrix'''


'''similarity score=dice'''
similarity_score = test_DICE

# make similarity matrix
size = int((-1 + np.sqrt(1 + 4 * 2 * len(similarity_score))) / 2) + 1
similarity_mtx = np.zeros((size, size))
pair_n = 0
for i in range(size):
    for j in range(i + 1, size):
        similarity_mtx[i, j] = similarity_score[pair_n]
        pair_n += 1
similarity_mtx = similarity_mtx + similarity_mtx.T - np.diag(np.diag(similarity_mtx))
similarity_score = similarity_mtx # dice the higher the more similar

np.save('dendrogram_'+lobe+'/cc_'+lobe+'_dice_affine_mask_mtx.npy', similarity_score)   #'''save similarity matrix'''






