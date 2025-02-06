'''
For HTconcate

'''


import pandas as pd
import nibabel as nib
import numpy as np
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
from sklearn.metrics import mean_absolute_error
import os




'''
initialisation
'''
lobe='parietal'
simi_method = 'corrdice'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'
n_hemi = 2220
num_ver = 40962

# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/'+lobe+'/curv'
# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/push_dist'


work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/'+lobe+'/myelin'
# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/'+lobe
# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/'+lobe+'/curv'
# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global_push/curv'
# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/top'

# mean_suffix = 'sulc.MSM_popu_mean.func.gii'
# std_suffix = 'sulc.MSM_popu_std.func.gii'
# mean_suffix = 'sulc.MSM_HT_mean.func.gii'
# std_suffix = 'sulc.MSM_HT_std.func.gii'
mean_suffix = '.myelin.MSM_HT_top.func.gii'

# mean_suffix = '.curv.MSM_HT_mean.func.gii'
# std_suffix = '.curv.MSM_HT_std.func.gii'
# mean_suffix = '.curv.MSM_popu_mean.func.gii'
# std_suffix = '.curv.MSM_popu_std.func.gii'
# mean_suffix = '.curv.MSM_HT_top_mean.func.gii'
# std_suffix = '.curv.MSM_HT_top_std.func.gii'

# check 30 template threshold
if simi_method == 'corrdice':
    if lobe == 'frontal':
        cluster_thre = 0.38
    elif lobe == 'parietal':
        cluster_thre = 0.477
    elif lobe == 'temporal':
        cluster_thre = 0.365

'''
get cluster frequency
'''
merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
### TODO:frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )


cluster_subject = leaf_in_cluster(merge_path)



'''
calculate mean std maps of clusters
'''
sub_img_gifti=None
for node in temps_30:
    leaf_id = cluster_subject[node]
    cnt=0
    for i, sub in enumerate(leaf_id):  # go through every subject in one cluster and count the number of subjects in each cluster
        if i == 0:
            cluster_subject_mtx = np.zeros((len(leaf_id), num_ver))  # initialize the cluster mean and std

        '''HTconcate_temporal_myelin'''
        # not everyone have the myelin map, I would skip them when calculating the main myelin
        if os.path.exists('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/'+sub+'.MyelinMap_BC.MSMHTtop_ico6.shape.gii'):
            sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/'+sub+'.MyelinMap_BC.MSMHTtop_ico6.shape.gii')

            '''MSMHT-parietal-sulc'''
            # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/'+lobe+'/'+sub+'.MSMsulc_HT.'+node+'.transformed_and_reprojected.func.gii')
            '''MSMHT-parietal-curv'''
            # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/'+lobe+'/curv/'+sub+'.MSMsulc_HT.'+node+'.curv.func.gii')
            '''MSM-popu'''
            # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global_push/'+sub+'.MSM_popu.6.transformed_and_reprojected.func.gii')
            # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global_push/curv/'+sub+'.MSM_popu.curv.func.gii')
            '''top, where top is marked by temporal level 3'''
            # os.rename('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/top/temporal3.'+sub+'.MSM.'+node+'.transformed_and_reprojected.func.gii','/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/top/'+sub+'.MSMHT_top.transformed_and_reprojected.func.gii')
            # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/top/'+sub+'.MSMHT_top.transformed_and_reprojected.func.gii')


            sub_img = sub_img_gifti.darrays[0].data
            cluster_subject_mtx[cnt, :] = sub_img
            cnt += 1

        # f.write('-metric /home/yg21/YourongGuo/normativemodel/tfMRI_cluster/cluster_'+node[4:]+'_folder/'+sub+'/MNINonLinear/Results/tfMRI_LANGUAGE/tfMRI_LANGUAGE_hp200_s2_level2_MSMSulchie.feat/GrayordinatesStats/cope2.feat/cope1.dtseries.func.gii ')

    '''calculate mean and std'''
    cluster_template_mean = np.mean(cluster_subject_mtx, axis=0)
    # cluster_template_std = np.std(cluster_subject_mtx, axis=0)


    '''save mean and std'''
    if sub_img_gifti is not None:
        sub_img_gifti.darrays[0].data = cluster_template_mean
        nib.save(sub_img_gifti, work_path+'/'+node+mean_suffix)
        # sub_img_gifti.darrays[0].data = cluster_template_std
        # nib.save(sub_img_gifti, work_path+'/'+node+std_suffix)



    '''for top'''
    # sub_img_gifti.darrays[0].data = cluster_template_mean
    # nib.save(sub_img_gifti, work_path+'/'+lobe+'.'+node+mean_suffix)
    # sub_img_gifti.darrays[0].data = cluster_template_std
    # nib.save(sub_img_gifti, work_path+'/'+lobe+'.'+node+std_suffix)






