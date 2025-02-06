import numpy as np
import nibabel as nib
import scipy
import pandas as pd
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
from sklearn.metrics import mean_absolute_error
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chisquare,fisher_exact,ttest_ind

'''
initialisation
'''
lobe='temporal'  # this analysis is only done on the temporal lobe, with temporal lobe without the insula mask
simi_method = 'corrdice'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'

# subjects = open(subject_list).read().splitlines()


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
cluster_left = ['NODE2071','NODE2129','NODE2131','NODE2139','NODE2153','NODE2156','NODE2159','NODE2160','NODE2163','NODE2164','NODE2169','NODE2170','NODE2172','NODE2173','NODE2174','NODE2175','NODE2176','NODE2179','NODE2181','NODE2182','NODE2183']
cluster_right=['NODE2142','NODE2162','NODE2166','NODE2168','NODE2171','NODE2177','NODE2178','NODE2180','NODE2184']




'''
hcp parcellation find the hcp_parcellation labels in temporal lobe: labels have more then 50% vertices in the temporal lobe mask are included
'''
# hcp_parcel_list = open('/home/yg21/YourongGuo/normativemodel/HCP_1200/Native_HCP_parcellations/HCP_LR_parcellation').read().splitlines()
# surf_area_temporal = pd.read_csv('surf_area_temporal_ratio.csv')
#
# for node in temps_30:
#     leaf_id = cluster_subject[node]
#
#     # Rcluster or Lcluster
#     if node in cluster_left:
#         LR_cluster='left'
#     else:
#         LR_cluster='right'
#
#     for sub in leaf_id:
#         if sub in hcp_parcel_list:
#             hcp_parcellation = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/Native_HCP_parcellations/'+sub+'.CorticalAreas_dil_NewMLP_Individual.Native.label.gii').darrays[0].data
#             temporal_mask = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/native_sts/'+sub+'.temporal.native.shape.gii').darrays[0].data
#
#             hcp_parcellation_temporal = np.multiply(hcp_parcellation,temporal_mask)
#             hcp_parcellation_temporal_labelind = np.unique(hcp_parcellation_temporal)
#
#             temporal_label_list = []
#             for roi in hcp_parcellation_temporal_labelind:
#                 ver_roi = len(np.where(hcp_parcellation == roi)[0])
#                 ver_roi_temporal = len(np.where(hcp_parcellation_temporal == roi)[0])
#
#                 if ver_roi_temporal/ver_roi > 0.5:
#                     temporal_label_list.append(roi)
#
#             hcp_parcellation_temporal_labelind = np.asarray(temporal_label_list)
#             aaa=np.zeros(len(hcp_parcellation_temporal))
#             aaa[np.in1d(hcp_parcellation,hcp_parcellation_temporal_labelind)]=1
#             img_header = nib.load(
#                 '/home/yg21/YourongGuo/normativemodel/HCP_1200/native_sts/'+sub+'.temporal.native.shape.gii')
#             img_header.darrays[0].data = np.multiply(aaa,hcp_parcellation)
#             nib.save(img_header,'test_label.shape.gii')
#
#
#             np.save('hcp_parcellation_temporal_labelind',hcp_parcellation_temporal_labelind)




