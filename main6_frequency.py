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
from scipy.stats import chisquare,fisher_exact
import matplotlib
import seaborn.objects as so
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

'''
initialisation
'''


lobe='parietal'  # ratio only temporal lobe
sort_lhr= False

simi_method = 'corrdice'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'
n_hemi = 2220

# gyral_ratio = np.load('/home/yg21/YourongGuo/normativemodel/calculate_GI/gyral_ratio_all.npy')
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

merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )
temps_30 = np.setdiff1d(temps_30, exclude_cluster)



cluster_subject = leaf_in_cluster(merge_path)
cnt_left=[]
cnt_Left_rate = []
cnt_sub_percent = []
cnt_sub_size = []
gyral_ratio_clusters = []

for temp in temps_30:
    cnt_L = 0
    subjects = cluster_subject[temp]

    ratio_cluster = []
    for sub in subjects:
        if '.L' in sub:
            cnt_L+=1
        sub_id = np.where(subject_all == sub)[0][0]

    gyral_ratio_clusters.append(np.mean(ratio_cluster))

    cnt_left.append(cnt_L)
    cnt_Left_rate.append(cnt_L/len(subjects))
    cnt_sub_percent.append(len(subjects)/n_hemi)
    cnt_sub_size.append(len(subjects))




template_info = np.asarray([temps_30, cnt_sub_percent, cnt_sub_size, cnt_Left_rate,cnt_left,gyral_ratio_clusters]).T
freq_result = pd.DataFrame(template_info,columns=['templates', 'frequency','sizes', 'left_rate','left_num','gyral_ratio_sts'])
freq_result['sizes'] = freq_result['sizes'].astype('int')
freq_result['left_num'] = freq_result['left_num'].astype('int')
freq_result['left_rate'] = freq_result['left_rate'].astype('float64')
freq_result['frequency'] = freq_result['frequency'].astype('float64')
freq_result['gyral_ratio_sts'] = freq_result['gyral_ratio_sts'].astype('float64')

freq_result.to_csv(lobe+'_lobe_freq_result_30.csv',index=False)

# sort freq_Result by left rate
# freq_result = freq_result.sort_values(by=['left_rate'])


'''
sort everything with the left hemisphere proportion (this step is for the figures)
'''

if sort_lhr == True:
    freq_result = freq_result.sort_values(by='left_rate',ascending=False)
    freq_result.to_csv(lobe+'_lobe_freq_result_30_sorted.csv',index=False)


'''
mannwhitney U
'''

freq_result = []
for lobe_i in ['frontal','parietal','temporal']:
    freq_result.append(pd.read_csv(lobe_i+'_lobe_freq_result_30.csv')['left_rate'].to_numpy())

p_values = []
# compare temporal parietal
stat, p_value_fp = mannwhitneyu(freq_result[2], freq_result[1], alternative='two-sided')
print(f'Temporal vs Parietal: U={stat}, p={p_value_fp}')
p_values.append(p_value_fp)

# compare temporal frontal
stat, p_value_fp = mannwhitneyu(freq_result[2], freq_result[0], alternative='two-sided')
print(f'Temporal vs Frontal: U={stat}, p={p_value_fp}')
p_values.append(p_value_fp)

# compare parietal frontal
stat, p_value_fp = mannwhitneyu(freq_result[1], freq_result[0], alternative='two-sided')
print(f'Parietal vs Frontal: U={stat}, p={p_value_fp}')
p_values.append(p_value_fp)


_, corrected_p_values, _, _ = multipletests(p_values, method='fdr_bh')

# Print corrected p-values
for i, corrected_p in enumerate(corrected_p_values):
    print(f'Corrected p-value for comparison {i+1}: {corrected_p}')





'''
# plot
'''

