import numpy as np
from get_clusters_with_thre import get_clusters_with_thre
import nibabel as nb
import matplotlib.pyplot as plt
from scipy.stats import shapiro, ttest_rel, wilcoxon
from get_clusters_with_thre import get_clusters_with_thre

simi_method='corrdice'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'
std_lobe = []
p_values = []
for lobe in ['frontal','parietal','temporal']:

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

    merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl' #TODO: change it back to '+lobe+', now is just testing code using frontal lobe
    temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )
    ### frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
    # exclude_cluster = np.asarray(['NODE2066', 'NODE2107', 'NODE2119', 'NODE2137', 'NODE2144'])
    temps_30 = np.setdiff1d(temps_30, exclude_cluster)

    std_temp=[]

    for temp in temps_30:
        # msmht_std_map = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/{lobe}/curv/{temp}.curv.MSM_HT_std.func.gii').darrays[0].data
        msmht_std_map = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/{lobe}/curv/{temp}.curv.MSM_HT_std.func.gii').darrays[0].data
        msmpopu_std_map = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_reg_to_global_push/curv/{lobe}.{temp}.curv.MSM_popu_std.func.gii').darrays[0].data
        msmhttop_std_map = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/top/{lobe}.{temp}.curv.MSM_HT_top_std.func.gii').darrays[0].data
        lobe_mask = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/lobe_msk/{lobe}/{temp}_{lobe}_mask.shape.gii').darrays[0].data

        lobe_indices = np.where(lobe_mask==1)[0]
        msmht_std = np.mean(msmht_std_map[lobe_indices])
        msmhttop_std = np.mean(msmhttop_std_map[lobe_indices])
        msmpopu_std = np.mean(msmpopu_std_map[lobe_indices])

        std_temp.append([msmht_std,msmhttop_std,msmpopu_std])

    std_temp = np.asarray(std_temp)
    std_lobe.append(std_temp)


    # Convert the std_temp to separate arrays for MSMHT and MSMpopu
    msmht_std_array = std_temp[:, 0]
    msmhttop_std_array = std_temp[:, 1]
    msmpopu_std_array = std_temp[:, 2]

    # Visualize the distributions
    plt.figure(figsize=(12, 6))
    plt.hist(msmht_std_array, bins=10, alpha=0.5, label='MSMHT', color='blue', edgecolor='black')
    plt.hist(msmhttop_std_array, bins=10, alpha=0.5, label='MSMHT-top', color='yellow', edgecolor='black')
    plt.hist(msmpopu_std_array, bins=10, alpha=0.5, label='MSMpopu', color='red', edgecolor='black')
    plt.title(f'{lobe.capitalize()} Lobe: MSMHT vs MSMpopu Standard Deviations')
    plt.xlabel('Standard Deviation')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    # # Perform normality test
    # shapiro_msmht = shapiro(msmht_std_array)
    # shapiro_msmhttop = shapiro(msmhttop_std_array)
    # shapiro_msmpopu = shapiro(msmpopu_std_array)
    #
    # print(f'{lobe.capitalize()} Lobe:')
    # print(f'MSMHT Shapiro-Wilk Test: Statistic={shapiro_msmht.statistic:.4f}, p-value={shapiro_msmht.pvalue:.4f}')
    # print(f'MSMHT Shapiro-Wilk Test: Statistic={shapiro_msmhttop.statistic:.4f}, p-value={shapiro_msmhttop.pvalue:.4f}')
    # print(f'MSMpopu Shapiro-Wilk Test: Statistic={shapiro_msmpopu.statistic:.4f}, p-value={shapiro_msmpopu.pvalue:.4f}')

    # # Choose the appropriate test
    # if shapiro_msmht.pvalue > 0.05 and shapiro_msmpopu.pvalue > 0.05 and shapiro_msmhttop.pvalue > 0.05:
    #     # Both distributions are normal
    #     stat, p_value = ttest_rel(msmht_std_array, msmpopu_std_array)
    #     print(f'ht vs. popu Paired t-test: t-statistic={stat:.4f}, p-value={p_value:.4f}')
    #     stat, p_value = ttest_rel(msmht_std_array, msmhttop_std_array)
    #     print(f'ht vs. top Paired t-test: t-statistic={stat:.4f}, p-value={p_value:.4f}')
    # else:
        # Non-normal distributions
    stat, p_value = wilcoxon(msmht_std_array, msmpopu_std_array)
    print(f'ht vs. popu Wilcoxon signed-rank test: W-statistic={stat:.4f}, p-value={p_value:.4f}')
    stat, p_value = wilcoxon(msmhttop_std_array, msmpopu_std_array)
    print(f'ht vs. top Wilcoxon signed-rank test: W-statistic={stat:.4f}, p-value={p_value:.4f}')

    print('\n')
    p_values.append(p_value)

print("Analysis completed.")