'''
hcp parcellation temporal area wise collect values: area surf in cortical areas/ areasurf in the hemisphere MT
cannot normalise by the lobe, the reason why this lobe has larger area might be this area, if normalise this off then cannot explain.
asking question: left bias clusters areas mainly driven by which region of the lobe?
'''
# TODO probably need to normalise using the inflated surface area - because cortical area for different subjects are also different
# hcp_parcel_list = open('/home/yg21/YourongGuo/normativemodel/HCP_1200/Native_HCP_parcellations/HCP_LR_parcellation').read().splitlines()
# # surf_area_temporal = pd.read_csv('surf_area_temporal_ratio.csv')
# hcp_parcellation_temporal_labelind_L = np.load('hcp_parcellation_temporal_labelind.npy')[1:]   #no zero
# hcp_parcellation_temporal_labelind_R = hcp_parcellation_temporal_labelind_L-180
#
#
#
# cluster_subjects = []
# cluster_id = []
# LR_cluster_all = []
# surf_area_cortarea_ratio = []
#
# for node in temps_30:
#     leaf_id = cluster_subject[node]
#
#     # Rcluster or Lcluster
#     if node in cluster_left:
#         LR_cluster='left'
#     else:
#         LR_cluster='right'
#
#     for sub in leaf_id:
#         if sub in hcp_parcel_list:
#             if '.R' in sub:  # if right hemisphere
#                 hcp_parcellation_temporal_labelind  = hcp_parcellation_temporal_labelind_R
#             else:
#                 hcp_parcellation_temporal_labelind = hcp_parcellation_temporal_labelind_L
#
#             # surface area, mask, curvature-binarised
#             surf_area = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/freesurfer_pial/Native_MT_SurfArea/'+sub+'.MT.SurfArea.native.func.gii').darrays[0].data
#             # temporal_mask = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/native_sts/'+sub+'.temporal.native.shape.gii').darrays[0].data
#             brain_mask = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/native_sts/'+sub+'.brain.native.shape.gii').darrays[0].data
#             hcp_parcellation_header = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/Native_HCP_parcellations/'+sub+'.CorticalAreas_dil_NewMLP_Individual.Native.label.gii')
#             hcp_parcellation = hcp_parcellation_header.darrays[0].data
#
#
#             surf_area_brain_sub = np.sum(np.multiply(brain_mask, surf_area))
#             surf_area_cortarea = []
#             for roi in hcp_parcellation_temporal_labelind:
#                 roi_indices = np.where(hcp_parcellation==roi)[0]
#                 surf_area_cortarea_sub = np.sum(surf_area[roi_indices])
#                 surf_area_cortarea.append(surf_area_cortarea_sub)
#             surf_area_cortarea_sub = np.asarray(surf_area_cortarea)
#
#             # collect
#             cluster_subjects.append(sub)
#             surf_area_cortarea_ratio.append(surf_area_cortarea_sub/surf_area_brain_sub)
#             cluster_id.append(node)
#             LR_cluster_all.append(LR_cluster)
#
#
# cluster_subjects = np.asarray(cluster_subjects).reshape(-1,1)
# surf_area_cortarea_ratio = np.asarray(surf_area_cortarea_ratio)
# cluster_id = np.asarray(cluster_id).reshape(-1,1)
# LR_cluster_all = np.asarray(LR_cluster_all).reshape(-1,1)
#
# parcellation_label_list = [hcp_parcellation_header.labeltable.get_labels_as_dict().get(key)[2:] for key in hcp_parcellation_temporal_labelind]
# #np.save('parcellation_label_list',parcellation_label_list)
# surf_area_cortarea_csv = pd.DataFrame(np.concatenate([cluster_id,cluster_subjects,LR_cluster_all,surf_area_cortarea_ratio],axis=1),columns=['cluster_id','cluster_subjects','LR_cluster']+parcellation_label_list)
# surf_area_cortarea_csv.to_csv('surf_area_cortarea_ratio.csv',index=False)




'''
statistical analysis
'''
avearage_parcellation = nib.load('temporal_asymmetry/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.label.gii')
img_header = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/HCP_1200/100206/MNINonLinear/fsaverage_LR32k/100206.L.sulc_MSMAll.32k_fs_LR.shape.gii')

hcp_parcellation_temporal_labelind_L = np.load('hcp_parcellation_temporal_labelind.npy')[1:]   #no zero
# hcp_parcellation_temporal_labelind_R = hcp_parcellation_temporal_labelind_L-180

surf_area_corticalarea = pd.read_csv('surf_area_cortarea_ratio.csv')
parcellation_label_list = np.load('parcellation_label_list.npy')
# belongs to L/R clusters, does it have anything to do with temporal lobe surface area ratio?