'''frequency of the cluster'''
sns.set_theme(style="whitegrid")
matplotlib.rcParams.update({'font.size': 22})
g = sns.catplot(
    data=freq_result, kind="bar",
    x="templates", y="sizes",
    errorbar="sd", alpha=.6, height=6,aspect=4,color='blue'
)
g.set(ylim=(0, 470))
plt.yticks(np.arange(0,400,50))
g.despine(left=True)
g.set_axis_labels("", "Number of subjects")
plt.title(f'Incidence rates for parieto-occipital lobe folding patterns ', fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.xticks(rotation=45)

plt.plot()
plt.show()


'''Left hemisphere proportion'''

sns.set_theme(style="whitegrid")
matplotlib.rcParams.update({'font.size': 22})

g = sns.catplot(
    data=freq_result, kind="bar",
    x="templates", y="left_rate",
    errorbar="sd", alpha=.6, height=6, aspect=4, color='orange', sharey=False)

g.despine(left=True)
g.set_axis_labels("", "Left hemisphere proportion")
g.set(ylim=(0, 1.2))

l1, = plt.plot(0.5*np.ones(len(freq_result)), linewidth=2, color='r')  # average

# Get the handles and labels from the bar legend created by Seaborn
bar_handles, bar_labels = g.ax.get_legend_handles_labels()

# Create the custom legend handles and labels
custom_handles = [l1]
custom_labels = ['0.5', 'Significance']

# Combine the handles and labels from both legends
all_handles = bar_handles + custom_handles
all_labels = bar_labels + custom_labels

# Add the combined legend to the plot
g.ax.legend(all_handles, all_labels, loc='upper left')

plt.tick_params(axis='both', which='major', labelsize=10)
plt.xticks(rotation=45)
plt.show()

















# load
freq_result_frontal = pd.read_csv('frontal_lobe_freq_result_30_sorted.csv')
freq_result_temporal = pd.read_csv('temporal_lobe_freq_result_30_sorted.csv')
freq_result_parietal = pd.read_csv('parietal_lobe_freq_result_30_sorted.csv')
freq_result_significant_frontal = np.load('freq_result_significant_frontal.npy')
freq_result_significant_parietal = np.load('freq_result_significant_parietal.npy')
freq_result_significant_temporal = np.load('freq_result_significant_temporal.npy')

newtemp_order = np.arange(30).reshape(-1,1).astype('str')
Ratio_all = pd.DataFrame(
    np.concatenate((newtemp_order,freq_result_frontal['left_rate'].to_numpy().reshape(-1,1),
                    freq_result_parietal['left_rate'].to_numpy().reshape(-1,1),
                    freq_result_temporal['left_rate'].to_numpy().reshape(-1,1)),axis=1
                   ),
    columns=['temp_id','frontal_left_rate','parietal_left_rate','temporal_left_rate']
)
Ratio_all['temp_id'] = Ratio_all['temp_id'].astype('str')
Ratio_all['frontal_left_rate'] = Ratio_all['frontal_left_rate'].astype('float')
Ratio_all['parietal_left_rate'] = Ratio_all['parietal_left_rate'].astype('float')
Ratio_all['temporal_left_rate'] = Ratio_all['temporal_left_rate'].astype('float')
Ratio_all['Frontal'] = ['Frontal'] *30
Ratio_all['Parietal'] = ['Parietal'] *30
Ratio_all['Temporal'] = ['Temporal'] *30


sns.set_theme(style="whitegrid",font_scale=1.2)
# matplotlib.rcParams.update({'font.size': 30})
# temporal lobe
fig,ax = plt.subplots(3,1, figsize=(12,12),sharey=True)
bar_plot = sns.barplot(
    data=Ratio_all,
    x="temp_id", y="temporal_left_rate", alpha = 0.7, color= 'gold',ax=ax[0], label='Temporal')

line_plot, = ax[0].plot(np.linspace(-0.5,29.5,30),0.5*np.ones(len(freq_result_frontal)), linewidth=2, color='r',label='0.5')  # average

l_frontal= sns.lineplot(data=Ratio_all,
    x="temp_id", y="frontal_left_rate", alpha = 1, color= 'cadetblue',ax=ax[0], label='Frontal', linewidth=2.5)

l_parietal= sns.lineplot(data=Ratio_all,
    x="temp_id", y="parietal_left_rate", alpha = 1, color= 'Darkseagreen',ax=ax[0], label='Parietal', linewidth=2.5)


# signif_dot = ax[0].plot(freq_result_significant_temporal.reshape(-1),
#                         freq_result_temporal['left_rate'].iloc[freq_result_significant_temporal[0]].to_numpy(),
#                         color='cornflowerblue',
#                         marker='*',
#                         linestyle = '',
#                         label='Significance')  # significance
ax[0].legend(loc='upper right')

ax[0].set_xlabel('')
ax[0].set_ylabel('')
ax[0].set_ylim([0, 1.2])



# frontal lobe

bar_plot1 = sns.barplot(
    data=Ratio_all,
    x="temp_id", y="frontal_left_rate", alpha = 0.7, color= 'cadetblue',ax=ax[1], label='Frontal')

line_plot1, = ax[1].plot(np.linspace(-0.5,29.5,30),0.5*np.ones(len(freq_result_frontal)), linewidth=2, color='r',label='0.5')  # average

l_temporal= sns.lineplot(data=Ratio_all,
    x="temp_id", y="temporal_left_rate", alpha = 1, color= 'gold',ax=ax[1], label='Temporal', linewidth=2.5)

l_parietal= sns.lineplot(data=Ratio_all,
    x="temp_id", y="parietal_left_rate", alpha = 1, color= 'Darkseagreen',ax=ax[1], label='Parietal', linewidth=2.5)

# signif_dot1 = ax[1].plot(freq_result_significant_frontal.reshape(-1),
#                          freq_result_frontal['left_rate'].iloc[freq_result_significant_frontal[0]].to_numpy(),
#                          color='cornflowerblue',
#                          marker='*',
#                          linestyle = '',
#                          label='Significance')  # significance
ax[1].legend(loc='upper right')


ax[1].set_xlabel('')
ax[1].set_ylabel('')
ax[1].set_ylim([0, 1.2])


# parietal lobe

bar_plot2 = sns.barplot(
    data=Ratio_all,
    x="temp_id", y="parietal_left_rate", alpha = 0.7, color= 'Darkseagreen',ax=ax[2], label='Parietal')

line_plot2, = ax[2].plot(np.linspace(-0.5,29.5,30),0.5*np.ones(len(freq_result_parietal)), linewidth=2, color='r',label='0.5')  # average

l_temporal= sns.lineplot(data=Ratio_all,
    x="temp_id", y="temporal_left_rate", alpha = 1, color= 'gold',ax=ax[2], label='Temporal', linewidth=2.5)

l_frontal= sns.lineplot(data=Ratio_all,
    x="temp_id", y="frontal_left_rate", alpha = 1, color= 'cadetblue',ax=ax[2], label='Frontal', linewidth=2.5)

# signif_dot2 = ax[2].plot(freq_result_significant_parietal.reshape(-2),
#                             freq_result_parietal['left_rate'].iloc[freq_result_significant_parietal[0]].to_numpy(),
#                             color='cornflowerblue',
#                             marker='*',
#                             linestyle = '',
#                             label='Significance')  # significance
ax[2].legend(loc='upper right')


ax[2].set_xlabel('')
ax[2].set_ylabel('')
ax[2].set_ylim([0, 1.2])


fig.text(0.04, 0.5, 'Proportion of Left hemisphere', va='center', rotation='vertical',fontsize=20)
# plt.tick_params(axis='both', which='major', labelsize=10)
fig.text(0.5, 0.05, 'Cluster IDs', ha='center', rotation='horizontal',fontsize=20)
fig.text(0.5, 0.94, 'Asymmetry of folding variants', ha='center', va='top', rotation='horizontal',fontsize=22,weight='bold')
# fig.suptitle('Left hemisphere proportion for temporal, frontal, and parietal-occipital lobes', fontsize=18)

plt.show()













