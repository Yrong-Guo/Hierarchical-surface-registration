'''
For HTconcatetop

temporal lobe myelin asymmetry
using the template
'''


import pandas as pd
import nibabel as nib
import numpy as np
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
import os


'''
initialisation
'''
lobe='temporal'
simi_method = 'corrdice'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'
n_hemi = 2220
num_ver = 40962

work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/'+lobe+'/myelin'
mean_suffix = '.myelin.MSM_HT_top.func.gii'
temporal_mask = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/main5_levelstep/temporal_asymmetry/NODE2218_temporal_mask.shape.gii').darrays[0].data
temporal_indices = np.where(temporal_mask==1)[0]

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


'''
get cluster frequency
'''

merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
### TODO:frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )
temps_30 = np.setdiff1d(temps_30, exclude_cluster)

cluster_subject = leaf_in_cluster(merge_path)

scaler = StandardScaler()

'''
calculate mean std maps of clusters
'''
subject_hcp = open(subject_list).read().splitlines()[:1110]

for sub in subject_hcp:

    sub_img_gifti_L = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/top/'+sub[:6]+'.L.MSMHT_top.transformed_and_reprojected.func.gii')
    # sub_img_gifti_L = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/'+sub[:6]+'.L.MyelinMap_BC.MSMHTtop_ico6.shape.gii')
    myelin_map_L = sub_img_gifti_L.darrays[0].data
    myelin_map_L_temporal = np.multiply(myelin_map_L, temporal_mask)
    myelin_L_temporal_array = myelin_map_L[temporal_indices]
    myelin_L_temporal_zscored = scaler.fit_transform(myelin_L_temporal_array.reshape(-1, 1))

    sub_img_gifti_R = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/top/'+sub[:6]+'.R.MSMHT_top.transformed_and_reprojected.func.gii')
    # sub_img_gifti_R = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/'+sub[:6]+'.R.MyelinMap_BC.MSMHTtop_ico6.shape.gii')
    myelin_map_R = sub_img_gifti_R.darrays[0].data
    myelin_map_R_temporal = np.multiply(myelin_map_R, temporal_mask)
    myelin_R_temporal_array = myelin_map_R[temporal_indices]
    myelin_R_temporal_zscored = scaler.fit_transform(myelin_R_temporal_array.reshape(-1, 1))

    '''calculate the asymmetry indices'''
    init_img = np.zeros(num_ver)
    init_img[temporal_indices] = myelin_L_temporal_zscored.reshape(-1)-myelin_R_temporal_zscored.reshape(-1)
    # init_img = myelin_L_temporal_zscored.reshape(-1)-myelin_R_temporal_zscored.reshape(-1)
    sub_img_gifti_L.darrays[0].data = init_img
    nib.save(sub_img_gifti_L,f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/asymmetry/{sub[:6]}.temporal_curv_asymmind.MSMHTtop_ico6.shape.gii')
    # nib.save(sub_img_gifti_L,f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/{sub[:6]}.MyelinMap_asymmind.MSMHTtop_ico6.shape.gii')

    # '''save images'''
    # init_img = np.zeros(num_ver)
    # init_img[temporal_indices] = myelin_L_temporal_zscored.reshape(-1)
    # sub_img_gifti_L.darrays[0].data = init_img
    # nib.save(sub_img_gifti_L,f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/{sub[:6]}.L.temporal_MyelinMap_zscored.MSMHTtop_ico6.shape.gii')
    #
    # init_img = np.zeros(num_ver)
    # init_img[temporal_indices] = myelin_R_temporal_zscored.reshape(-1)
    # sub_img_gifti_R.darrays[0].data = init_img
    # nib.save(sub_img_gifti_R,f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/{sub[:6]}.R.temporal_MyelinMap_zscored.MSMHTtop_ico6.shape.gii')





    # '''calculate mean and std'''
    # sub_img_gifti = nib.load(work_path+'/'+node+mean_suffix)
    # myelin_clustermean_map = sub_img_gifti.darrays[0].data
    # myelin_clustermean_temporal_map = np.multiply(myelin_clustermean_map,temporal_mask)
    #
    # '''save mean and std'''
    # sub_img_gifti.darrays[0].data = myelin_clustermean_temporal_map
    # nib.save(sub_img_gifti, work_path + '/' + node + '.temporal_myelin.MSM_HT_top.func.gii')
    #
    # # myelin_clustermean_temporal_array = myelin_clustermean_map[temporal_indices]