data_label = np.zeros(32492)

for i, cortical_Area in enumerate(parcellation_label_list):

    temporal_area_ratio_L = surf_area_corticalarea[surf_area_corticalarea['LR_cluster']=='left'][cortical_Area].values
    temporal_area_ratio_R = surf_area_corticalarea[surf_area_corticalarea['LR_cluster']=='right'][cortical_Area].values
    # use permutation test to see if subjects surf_area belongs to the left clusters is greater than that belongs to the right clusters
    tstat, p_val = ttest_ind(temporal_area_ratio_L,temporal_area_ratio_R,alternative='two-sided')

    print('Area: {}, p_val = {}'.format(cortical_Area,p_val))

    if p_val < (0.05 / len(parcellation_label_list)):
        area_indices = np.where(avearage_parcellation.darrays[0].data == hcp_parcellation_temporal_labelind_L[i])
        if temporal_area_ratio_L.mean() > temporal_area_ratio_R.mean():
            data_label[area_indices]=1
        else:
            data_label[area_indices]=-1

img_header.darrays[0].data = data_label
nib.save(img_header,'temporal_asymmetry/Asymmetry_significant_CorticalAreas.func.gii')


# Area: V8_ROI, p_val = 9.99990000099999e-06
# Area: FFC_ROI, p_val = 1.999980000199998e-05
# Area: A1_ROI, p_val = 0.000919990800091999
# Area: PSL_ROI, p_val = 9.99990000099999e-06
# Area: STV_ROI, p_val = 0.23895761042389577
# Area: 52_ROI, p_val = 9.99990000099999e-06
# Area: RI_ROI, p_val = 9.99990000099999e-06
# Area: TA2_ROI, p_val = 0.011859881401185988
# Area: EC_ROI, p_val = 9.99990000099999e-06
# Area: PreS_ROI, p_val = 9.99990000099999e-06
# Area: PeEc_ROI, p_val = 0.8263817361826382
# Area: STGa_ROI, p_val = 9.99990000099999e-06
# Area: PBelt_ROI, p_val = 9.99990000099999e-06
# Area: A5_ROI, p_val = 9.99990000099999e-06
# Area: PHA1_ROI, p_val = 0.006469935300646994
# Area: PHA3_ROI, p_val = 9.99990000099999e-06
# Area: STSda_ROI, p_val = 9.99990000099999e-06
# Area: STSdp_ROI, p_val = 9.99990000099999e-06
# Area: STSvp_ROI, p_val = 9.99990000099999e-06
# Area: TGd_ROI, p_val = 9.99990000099999e-06
# Area: TE1a_ROI, p_val = 9.99990000099999e-06
# Area: TE1p_ROI, p_val = 0.04199958000419996
# Area: TE2a_ROI, p_val = 0.5683743162568374
# Area: TF_ROI, p_val = 0.2936070639293607
# Area: TE2p_ROI, p_val = 1.999980000199998e-05
# Area: PHT_ROI, p_val = 9.99990000099999e-06
# Area: PH_ROI, p_val = 0.0008999910000899991
# Area: TPOJ1_ROI, p_val = 9.99990000099999e-06
# Area: TPOJ2_ROI, p_val = 9.99990000099999e-06
# Area: VMV3_ROI, p_val = 0.07627923720762793
# Area: PHA2_ROI, p_val = 0.16138838611613884
# Area: FST_ROI, p_val = 0.005529944700552994
# Area: VVC_ROI, p_val = 0.2102278977210228
# Area: TGv_ROI, p_val = 9.99990000099999e-06
# Area: MBelt_ROI, p_val = 9.99990000099999e-06
# Area: LBelt_ROI, p_val = 0.4996050039499605
# Area: A4_ROI, p_val = 0.24693753062469376
# Area: STSva_ROI, p_val = 9.99990000099999e-06
# Area: TE1m_ROI, p_val = 9.99990000099999e-06
# Area: PI_ROI, p_val = 9.99990000099999e-06

