''''''

import matplotlib.pyplot as plt
import numpy as np
import pandas

from utils.hierarch_tools import leaf_in_cluster, hierarch_path_dict
from get_clusters_with_thre import get_clusters_with_thre
import pandas as pd

'''1. concurrence matrix'''
simi_method='corrdice'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'

lobe='frontal'

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

merge_path = '../main5_levelstep/dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl' #TODO: change it back to '+lobe+', now is just testing code using frontal lobe
temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )
### frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
# exclude_cluster = np.asarray(['NODE2066', 'NODE2107', 'NODE2119', 'NODE2137', 'NODE2144'])
temps_30 = np.setdiff1d(temps_30, exclude_cluster)



merge_path_temporal = '../main5_levelstep/dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
cluster_hie_dict_temporal = hierarch_path_dict(temps_30,merge_path_temporal)
cluster_leaf_dict_temporal = leaf_in_cluster(merge_path=merge_path_temporal)


sub_temp_hie_dict_temporal = {} # dict key:subject values:hierarchy

for temp in temps_30:

    dhcp_subs = cluster_leaf_dict_temporal[temp]

    for sub in dhcp_subs:

        # get subject - hierarchical path
        sub_temp_hie_dict_temporal[sub] = np.concatenate([np.asarray([temp]), np.asarray(cluster_hie_dict_temporal[temp])])



merge_path_temporal = '../main5_levelstep/dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
cluster_leaf_dict_temporal = leaf_in_cluster(merge_path=merge_path_temporal)



sub_temporal=np.asarray([])

for temp in temps_30:
    sub_temporal = np.append(sub_temporal,cluster_leaf_dict_temporal[temp])



sub_temp_data = pd.DataFrame(columns=['subjects', lobe])
for sub in sub_temporal:

    temp_data = pd.DataFrame({
        'subjects': [sub],
        lobe: [sub_temp_hie_dict_temporal[sub][0]]
    })
    # Append the new row to the DataFrame
    sub_temp_data = pd.concat([sub_temp_data, temp_data], ignore_index=True)


# Create a DataFrame from the collected data
sub_temp_data.to_csv('temporal_asymmetry/sub_hemi_'+lobe+'_clusterID.csv', index=False)



# Assuming data loading from 'data.csv' (you will replace this with your actual file path)
data = pd.read_csv('temporal_asymmetry/sub_hemi_'+lobe+'_clusterID.csv')

# Split the 'subjects' column to isolate the subject identifier and the side (L or R)
data['Subject'] = data['subjects'].str.extract(r'(\d+)')
data['Side'] = data['subjects'].str.extract(r'([LR])$')

# Pivot the table to wide format with separate columns for L and R nodes
pivot_table = data.pivot_table(index='Subject', columns='Side', values=lobe, aggfunc='first')

# Flatten the columns by renaming them
pivot_table.columns = [f'{col}' for col in pivot_table.columns]

# Reset the index to include 'Subject' as a column
result = pivot_table.reset_index()
result = result.dropna(subset=['L', 'R'])

# Save the resulting DataFrame to a CSV file
result.to_csv('temporal_asymmetry/sub_'+lobe+'_clusterID.csv', index=False)

# Display the first few rows to confirm the result
print(result.head())


language_score_df = pd.read_csv('temporal_asymmetry/unrestricted_guoyourong_6_21_2023_9_9_43.csv',index_col=False)
filtered_language_scores = language_score_df[language_score_df['Subject'].isin(result['Subject'].astype('int64'))]
filtered_language_scores['Subject'] = filtered_language_scores['Subject'].astype(str)
required_columns = [
    'Subject', 'ReadEng_Unadj', 'ReadEng_AgeAdj', 'PicVocab_Unadj', 'PicVocab_AgeAdj',
    'Language_Task_Acc', 'Language_Task_Median_RT', 'Language_Task_Story_Acc',
    'Language_Task_Story_Median_RT', 'Language_Task_Story_Avg_Difficulty_Level',
    'Language_Task_Math_Acc', 'Language_Task_Math_Median_RT', 'Language_Task_Math_Avg_Difficulty_Level' ,'PMAT24_A_CR','PMAT24_A_SI', 'PMAT24_A_RTCR'
]

final_scores = filtered_language_scores[filtered_language_scores.columns.intersection(required_columns)]



final_scores.to_csv('temporal_asymmetry/filtered_language_scores.csv', index=False)

combined_df = pd.merge(result, final_scores, on='Subject', how='left')
combined_df.to_csv('temporal_asymmetry/'+lobe+'_clusterID_language_scores.csv', index=False)


language_score_df_2 = pd.read_csv('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/main5_levelstep/temporal_asymmetry/RESTRICTED_guoyourong_5_25_2023_8_45_0.csv')
filtered_language_scores = language_score_df_2[language_score_df_2['Subject'].isin(result['Subject'].astype('int64'))]
required_columns = ['Subject','Handedness']
final_scores = filtered_language_scores[filtered_language_scores.columns.intersection(required_columns)]
final_scores['Subject'] = final_scores['Subject'].astype(str)
combined_df = pd.merge(combined_df, final_scores, on='Subject', how='left')
combined_df.to_csv('temporal_asymmetry/'+lobe+'_clusterID_language_scores.csv', index=False)

