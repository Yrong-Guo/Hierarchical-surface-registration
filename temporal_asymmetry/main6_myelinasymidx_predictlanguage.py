import pandas as pd
import numpy as np
from sklearn.manifold import TSNE, SpectralEmbedding
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, KFold
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import pearsonr
from sklearn.metrics import make_scorer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.cross_decomposition import CCA
from sklearn.decomposition import PCA
from sklearn.manifold import SpectralEmbedding
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import nibabel as nb
import json
import os


lobe='temporal'
simi_method = 'corrdice'
subject_list = open('../../Data_files/Subjects_IDs_HCP_all_LR').read().splitlines()
df_surf_area_temporal_ratio = pd.read_csv('../surf_area_temporal_ratio.csv')
df_leftrate = pd.read_csv('../'+lobe+'_lobe_freq_result_30.csv')
df_language_scores= pd.read_csv(lobe+'_clusterID_language_scores.csv',index_col=False)
temporal_mask = nb.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/main5_levelstep/temporal_asymmetry/NODE2218_temporal_mask.shape.gii').darrays[0].data
temporal_indices = np.where(temporal_mask==1)[0]


parcellation_dict = nb.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/100206.L.CorticalAreas_dil_NewMLP_Individual.MSMHTtop_ico6.label.gii').labeltable.get_labels_as_dict()
parcellation_dict_L = {}
for roi_id, roi_name in parcellation_dict.items():
    if (int(roi_id) > 180) &('L_' in roi_name):
        parcellation_dict_L[roi_id] = roi_name
output_file = 'parcellation_dict_L.json'
with open(output_file, 'w') as f:
    json.dump(parcellation_dict_L, f, indent=4)



# parcellation_data = nb.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/100206.L.CorticalAreas_dil_NewMLP_Individual.MSMHTtop_ico6.label.gii').darrays[0].data
# temporal_ROIs_subdict_L = {}
# temporal_ROIs_subdict_R = {}
# img_init = np.zeros(40962)

# for roi_id, roi_name in parcellation_dict.items():
#     current_roi_ind = np.where(parcellation_data == roi_id)[0]
#
#     intersection = np.intersect1d(current_roi_ind, temporal_indices)
#
#     if current_roi_ind.any():
#         overlap_percentage = (len(intersection) / len(current_roi_ind)) * 100
#
#     # Check if overlap is more than 50%
#     if overlap_percentage > 50:
#         temporal_ROIs_subdict_L[roi_name] = roi_id
#         temporal_ROIs_subdict_R['R_'+roi_name[2:]] = roi_id-180
#         img_init[current_roi_ind] = 1
#
# header_init = parcellation_data = nb.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/100206.L.CorticalAreas_dil_NewMLP_Individual.MSMHTtop_ico6.label.gii')
# header_init.darrays[0].data = img_init
# nb.save(header_init, 'temp_test.label.gii')

# # Save the dictionary to a JSON file
# output_file = 'temporal_rois_overlap_L.json'
# with open(output_file, 'w') as f:
#     json.dump(temporal_ROIs_subdict_L, f, indent=4)
#     output_file = 'temporal_rois_overlap_R.json'
#     with open(output_file, 'w') as f:
#         json.dump(temporal_ROIs_subdict_R, f, indent=4)



parcellation_dict = 'parcellation_dict_L.json'
with open(parcellation_dict, 'r') as f:
    parcellation_dict_L = json.load(f)

# temporal_rois_file = 'temporal_rois_overlap_L.json'
# with open(temporal_rois_file, 'r') as f:
#     loaded_temporal_rois_subdict_L = json.load(f)

# temporal_rois_file = 'temporal_rois_overlap_R.json'
# with open(temporal_rois_file, 'r') as f:
#     loaded_temporal_rois_subdict_R = json.load(f)



# Filter rows where both 'ReadEng_AgeAdj' and 'PicVocab_AgeAdj' are not None (or NaN)
filtered_df = df_language_scores[df_language_scores['ReadEng_AgeAdj'].notna() & df_language_scores['PicVocab_AgeAdj'].notna()]

# Extract the 'Subject' column from the filtered DataFrame
subjects = filtered_df['Subject'].tolist()

