import pandas as pd
import nibabel as nib
import numpy as np
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
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

# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/'+lobe+'/curv'
# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/push_dist'
# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/weighted/'+lobe
# work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/weighted/'
work_path = '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/weighted/curv/'+lobe
mean_suffix = '.curv.MSM_popu_weighted_mean.func.gii'
std_suffix = '.curv.MSM_popu_weighted_std.func.gii'

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

# for node in temps_30:
#     leaf_id = cluster_subject[node]
#
#     for cnt, sub in enumerate(leaf_id):  # go through every subject in one cluster and count the number of subjects in each cluster
#         if cnt == 0:
#             cluster_subject_mtx = np.zeros((len(leaf_id), num_ver))  # initialize the cluster mean and std
#
#         '''# msm global same lambda as HT'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/'+sub+'.MSM_popu.transformed_and_reprojected.func.gii')
#
#         '''# msm global push0.06'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/push_dist/'+sub+'.MSM_popu.6.transformed_and_reprojected.func.gii')
#
#         '''# msmht'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/'+sub+'.MSMsulc_HT.'+node+'.transformed_and_reprojected.func.gii')
#
#         '''# curv_global same lambda as HT'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/curv/'+sub+'.MSM_popu.curv.func.gii')
#
#         '''# curv_global push0.06'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/push_dist/'+sub+'.MSM_popu.curv.func.gii')
#
#         '''# curv_msmht'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/curv/'+sub+'.MSMsulc_HT.'+node+'.curv.func.gii')
#
#         '''# curv_MSMHT_top'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/MSM_HT_top/curv/'+sub+'.frontal.parietal.temporal.MSMHT.shape.gii')
#
#         '''parietal sulc'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/parietal/'+sub+'.MSMsulc_HT.'+node+'.transformed_and_reprojected.func.gii')
#
#         '''parietal curv'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/parietal/curv/'+sub+'.MSMsulc_HT.'+node+'.curv.func.gii')
#
#         '''temporal sulc'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/temporal/'+sub+'.MSMsulc_HT.'+node+'.transformed_and_reprojected.func.gii')
#
#         '''temporal curve'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/temporal/curv/'+sub+'.MSMsulc_HT.'+node+'.curv.func.gii')
#
#         '''# msm global WEIGHTED sulc'''
#         # sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/weighted/' + sub + '.MSM_popu_weig.transformed_and_reprojected.func.gii')
#
#         '''# msm global WEIGHTED curv'''
#         sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/weighted/curv/' + sub + '.MSM_popu_weig.curv.func.gii')
#
#
#         sub_img = sub_img_gifti.darrays[0].data
#         cluster_subject_mtx[cnt, :] = sub_img
#
#         # f.write('-metric /home/yg21/YourongGuo/normativemodel/tfMRI_cluster/cluster_'+node[4:]+'_folder/'+sub+'/MNINonLinear/Results/tfMRI_LANGUAGE/tfMRI_LANGUAGE_hp200_s2_level2_MSMSulchie.feat/GrayordinatesStats/cope2.feat/cope1.dtseries.func.gii ')
#
#     '''calculate mean and std'''
#     cluster_template_mean = np.mean(cluster_subject_mtx, axis=0)
#     cluster_template_std = np.std(cluster_subject_mtx, axis=0)
#
#
#     '''save mean and std'''
#     sub_img_gifti.darrays[0].data = cluster_template_mean
#     nib.save(sub_img_gifti, work_path+'/'+node+mean_suffix)
#     sub_img_gifti.darrays[0].data = cluster_template_std
#     nib.save(sub_img_gifti, work_path+'/'+node+std_suffix)










'''
calculate mean std maps of clusters
'''

