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
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
import matplotlib




lobe = 'temporal'


# get the left rate
temporal_ratio_lr = pd.read_csv('../'+lobe+'_lobe_freq_result_30.csv')
# get the surf area
temporal_surf_area = pd.read_csv('../'+lobe+'_cluster_surfarearatio.csv')
temporal_ratio_lr['temporal_area/hemi_area']=temporal_surf_area['surf_area'].values
surf_area_temporal = pd.read_csv('../surf_area_temporal_ratio.csv')

# save new
# temporal_ratio_lr.to_csv(lobe+'_lobe_result_30.csv',index_label=False)


# sort according to the ratio descending
temporal_ratio_lr_sorted = temporal_ratio_lr.sort_values(by='left_rate',ascending=False)
temporal_ratio_lr_sorted['order'] = np.arange(1,len(temporal_ratio_lr_sorted)+1)


# sort the subject surf area temporal lobe according to that
order=[]
left_rate = []
for i, cluster_sub in enumerate(temporal_ratio_lr_sorted['templates']):
    df_sub = surf_area_temporal['cluster_id'][surf_area_temporal['cluster_id']==cluster_sub].to_frame()
    df_sub['left_rate'] = temporal_ratio_lr_sorted['left_rate'].iloc[i] * np.ones(len(df_sub))
    order.append(df_sub['cluster_id'].index.values)
    left_rate.append(df_sub['left_rate'].to_numpy())

order = np.concatenate(order)
left_rate = np.concatenate(left_rate)
surf_area_temporal_sorted = surf_area_temporal.reindex(order)
surf_area_temporal_sorted['left_rate'] = left_rate











# # plot the clusters against the left temporal lobe surface area

sns.set_theme(style="ticks")

# Initialize the figure with a logarithmic x axis
f, ax = plt.subplots(figsize=(12, 20))
# ax.set_xscale("log")



# Plot the orbital period with horizontal boxes
sns.boxplot(
    surf_area_temporal_sorted, x="surf_area_temporal_ratio", y="cluster_id",hue='left_rate',
    whis=1.5,width=.6, palette="vlag"
)
plt.xlim([0.19,0.225])
# ,hue=temporal_ratio_lr_sorted['left_rate']
# Add in points to show each observation
# sns.stripplot(surf_area_temporal_sorted, x="surf_area_temporal_ratio", y="cluster_id", size=4, color=".3")

# Tweak the visual presentation
ax.xaxis.grid(True)
ax.set(ylabel="")
sns.despine(trim=True, left=True)
plt.show()




# plot the scatter left_ratio and temporal surf area


# values = surf_area_temporal_sorted["surf_area_temporal_ratio"].to_numpy()
# kernel = stats.gaussian_kde(values)(values)
# fig, ax = plt.subplots(figsize=(7, 7))
# sns.scatterplot(
#     data=surf_area_temporal_sorted,
#     x="left_rate",
#     y="surf_area_temporal_ratio",
#     c=kernel,
#     cmap="viridis",
#     ax=ax,
# )
# plt.xlabel('Left hemisphere proportion')
# plt.ylabel('Surface area of temporal lobe')
# plt.show()




sns.set_theme(style="whitegrid")
matplotlib.rcParams.update({'font.size': 22})
g = sns.catplot(
    data=temporal_ratio_lr_sorted, kind="bar",
    x="templates", y="sizes",
    errorbar="sd", alpha=.6, height=6,aspect=4,color='blue'
)
g.set(ylim=(0, 470))
plt.yticks(np.arange(0,400,50))
g.despine(left=True)
g.set_axis_labels("", "Number of subjects")
plt.tick_params(axis='both', which='major', labelsize=10)
plt.xticks(rotation=45)

plt.plot()
plt.show()




# freq_result_significant = np.load('../freq_result_significant.npy')
freq_result_significant = [0,8,9,26,12,28,25,29,4,24,2,3,13]
sns.set_theme(style="whitegrid")
matplotlib.rcParams.update({'font.size': 22})
g = sns.catplot(
    data=temporal_ratio_lr_sorted, kind="bar",
    x="templates", y="left_rate",
    errorbar="sd", alpha=.6, height=6, aspect=4, color='orange', sharey=False
)
g.despine(left=True)
g.set_axis_labels("", "Left hemisphere proportion")
g.set(ylim=(0, 1.2))

l1, = plt.plot(0.5*np.ones(len(temporal_ratio_lr_sorted)), linewidth=2, color='r')  # average
l2 = plt.scatter(freq_result_significant, temporal_ratio_lr_sorted['left_rate'].iloc[freq_result_significant], color='b', marker='*')  # significance

# Get the handles and labels from the bar legend created by Seaborn
bar_handles, bar_labels = g.ax.get_legend_handles_labels()

# Create the custom legend handles and labels
custom_handles = [l1, l2]
custom_labels = ['0.5', 'Significance']

# Combine the handles and labels from both legends
all_handles = bar_handles + custom_handles
all_labels = bar_labels + custom_labels

# Add the combined legend to the plot
g.ax.legend(all_handles, all_labels, loc='upper left')

plt.tick_params(axis='both', which='major', labelsize=10)
plt.xticks(rotation=45)
plt.show()