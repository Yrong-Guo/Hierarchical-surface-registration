import numpy as np
import nibabel as nib
from scipy import stats
import pandas as pd
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
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

temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )
temps_30 = np.setdiff1d(temps_30, exclude_cluster)

cluster_subject = leaf_in_cluster(merge_path)
cluster_left = ['NODE2071','NODE2129','NODE2131','NODE2139','NODE2153','NODE2156','NODE2159','NODE2160','NODE2163','NODE2164','NODE2169','NODE2170','NODE2172','NODE2173','NODE2174','NODE2175','NODE2176','NODE2179','NODE2181','NODE2182','NODE2183']
cluster_right=['NODE2142','NODE2162','NODE2166','NODE2168','NODE2171','NODE2177','NODE2178','NODE2180','NODE2184']

'''
read images and save the surface areas in temporal lobe
'''

cluster_subjects = []
surf_area_temporal = []
surf_area_brain = []
surf_area_temporal_ratio = []
LR_cluster_all = []
# surf_area_stl = []
cluster_id = []
for node in temps_30:
    leaf_id = cluster_subject[node]

    # Rcluster or Lcluster
    if node in cluster_left:
        LR_cluster='left'
    else:
        LR_cluster='right'

    for sub in leaf_id:
        # surface area, mask, curvature-binarised
        surf_area = nib.load('Native_MT_SurfArea/'+sub+'.MT.SurfArea.native.func.gii').darrays[0].data
        temporal_mask = nib.load('native_sts/'+sub+'.temporal.native.shape.gii').darrays[0].data
        brain_mask = nib.load('native_sts/'+sub+'.brain.native.shape.gii').darrays[0].data


        # registration calculate the cortical surface area for this subjects temporal lobe
        surf_area_temporal_sub = np.sum(np.multiply(temporal_mask,surf_area))
        surf_area_brain_sub = np.sum(np.multiply(brain_mask,surf_area))


        cluster_subjects.append(sub)
        surf_area_temporal.append(surf_area_temporal_sub)
        surf_area_brain.append(surf_area_brain_sub)
        surf_area_temporal_ratio.append(surf_area_temporal_sub/surf_area_brain_sub)
        cluster_id.append(node)
        LR_cluster_all.append(LR_cluster)

cluster_subjects = np.asarray(cluster_subjects).reshape(-1,1)
surf_area_temporal = np.asarray(surf_area_temporal).reshape(-1,1)
surf_area_temporal_ratio = np.asarray(surf_area_temporal_ratio).reshape(-1,1)


cluster_id = np.asarray(cluster_id).reshape(-1,1)
LR_cluster_all = np.asarray(LR_cluster_all).reshape(-1,1)
surf_area_temporal_csv = pd.DataFrame(np.concatenate([cluster_id,cluster_subjects,LR_cluster_all,surf_area_temporal,surf_area_temporal_ratio],axis=1),columns=['cluster_id','cluster_subjects','LR_cluster','surf_area_temporal','surf_area_temporal_ratio'])
surf_area_temporal_csv.to_csv('surf_area_temporal_ratio.csv',index=False)




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



'''plot'''


temporal_area_ratio_L = surf_area_temporal[surf_area_temporal['LR_cluster']=='left']
temporal_area_ratio_R = surf_area_temporal[surf_area_temporal['LR_cluster']=='right']
values_L = np.vstack([temporal_area_ratio_L["surf_area_hemi"], temporal_area_ratio_L["surf_area_temporal"]])
values_R = np.vstack([temporal_area_ratio_R["surf_area_hemi"], temporal_area_ratio_R["surf_area_temporal"]])
kernel_L = stats.gaussian_kde(values_L)(values_L)
kernel_R = stats.gaussian_kde(values_R)(values_R)

fig, ax = plt.subplots(figsize=(7, 7))
sns.scatterplot(
    data=temporal_area_ratio_L,
    x="surf_area_hemi",
    y="surf_area_temporal",
    c='red',
    alpha = 0.6,
    ax=ax,
)

sns.scatterplot(
    data=temporal_area_ratio_R,
    x="surf_area_hemi",
    y="surf_area_temporal",
    c='green',
    alpha = 0.6,
    ax=ax,
)
plt.xlim([90000,130000])
plt.ylim([18000,27000])
plt.xlabel('Surface area of the hemisphere')
plt.ylabel('Surface area of temporal lobe')
plt.show()



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


cluster_LR = surf_area_temporal['LR_cluster']
temporal_area_ratio_L = surf_area_temporal[surf_area_temporal['LR_cluster']=='left']['surf_area_temporal_ratio'].values
temporal_area_ratio_R = surf_area_temporal[surf_area_temporal['LR_cluster']=='right']['surf_area_temporal_ratio'].values

# use permutation test to see if subjects surf_area belongs to the left clusters is greater than that belongs to the right clusters
tstat, p_val = ttest_ind(temporal_area_ratio_L,temporal_area_ratio_R,alternative='greater',permutations=100000)

print('p_val = {}'.format(p_val))






'''
plot surf_Area
'''


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