# temporal_lobe_asymind_data = np.zeros((len(subjects),len(temporal_indices)))
temporal_lobe_asymind_parcel = []
no_myelin = []
for i, sub in enumerate(subjects):
    if not os.path.exists(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/{sub}.L.CorticalAreas_dil_NewMLP_Individual.MSMHTtop_ico6.label.gii'):
        no_myelin.append(i)
        continue
    # temporal_lobe_asymind_data[i,:] = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/{sub}.temporal_MyelinMap_asymmind.MSMHTtop_ico6.shape.gii').darrays[0].data[temporal_indices]
    temporal_lobe_asymind_data = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/{sub}.MyelinMap_asymmind.MSMHTtop_ico6.shape.gii').darrays[0].data
    temporal_lobe_asymind_label = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/myelin_parcellation_va/{sub}.L.CorticalAreas_dil_NewMLP_Individual.MSMHTtop_ico6.label.gii').darrays[0].data
    cnt = 0
    current_data = np.zeros((1,180))
    for roi_id, roi_name in parcellation_dict_L.items():

        ind_i = np.where(temporal_lobe_asymind_label== int(roi_id))[0]
        label_value = np.mean(temporal_lobe_asymind_data[ind_i])
        if np.isnan(label_value):
            label_value = 0
        current_data[0,cnt]=label_value
        cnt += 1
    temporal_lobe_asymind_parcel.append(current_data)
temporal_lobe_asymind_parcel = np.concatenate(temporal_lobe_asymind_parcel)
np.save('asymind_parcel.npy',temporal_lobe_asymind_parcel)

filtered_df = filtered_df.drop(no_myelin).reset_index(drop=True)
# # Step 1: Prepare data
# #     'Subject', 'ReadEng_Unadj', 'ReadEng_AgeAdj', 'PicVocab_Unadj', 'PicVocab_AgeAdj',
# #     'Language_Task_Acc', 'Language_Task_Median_RT', 'Language_Task_Story_Acc',
# #     'Language_Task_Story_Median_RT', 'Language_Task_Story_Avg_Difficulty_Level',
# #     'Language_Task_Math_Acc', 'Language_Task_Math_Median_RT', 'Language_Task_Math_Avg_Difficulty_Level,PMAT24_A_CR, PMAT24_A_SI, PMAT24_A_RTCR'


X = temporal_lobe_asymind_parcel
# X_encoded = np.concatenate([X_encoded,df_filtered[['left_rate_x','left_rate_y']].to_numpy()],axis=1)
Y = filtered_df[['ReadEng_AgeAdj', 'PicVocab_AgeAdj']]  # Language scores


# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
Y_scaled = scaler.fit_transform(Y)

# pca = PCA(n_components=2)
# pca.fit(X_scaled)
# X_c = pca.transform(X_scaled)
# observed_correlation = np.corrcoef(X_c[:,0], Y_scaled[:,0])
# correlation, p_value = pearsonr(X_c[:,0],  Y_scaled[:,0])


cca = CCA(n_components=1)
cca.fit(X_scaled,Y_scaled)
X_c, Y_c = cca.transform(X_scaled,Y_scaled)
observed_correlation = np.corrcoef(X_c[:,0], Y_c[:,0])

observed_correlations = [np.corrcoef(X_c[:, i], Y_c[:, i])[0, 1] for i in range(cca.n_components)]
correlation, p_value = pearsonr(X_c[:,0],  Y_c[:,0])




# Permutation test
num_permutations = 1000
permuted_correlations = np.zeros((num_permutations, cca.n_components))

for i in range(num_permutations):
    np.random.shuffle(Y_scaled)  # Shuffle the rows of Y
    X_perm, Y_perm = cca.fit_transform(X_scaled, Y_scaled)
    permuted_correlations[i, :] = [np.corrcoef(X_perm[:, j], Y_perm[:, j])[0, 1] for j in range(cca.n_components)]

# Calculate p-values
p_values = np.mean(permuted_correlations >= observed_correlations, axis=0)
print("P-values:", p_values)




# embedding = SpectralEmbedding(n_components=15, affinity='nearest_neighbors', random_state=42)
# X_transformed = embedding.fit_transform(X_scaled)
# # Plot the result
# plt.scatter(X_transformed[:, 0], X_transformed[:, 1], c='blue', marker='o')
# plt.title('Spectral Embedding')
# plt.xlabel('Component 1')
# plt.ylabel('Component 2')
# plt.show()
#
# # Split the data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(X_transformed, Y_scaled, test_size=0.2, random_state=42)
#
# # Train a linear regression model
# model = LinearRegression()
# model.fit(X_train, y_train)
#
# # Predict on the test set
# y_pred = model.predict(X_test)
#
# # Evaluate the model
# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)
#
# print(f"Mean Squared Error: {mse:.2f}")
# print(f"R^2 Score: {r2:.2f}")
# # Extract the first component
# first_component = X_transformed[:, 0]
#
# # Calculate Pearson correlation
# correlation, p_value = pearsonr(first_component, Y_scaled[:,1])
#
# # Print the results
# print(f"Pearson Correlation Coefficient: {correlation:.2f}")
# print(f"P-value: {p_value:.2f}")