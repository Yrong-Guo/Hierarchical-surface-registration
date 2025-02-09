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
import seaborn as sns
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
import matplotlib
import seaborn.objects as so

'''
initialisation
'''


lobe='frontal'  # ratio only temporal lobe


simi_method = 'corrdice'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'
n_hemi = 2220

subject_all = np.asarray(open(subject_list).read().splitlines())

'''
get cluster frequency
'''
# check 30 template threshold
# exclude very small clusters
if lobe == 'temporal':
    exclude_cluster = np.asarray(['NODE2066', 'NODE2107', 'NODE2119', 'NODE2137', 'NODE2144'])
    cluster_thre = 0.365
elif lobe == 'parietal':
    exclude_cluster = np.asarray(['NODE1856'])
    cluster_thre = 0.477
elif lobe == 'frontal':
    exclude_cluster = np.asarray(['NODE1910', 'NODE2115','NODE2147'])
    cluster_thre = 0.38

merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl' #TODO: change it back to '+lobe+', now is just testing code using frontal lobe
temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )
temps_30 = np.setdiff1d(temps_30, exclude_cluster)


freq_result = []
for lobe in ['frontal','parietal','temporal']:
    freq_result.append(pd.read_csv(lobe+'_lobe_freq_result_30.csv')['left_rate'].to_numpy())


p_vals = []

# compare temporal parietal
stat, p_value_fp = mannwhitneyu(freq_result[2], freq_result[1], alternative='two-sided')
print(f'Temporal vs Parietal: U={stat}, p={p_value_fp}')
p_vals.append(p_value_fp)

# compare temporal frontal
stat, p_value_fp = mannwhitneyu(freq_result[2], freq_result[0], alternative='two-sided')
print(f'Temporal vs Frontal: U={stat}, p={p_value_fp}')
p_vals.append(p_value_fp)

# compare parietal frontal
stat, p_value_fp = mannwhitneyu(freq_result[1], freq_result[0], alternative='two-sided')
print(f'Parietal vs Frontal: U={stat}, p={p_value_fp}')
p_vals.append(p_value_fp)

_, p_adjusted, _, _ = multipletests(p_vals, method='bonferroni')