for node in temps_30:
    leaf_id = cluster_subject[node]

    for cnt, sub in enumerate(leaf_id):  # go through every subject in one cluster and count the number of subjects in each cluster
        if cnt == 0:
            cluster_subject_mtx = np.zeros((len(leaf_id), num_ver))  # initialize the cluster mean and std

        '''frontal'''
        sub_img_gifti = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/'+lobe+'/'+sub+'.MSMsulc_HT.'+node+'.transformed_and_reprojected.func.gii')


        sub_img = sub_img_gifti.darrays[0].data
        cluster_subject_mtx[cnt, :] = sub_img

        # f.write('-metric /home/yg21/YourongGuo/normativemodel/tfMRI_cluster/cluster_'+node[4:]+'_folder/'+sub+'/MNINonLinear/Results/tfMRI_LANGUAGE/tfMRI_LANGUAGE_hp200_s2_level2_MSMSulchie.feat/GrayordinatesStats/cope2.feat/cope1.dtseries.func.gii ')

    '''calculate mean and std'''
    cluster_template_mean = np.mean(cluster_subject_mtx, axis=0)
    cluster_template_std = np.std(cluster_subject_mtx, axis=0)


    '''save mean and std'''
    sub_img_gifti.darrays[0].data = cluster_template_mean
    nib.save(sub_img_gifti, work_path+'/'+node+mean_suffix)
    sub_img_gifti.darrays[0].data = cluster_template_std
    nib.save(sub_img_gifti, work_path+'/'+node+std_suffix)











'''
calculate gradient for templates
'''
# f = open('analysis_bashcode/template_grad_msmht.sh','w')
#
# for node in temps_30:
#     leaf_id = cluster_subject[node]
#     command_n = 'wb_command -surface-average /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/midthickness/'+node+'.MSM_HT.midthickness.surf.gii'
#     for cnt, sub in enumerate(leaf_id):  # go through every subject in one cluster and count the number of subjects in each cluster
#         if cnt == 0:
#             cluster_subject_mtx = np.zeros((len(leaf_id), num_ver))  # initialize the cluster mean and std
#
#         '''# msm global same lambda as HT'''
#
#         '''# msmht'''
#         command_n = command_n + ' -surf /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/midthickness/midthick_msmht/' + sub + '.rtMSMsulc_HT.' + node + '.midthickness.reg.surf.gii'
#     command_n = command_n+'\n\n'
#     command_n = command_n+'wb_command -metric-gradient /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/midthickness/'+node+'.MSM_HT.midthickness.surf.gii '+work_path+'/'+node+mean_suffix+' /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/'+node+'.MSM_HT.gradient.func.gii\n\n\n\n'
#     f.write(command_n)
#
# f.close()
#
#
# '''popu'''
# f = open('analysis_bashcode/template_grad_msmpopu.sh','w')
#
# for node in temps_30:
#     leaf_id = cluster_subject[node]
#     command_n = 'wb_command -surface-average /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/midthickness/'+node+'.MSM_popu.midthickness.surf.gii'
#     for cnt, sub in enumerate(leaf_id):  # go through every subject in one cluster and count the number of subjects in each cluster
#         if cnt == 0:
#             cluster_subject_mtx = np.zeros((len(leaf_id), num_ver))  # initialize the cluster mean and std
#
#         '''# msm global same lambda as HT'''
#
#         '''# msmht'''
#         command_n = command_n + ' -surf /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/midthickness/midthick_msmpopu/'+sub+'.rtMSM_popu.'+node+'.midthickness.reg.surf.gii'
#     command_n = command_n+'\n\n'
#     command_n = command_n+'wb_command -metric-gradient /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/midthickness/'+node+'.MSM_popu.midthickness.surf.gii /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/'+node+'.MSM_popu_mean.func.gii /home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global/'+node+'.MSM_popu.gradient.func.gii\n\n\n\n'
#     f.write(command_n)
#
# f.close()










'''check-==========================================where does this sub comes from============================================'''
# leaf_id=[100307,107422,111716,113215,127630,128127,149337,151728,153429,159441,163129,172938,181131,201414,205220,298455,361941,377451,436845,441939,500222,601127,613538,687163,702133,759869,802844,814649,861456]
#
# template_list = ['NODE994','NODE1012','NODE1017','NODE1026','NODE1030','NODE1031','NODE1035',
#             'NODE1037','NODE1042','NODE1044','NODE1047','NODE1049','NODE1052','NODE1053',
#             'NODE1058','NODE1060','NODE1061','NODE1062','NODE1063','NODE1064',
#             'NODE1066','NODE1067','NODE1068','NODE1069','NODE1070','NODE1071','NODE1072',
#             'NODE1073','NODE1074','NODE1075']
#
# for node in template_list:
#     for sub in leaf_id:
#         if str(sub) in cluster_leaf_dict[node]:
#             print(node)
