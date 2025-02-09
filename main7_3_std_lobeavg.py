import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from scipy.stats import shapiro, ttest_rel, wilcoxon
from get_clusters_with_thre import get_clusters_with_thre
import os

simi_method='corrdice'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'



def load_and_compute_mean(file_path, mask):
    if os.path.exists(file_path):
        data = nb.load(file_path).darrays[0].data
        return np.mean(data[np.where(mask == 1)])
    else:
        print(f"File not found: {file_path}")
        return None

def process_lobe(lobe, exclude_cluster, cluster_thre, simi_method, subject_list):
    merge_path = f'dendrogram_{lobe}/mergeprocess_{lobe}_{simi_method}_affine_mask_complete_0.pkl'
    temps_30 = get_clusters_with_thre(merge_path, subject_list=subject_list, cluster_thre=cluster_thre, size=True, rt_temp=True)
    temps_30 = np.setdiff1d(temps_30, exclude_cluster)

    std_temp = []
    for temp in temps_30:
        msmht_std = load_and_compute_mean(f'/HPC_work_dir/msm_HT_concate/{lobe}/curv/{temp}.curv.MSM_HT_std.func.gii', mask)
        msmpopu_std = load_and_compute_mean(f'/HPC_work_dir/msm_reg_to_global_push/curv/{lobe}.{temp}.curv.MSM_popu_std.func.gii', mask)
        msmhttop_std = load_and_compute_mean(f'/HPC_work_dir/msm_HT_concate/top/{lobe}.{temp}.curv.MSM_HT_top_std.func.gii', mask)

        if msmht_std is not None and msmpopu_std is not None and msmhttop_std is not None:
            std_temp.append([msmht_std, msmhttop_std, msmpopu_std])

    return np.array(std_temp)

# Main analysis

# exclude very small clusters <5 hemis
lobe_params = {
    "frontal": (['NODE1910', 'NODE2115', 'NODE2147'], 0.38),
    "parietal": (['NODE1856'], 0.477),
    "temporal": (['NODE2066', 'NODE2107', 'NODE2119', 'NODE2137', 'NODE2144'], 0.365),
}

std_lobe = []
p_values = []

for lobe, (exclude_cluster, cluster_thre) in lobe_params.items():
    std_temp = process_lobe(lobe, exclude_cluster, cluster_thre, simi_method, subject_list)
    std_lobe.append(std_temp)

    msmht_std_array, msmhttop_std_array, msmpopu_std_array = std_temp.T

    # Visualization
    plt.hist([msmht_std_array, msmhttop_std_array, msmpopu_std_array], bins=10, label=["MSMHT", "MSMHT-top", "MSMpopu"])
    plt.legend()
    plt.savefig(f'{lobe}_std_deviation_comparison.png')
    plt.close()

    # Statistical test
    stat, p_value = wilcoxon(msmht_std_array, msmpopu_std_array)
    print(f'{lobe}: ht vs popu p={p_value}')
    p_values.append(p_value)

# Correct p-values
from statsmodels.stats.multitest import multipletests
corrected_p_values = multipletests(p_values, method='bonferroni')[1]
print("Corrected p-values:", corrected_p_values)
