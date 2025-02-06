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
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

lobe='temporal'
simi_method = 'corrdice'
subject_list = open('../../Data_files/Subjects_IDs_HCP_all_LR').read().splitlines()
df_surf_area_temporal_ratio = pd.read_csv('../surf_area_temporal_ratio.csv')
df_leftrate = pd.read_csv('../'+lobe+'_lobe_freq_result_30.csv')





# Parse subject and hemisphere from the subject ID
df_surf_area_temporal_ratio['Base_Subject'] = df_surf_area_temporal_ratio['cluster_subjects'].apply(lambda x: x[:-2])  # Remove '.L' or '.R' to get the base subject ID
df_surf_area_temporal_ratio['Hemisphere'] = df_surf_area_temporal_ratio['cluster_subjects'].apply(lambda x: x[-1]+'_narea')

df_sub_arearatioLR = df_surf_area_temporal_ratio.pivot(index='Base_Subject', columns='Hemisphere', values='surf_area_temporal_ratio')

df_sub_arearatioLR['Asymmetry_Index'] = (df_sub_arearatioLR['L_narea']-df_sub_arearatioLR['R_narea'])#/(df_sub_arearatioLR['L_narea']+df_sub_arearatioLR['R_narea'])
# Save the results to a new CSV file
df_sub_arearatioLR.to_csv('sub_arearatioLR_asymmetry_index.csv', columns=['Asymmetry_Index'])


'''now language scores'''

df_language_scores= pd.read_csv(lobe+'_clusterID_language_scores.csv',index_col=False)
df_language_scores['Subject'] = df_language_scores['Subject'].astype(str)
df_language_scores['Template'] = df_language_scores['L']
# Merge DataFrames on the 'Template' and 'templates' column
df_merged = pd.merge(df_language_scores, df_leftrate[['templates', 'left_rate']], left_on='Template', right_on='templates', how='left')
df_merged['Template'] = df_language_scores['R']
df_merged = pd.merge(df_merged, df_leftrate[['templates', 'left_rate']], left_on='Template', right_on='templates', how='left')

df_merged.drop(columns=['templates_x','templates_y','Template'], inplace=True)

# # Step 1: Prepare data
# #     'Subject', 'ReadEng_Unadj', 'ReadEng_AgeAdj', 'PicVocab_Unadj', 'PicVocab_AgeAdj',
# #     'Language_Task_Acc', 'Language_Task_Median_RT', 'Language_Task_Story_Acc',
# #     'Language_Task_Story_Median_RT', 'Language_Task_Story_Avg_Difficulty_Level',
# #     'Language_Task_Math_Acc', 'Language_Task_Math_Median_RT', 'Language_Task_Math_Avg_Difficulty_Level,PMAT24_A_CR, PMAT24_A_SI, PMAT24_A_RTCR'
score_type = 'ReadEng_AgeAdj'    #Language_Task_Median_RT


# df_merged = pd.merge(df_sub_arearatioLR, df_language_scores, left_index=True, right_on='Subject', how='inner')
df_filtered = df_merged[df_merged[score_type].notna()]
# df_filtered.to_csv('filtered_language_data.csv', index=False)
#

X = df_filtered[['L','R']]  # Cluster-level LHR for each subject
encoder = OneHotEncoder(sparse=False)
X_encoded = encoder.fit_transform(X)
X_encoded = np.concatenate([X_encoded,df_filtered[['left_rate_x','left_rate_y']].to_numpy()],axis=1)
Y = df_filtered[['ReadEng_AgeAdj', 'PicVocab_AgeAdj']]  # Language scores


# Standardize the data
scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)
Y_scaled = scaler.fit_transform(Y)

# Perform CCA
cca = CCA(n_components=1)  # Start with 1 component for simplicity
cca.fit(X_encoded, Y_scaled)

# Transform the datasets
X_c, Y_c = cca.transform(X_encoded, Y_scaled)

# Calculate and print canonical correlations
observed_correlation = np.corrcoef(X_c.T, Y_c.T).diagonal(offset=1)[:cca.n_components]
print("Canonical correlations:", observed_correlation)

# Permutation test for p-values
num_permutations = 1000
permuted_correlations = np.zeros(num_permutations)

for i in range(num_permutations):
    np.random.shuffle(Y_scaled)  # Shuffle the rows of Y
    X_perm, Y_perm = cca.fit_transform(X_encoded, Y_scaled)
    permuted_correlation = np.corrcoef(X_perm.T, Y_perm.T).diagonal(offset=1)[:cca.n_components]
    permuted_correlations[i] = permuted_correlation

# Calculate p-value
p_value = np.mean(permuted_correlations >= observed_correlation)
print("P-value:", p_value)


correlation_coefficient, p_value = pearsonr(df_filtered['left_rate_y'], df_filtered[score_type])

# df_filtered[score_type] = (df_filtered[score_type] >= 0).astype(int)
# Print the results
print(f"Pearson Correlation Coefficient: {correlation_coefficient}")
print(f"P-value: {p_value}")


# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df_filtered[['left_rate_y']], df_filtered[score_type], test_size=0.2, random_state=42)


# Fit a classification model (Logistic Regression as an example)
model = RandomForestClassifier(random_state=42)
# model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"ROC-AUC: {roc_auc:.2f}")


