'''
for each HCP temps
find the three most matched neonate temps in this lobe
and print the corresponding CCs
figure out which temps of HCP are not matched well with neonates, which means the difference between adults and neonates
'''
import numpy as np
import nibabel as nb
# from skimage.exposure import match_histograms
# from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import seaborn as sns
import copy
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, linkage, optimal_leaf_ordering,leaves_list
from skimage.exposure import match_histograms


lobe='temporal'

hcp_30=open('../matching_neonate_Temps/hcp_temp_only30_'+lobe).read().splitlines()
neo_30=open('../matching_neonate_Temps/neo_temp_only30_'+lobe).read().splitlines()

def corr_similarity(x,y,mask=None):
    # y = match_histograms(y, x)
    if mask is not None:
        x = x[np.where(mask==1)]
        y = y[np.where(mask==1)]

    corr_score = ((x - x.mean()) * (y - y.mean())).mean() / x.std() / y.std()
    # corr_score = ssim(x, y, data_range=y.max() - y.min())
    return corr_score

def DiceFun(x,y,mask=None):
    positive_x = x[x>0]
    positive_y = y[y>0]
    threshold_x = np.quantile(positive_x,0.3)
    threshold_y = np.quantile(positive_y,0.3)

    x1 = copy.deepcopy(x)
    y1 = copy.deepcopy(y)
    x1[x1<threshold_x]=0
    x1[x1>0]=1
    y1[y1<threshold_y]=0
    y1[y1>0]=1

    if mask is not None:
        x1 = x1[np.where(mask == 1)]
        y1 = y1[np.where(mask == 1)]

    intersection = np.sum(x1 * y1)
    if (np.sum(x1) == 0) and (np.sum(y1) == 0):
        return 1
    return (2 * intersection) / (np.sum(x1) + np.sum(y1))

corr_hcp_neo_mtx = np.zeros((30,30))
for i,sub_hcp in enumerate(hcp_30):
    sub_hcp_temp_img = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/final_temp/{lobe}/{sub_hcp}.curv.affine.ico6.shape.gii').darrays[0].data
    lobe_mask = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/lobe_msk/{lobe}/{sub_hcp}_{lobe}_mask.shape.gii').darrays[0].data
    for j,sub_neo in enumerate(neo_30):
        sub_neo_temp_img = nb.load(
            f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/matching_neonate_Temps/{lobe}_lobe/Neo_{sub_neo}.msm_unbiased.HCP_{sub_hcp}.curv.affine.ico6.shape.gii').darrays[
            0].data
        # hcp_matched = match_histograms(sub_hcp_temp_img, sub_neo_temp_img)
        corr_hcp_neo_mtx[i,j]=corr_similarity(sub_hcp_temp_img,sub_neo_temp_img,lobe_mask)


corr_neo_hcp_mtx = corr_hcp_neo_mtx.T

# Perform hierarchical clustering on HCP templates
hcp_distance_matrix = 1 - corr_neo_hcp_mtx  # Convert correlation to distance
linkage_matrix = linkage(hcp_distance_matrix, method='ward')
hcp_order = leaves_list(linkage_matrix)

# Reorder the rows based on hierarchical clustering
reordered_corr_mtx = corr_neo_hcp_mtx[hcp_order, :]

# Apply linear sum assignment to columns to maximize diagonal
row_indices, col_indices = linear_sum_assignment(-reordered_corr_mtx)

# Reorder both rows and columns
reordered_corr_mtx = reordered_corr_mtx[:, col_indices]

# Reorder the labels
reordered_hcp_30 = [hcp_30[i] for i in hcp_order]
reordered_neo_30 = [neo_30[i] for i in col_indices]


# # Define a cost matrix where the cost is the negative of the correlation matrix
# # This turns the problem into a maximization problem
# cost_matrix = -corr_hcp_neo_mtx
#
# # Use linear sum assignment to find the best row-column pairing that maximizes the diagonal
# row_indices, col_indices = linear_sum_assignment(cost_matrix)
#
# # Reorder the matrix according to the optimal assignment
# reordered_corr_mtx = corr_hcp_neo_mtx[np.ix_(row_indices, col_indices)]
#
# # Reorder the labels
# reordered_hcp_30 = [hcp_30[i] for i in row_indices]
# reordered_neo_30 = [neo_30[i] for i in col_indices]



