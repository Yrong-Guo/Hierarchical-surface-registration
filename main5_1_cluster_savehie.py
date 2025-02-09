import numpy as np
import os
import pandas as pd
from workbenchtools_main5 import deform_resample,deform_dedrift_resample,msm_reg#,modify_sphere
from test_deform import pairwise_reg_similarity
from find_hierarch import cluster_CC
import nibabel as nib
from DDR_Coarse_STN import bilinearResampleSphereSurfImg, get_latlon_img,get_bi_inter
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
import matplotlib.pyplot as plt


'''----------------------------# load similarity matrix and conduct hierarchical clustering-----------------------------'''
lobe='temporal'
simi_method = 'corrdice'
level = 0
n_hemi = 2220
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'

'''load in 3 similarity matrices'''
similarity_score_corr = np.load('dendrogram_'+lobe+'/cc_'+lobe+'_corr_affine_mask_mtx.npy')
similarity_score_mse = np.load('dendrogram_'+lobe+'/cc_'+lobe+'_mse_affine_mask_mtx.npy')
similarity_score_dice = np.load('dendrogram_'+lobe+'/cc_'+lobe+'_dice_affine_mask_mtx.npy')

'''similarity measurement'''
if simi_method == 'corrmse':
    similarity_score = 0.5 * similarity_score_corr + 0.5 * similarity_score_mse
elif simi_method == 'corrdice':
    similarity_score = 0.5 * similarity_score_corr + 0.5 * similarity_score_dice
else:
    simialrity_score = None
    print('Error! select true simi_method')


cluster_CC(similarity_score,level=level,lobe=lobe,simi_method=simi_method)


'''pairwise merge based on the cc similarity matrix'''

# load the children_distance matrix generated in cluster_CC function
children_distance = np.load('dendrogram_'+lobe+'/children_distance_cc_'+lobe+'_'+simi_method+'_affine_mask_complete_'+str(level)+'.npy',allow_pickle=True)

similarity_score = pd.DataFrame(children_distance, index=None, columns=['sub1', 'sub2', 'distance', 'cluster_size'])

subjects = open('Data_files/Subjects_IDs_HCP_all_LR', "r").read().splitlines()

# save this hierarchical path into the pandas data frame style. This file is important because we need to registration following the hierarchy in it.
for i in range(len(similarity_score)):
    if i==0:
        to_merge = similarity_score.loc[[i]]
        to_merge['subID1'] = np.asarray(subjects)[int(to_merge['sub1'])]
        to_merge['subID2'] = np.asarray(subjects)[int(to_merge['sub2'])]
        new_node_id = str(i).zfill(3)
        to_merge['mergeID'] = 'NODE' + new_node_id

    else:
        to_merge_1 = similarity_score.loc[[i]]
        if int(to_merge_1['sub1'])<n_hemi:
            to_merge_1['subID1'] = np.asarray(subjects)[int(to_merge_1['sub1'])]
        else:
            to_merge_1['subID1'] = 'NODE' + str(int(to_merge_1['sub1'])-n_hemi).zfill(3)
        if int(to_merge_1['sub2'])<n_hemi:
            to_merge_1['subID2'] = np.asarray(subjects)[int(to_merge_1['sub2'])]
        else:
            to_merge_1['subID2'] = 'NODE' + str(int(to_merge_1['sub2'])-n_hemi).zfill(3)
        new_node_id = str(i).zfill(3)
        to_merge_1['mergeID'] = 'NODE' + new_node_id

        to_merge = pd.concat([to_merge, to_merge_1])
merge = to_merge

'''save merge process'''
# pd.to_pickle(merge,'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl') # save merge process to later find representative clusters


"""================================Pairwise registration according to the dendrogram_'+lobe+'================================"""

merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl' #TODO: change it back to '+lobe+', now is just testing code using frontal lobe
get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=0.365,size=True,rt_temp=True) ### frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247

cluster_subject = leaf_in_cluster(merge_path)
