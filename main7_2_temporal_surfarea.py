import numpy as np
import nibabel as nib
from scipy import stats
import pandas as pd
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
from sklearn.metrics import mean_absolute_error
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chisquare,fisher_exact,ttest_ind
from scipy.stats import gaussian_kde
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
read images and save the surface areas in temporal lobe
'''

# cluster_subjects = []
# surf_area_temporal = []
# surf_area_brain = []
# surf_area_temporal_ratio = []
# LR_cluster_all = []
# # surf_area_stl = []
# cluster_id = []
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
#         # surface area, mask, curvature-binarised
#         surf_area = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/freesurfer_pial/Native_MT_SurfArea/'+sub+'.MT.SurfArea.native.func.gii').darrays[0].data
#         # sts_mask = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/freesurfer_pial/native_sts/'+sub+'.sts.native.shape.gii').darrays[0].data
#         temporal_mask = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/native_sts/'+sub+'.temporal.native.shape.gii').darrays[0].data
#         brain_mask = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/native_sts/'+sub+'.brain.native.shape.gii').darrays[0].data
#         # stl_mask = nib.load('/home/yg21/YourongGuo/normativemodel/HCP_1200/native_sts/'+sub+'.stl.native.shape.gii').darrays[0].data
#
#         # curvature = nib.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/HCP_native/native_curve/'+sub+'.curvature.native.shape.gii').darrays[0].data
#
#
#         # registration calculate the cortical surface area for this subjects temporal lobe
#         surf_area_temporal_sub = np.sum(np.multiply(temporal_mask,surf_area))
#         surf_area_brain_sub = np.sum(np.multiply(brain_mask,surf_area))
#         # surf_area_stl_sub = np.sum(np.multiply(stl_mask,surf_area))
#
#         cluster_subjects.append(sub)
#         surf_area_temporal.append(surf_area_temporal_sub)
#         surf_area_brain.append(surf_area_brain_sub)
#         surf_area_temporal_ratio.append(surf_area_temporal_sub/surf_area_brain_sub)
#         # surf_area_stl.append(surf_area_stl_sub)
#         cluster_id.append(node)
#         LR_cluster_all.append(LR_cluster)
#
# cluster_subjects = np.asarray(cluster_subjects).reshape(-1,1)
# surf_area_temporal = np.asarray(surf_area_temporal).reshape(-1,1)
# surf_area_temporal_ratio = np.asarray(surf_area_temporal_ratio).reshape(-1,1)
#
# # surf_area_stl = np.asarray(surf_area_stl).reshape(-1,1)
#
# cluster_id = np.asarray(cluster_id).reshape(-1,1)
# LR_cluster_all = np.asarray(LR_cluster_all).reshape(-1,1)
# surf_area_temporal_csv = pd.DataFrame(np.concatenate([cluster_id,cluster_subjects,LR_cluster_all,surf_area_temporal,surf_area_temporal_ratio],axis=1),columns=['cluster_id','cluster_subjects','LR_cluster','surf_area_temporal','surf_area_temporal_ratio'])
# surf_area_temporal_csv.to_csv('surf_area_temporal_ratio.csv',index=False)
#     # stat, p_val = scipy.stats.ttest_ind(gyral_ratio_all[0:1110],gyral_ratio_all[1110:],alternative='greater')
#







'''
proof temporal area with respect to brain area
'''
sns.set_theme(style="whitegrid")
surf_area_temporal = pd.read_csv('surf_area_temporal_ratio.csv')
surf_area_temporal['surf_area_hemi'] = (surf_area_temporal['surf_area_temporal']/surf_area_temporal['surf_area_temporal_ratio']).to_numpy().reshape(-1,1)

values = np.vstack([surf_area_temporal["surf_area_hemi"], surf_area_temporal["surf_area_temporal"]])
kernel = stats.gaussian_kde(values)(values)

surf_area_temporal["surf_area_hemi"] = surf_area_temporal["surf_area_hemi"]/100
surf_area_temporal["surf_area_temporal"] = surf_area_temporal["surf_area_temporal"]/100

fig, ax = plt.subplots(figsize=(10, 10))
sns.scatterplot(
    data=surf_area_temporal,
    x="surf_area_hemi",
    y="surf_area_temporal",
    c=kernel,
    cmap="mako",
    ax=ax,
)
sns.regplot(data=surf_area_temporal, x="surf_area_hemi", y="surf_area_temporal",
    scatter=False, truncate=False, order=1, color=".2",)

ax.grid(False)
plt.xlabel('Surface area of the hemisphere (cm²)', fontsize=16)
plt.ylabel('Surface area of temporal lobe (cm²)', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()






# temporal_area_ratio_L = surf_area_temporal[surf_area_temporal['LR_cluster']=='left']
# temporal_area_ratio_R = surf_area_temporal[surf_area_temporal['LR_cluster']=='right']
# values_L = np.vstack([temporal_area_ratio_L["surf_area_hemi"], temporal_area_ratio_L["surf_area_temporal"]])
# values_R = np.vstack([temporal_area_ratio_R["surf_area_hemi"], temporal_area_ratio_R["surf_area_temporal"]])
# kernel_L = stats.gaussian_kde(values_L)(values_L)
# kernel_R = stats.gaussian_kde(values_R)(values_R)
#
# fig, ax = plt.subplots(figsize=(7, 7))
# sns.scatterplot(
#     data=temporal_area_ratio_L,
#     x="surf_area_hemi",
#     y="surf_area_temporal",
#     c='red',
#     alpha = 0.6,
#     ax=ax,
# )
#
# sns.scatterplot(
#     data=temporal_area_ratio_R,
#     x="surf_area_hemi",
#     y="surf_area_temporal",
#     c='green',
#     alpha = 0.6,
#     ax=ax,
# )
# plt.xlim([90000,130000])
# plt.ylim([18000,27000])
# plt.xlabel('Surface area of the hemisphere')
# plt.ylabel('Surface area of temporal lobe')
# plt.show()


'''
statistical analysis
'''
# create cluster - areasurf ratio
surf_area_temporal = pd.read_csv('surf_area_temporal_ratio.csv')
surf_area_clusters = []
cnt=0
for i, node in enumerate(temps_30):
    leaf_id = cluster_subject[node]
    surf_area_cluster = []
    for sub in leaf_id:
        surf_area_cluster.append(surf_area_temporal['surf_area_temporal_ratio'].iloc[cnt])
        cnt+=1

    surf_area_clusters.append(np.mean(surf_area_cluster))

# make a df for template - mean area
temps_30 = np.asarray(temps_30).reshape(-1,1)
surf_area_clusters = np.asarray(surf_area_clusters).reshape(-1,1)
cluster_area_df = pd.DataFrame(np.concatenate([temps_30,surf_area_clusters],axis=1),columns=['templates','surf_area'])
cluster_area_df['surf_area'] = cluster_area_df['surf_area'].astype('float64')
cluster_area_df.to_csv(lobe+'_cluster_surfarearatio.csv',index_label=False)

# belongs to L/R clusters, does it have anything to do with temporal lobe surface area ratio?

cluster_LR = surf_area_temporal['LR_cluster']
temporal_area_ratio_L = surf_area_temporal[surf_area_temporal['LR_cluster']=='left']['surf_area_temporal_ratio'].values
temporal_area_ratio_R = surf_area_temporal[surf_area_temporal['LR_cluster']=='right']['surf_area_temporal_ratio'].values

# use permutation test to see if subjects surf_area belongs to the left clusters is greater than that belongs to the right clusters
tstat, p_val = ttest_ind(temporal_area_ratio_L,temporal_area_ratio_R,alternative='greater',permutations=100000)

print('p_val = {}'.format(p_val))






'''
plot surf_Area
'''


# freq_result_all = pd.read_csv(lobe+'_lobe_freq_result.csv')
# freq_result = freq_result_all[freq_result_all['templates'].isin(temps_30.reshape(-1))]
# significantfreq = [0, 3, 5, 9, 11, 12, 13, 23, 24, 25, 26, 27, 28]
#
# clrs = ['grey' if (x < 0.5) else 'red' for x in freq_result['left_rate'].values ]
#
# surf_area_temporal[surf_area_temporal['LR_cluster']=='right']
# g = sns.catplot(
#     data=cluster_area_df, kind="bar",
#     x="templates", y="surf_area",
#     errorbar="sd", alpha=.6, height=6,aspect=4,color='blue',palette=clrs
# )
# l2 = plt.scatter(significantfreq, cluster_area_df['surf_area'].iloc[significantfreq], color='b', marker='*')  # significance
#
# g.set(ylim=(0.1, 0.3))
# g.despine(left=True)
# g.set_axis_labels("", "Mean surface area")
#
# plt.tick_params(axis='both', which='major', labelsize=7)
# plt.plot()
# plt.show()


# sns.set(rc={'figure.figsize':(17,8)})
# sns.set(font_scale=0.7)
# sns.set_theme(style="whitegrid")
# ax=sns.boxplot(data=surf_area_temporal,
#                x="cluster_id", y="surf_area_temporal_ratio",palette=clrs,gap=0.5)
# plt.show()



surf_area_temporal_Left = surf_area_temporal[surf_area_temporal['LR_cluster']=='left']
surf_area_temporal_Right = surf_area_temporal[surf_area_temporal['LR_cluster']=='right']

density_l=gaussian_kde(surf_area_temporal_Left["surf_area_temporal_ratio"].to_numpy())
density_r=gaussian_kde(surf_area_temporal_Right["surf_area_temporal_ratio"].to_numpy())


sns.set_theme(style="whitegrid")
fig,ax = plt.subplots(figsize=(9,10))

# sns.boxplot(data=surf_area_temporal,
#                x="LR_cluster", y="surf_area_temporal_ratio",gap=0.5, color = 'Darkseagreen')
surf_area_temporal['group']=np.ones(len(surf_area_temporal))
sns.violinplot(data=surf_area_temporal,
               x="group", y="surf_area_temporal_ratio", hue='LR_cluster', inner='quart', cut=1, linewidth=2, palette="Set3",split=True)
ax.grid(False)
ax.legend(title="")

plt.xlabel('Cluster bias', fontsize=16)
ax.set_xticks([])
plt.ylabel('Proportion of temporal lobe surface area', fontsize=16)

plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()



# ,bw_adjust=.5

# Overlay a scatter plot
# cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
#
# sns.stripplot(data=surf_area_temporal_Left,
#                 x="LR_cluster", y="surf_area_temporal_ratio",
#                 hue=density_l(surf_area_temporal_Left["surf_area_temporal_ratio"])*100, palette='crest',
#                 alpha=0.1, legend=False,jitter=0.1,size=15,marker="D")
# sns.stripplot(data=surf_area_temporal_Right,
#                 x="LR_cluster", y="surf_area_temporal_ratio",
#                 hue=density_r(surf_area_temporal_Right["surf_area_temporal_ratio"])*100, palette='crest',
#                  alpha=0.1, legend=False,jitter=0.1,size=15,marker="D")





'''
box plot  temporary 
'''

# sign_temps = temps_30[significantfreq].reshape(-1)
#
# surf_area_temporal_sig = surf_area_temporal[surf_area_temporal['cluster_id'].isin(sign_temps)]
# # clrs=['red','red','red','grey','red','grey','grey','grey','red','grey','red','red','red']
# # clrs=['red','red','red','red','red','red','red','red','grey','grey','grey','grey','grey']
# clrs=['red'] * 8+ ['gray']*5
# order = ['NODE2071','NODE2139','NODE2153','NODE2164','NODE2179','NODE2181','NODE2182','NODE2183','NODE2162','NODE2166','NODE2168','NODE2178','NODE2180']
# sns.set(rc={'figure.figsize':(17,8)})
# sns.set(font_scale=0.7)
# sns.set_theme(style="whitegrid")
# ax=sns.boxplot(data=surf_area_temporal_sig, order=order,
#                x="cluster_id", y="surf_area_temporal_ratio",palette=clrs,gap=0.5)
# plt.show()
#