# Create a heatmap of the reordered matrix
# frontal vmin= 0.6,vmax=0.85
# parietal vmin= 0.7, vmax=0.9
# temporal vmin = 0.75, vmax = 0.85
if lobe == 'frontal':
     vmin= 0.65
     vmax=0.9
     # vmin= 0.4
     # vmax=0.9
elif lobe == 'parietal':
    vmin = 0.75
    vmax = 0.90
elif lobe == 'temporal':
    vmin = 0.7
    vmax = 0.85

plt.figure(figsize=(12, 10))
sns.heatmap(
    reordered_corr_mtx,
    cmap=sns.cubehelix_palette(start=.5, rot=-.5, as_cmap=True),#'YlOrBr',  # Choose an appropriate colormap
    xticklabels=reordered_hcp_30,
    yticklabels=reordered_neo_30,
    annot=False,
    cbar_kws={"label": "Correlation Coefficient"},
    linewidths=0.5,  # Add gridlines to separate cells
    linecolor='gray',
    vmin= vmin,
    vmax=vmax
)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title(f'{lobe.capitalize()} lobe: HCP vs Neonates', fontsize=20, pad=20)
plt.xlabel('HCP Templates',fontsize=16)
plt.ylabel('Neonate Templates',fontsize=16)
# Customize the color bar tick labels
cbar = plt.gca().collections[0].colorbar
cbar.ax.tick_params(labelsize=14)
cbar.set_label('Correlation Coefficient', fontsize=16)

# Center the layout
plt.tight_layout()

plt.show()





for i, sub_hcp in enumerate(hcp_30):
    # Get the indices of the top 3 highest correlations for each HCP subject
    top_3_indices = np.argsort(corr_hcp_neo_mtx[i])[-3:][::-1]   #slices the last three elements (i.e., the top three highest values) and reverses the order to descending.
    # Retrieve the corresponding neonatal template names
    top_3_neo_names = [neo_30[idx] for idx in top_3_indices]

    print(f"HCP Subject {sub_hcp}:")
    for idx in top_3_indices:
        neo_name = neo_30[idx]
        correlation_value = corr_hcp_neo_mtx[i, idx]
        print(f"  Neo Subject {neo_name} (Index: {idx}) - Correlation: {correlation_value:.4f}")




# dhcp_ choose closest hcp

for i, sub_neo in enumerate(neo_30):
    # Get the indices of the top 3 highest correlations for each HCP subject
    top_3_indices = np.argsort(corr_neo_hcp_mtx[i])[-3:][::-1]   #slices the last three elements (i.e., the top three highest values) and reverses the order to descending.
    # Retrieve the corresponding neonatal template names
    top_3_neo_names = [hcp_30[idx] for idx in top_3_indices]

    print(f"dHCP Subject {sub_neo}:")
    for idx in top_3_indices:
        neo_name = hcp_30[idx]
        correlation_value = corr_neo_hcp_mtx[i, idx]
        print(f"  HCP Subject {neo_name} (Index: {idx}) - Correlation: {correlation_value:.4f}")



# Additional code to rank HCP subjects based on average CC of top 3 and maximum CC
rankings_avg = []
rankings_max = []

for i, sub_hcp in enumerate(hcp_30):
    # Get the indices of the top 3 highest correlations for each HCP subject
    top_3_indices = np.argsort(corr_hcp_neo_mtx[i])[-3:][::-1]
    top_3_values = corr_hcp_neo_mtx[i, top_3_indices]

    # Calculate average and maximum CC
    avg_cc = np.mean(top_3_values)
    max_cc = np.max(top_3_values)

    # Append to rankings
    rankings_avg.append((sub_hcp, avg_cc))
    rankings_max.append((sub_hcp, max_cc))

# Sort rankings
rankings_avg.sort(key=lambda x: x[1], reverse=True)
rankings_max.sort(key=lambda x: x[1], reverse=True)

# Print rankings
print("\nRanking by Average CC of Top 3:")
for rank, (sub_hcp, avg_cc) in enumerate(rankings_avg, start=1):
    print(f"{rank}: HCP Subject {sub_hcp} - Average CC: {avg_cc:.4f}")

print("\nRanking by Maximum CC:")
for rank, (sub_hcp, max_cc) in enumerate(rankings_max, start=1):
    print(f"{rank}: HCP Subject {sub_hcp} - Maximum CC: {max_cc:.4f}")

print("Ranking analysis completed successfully.")