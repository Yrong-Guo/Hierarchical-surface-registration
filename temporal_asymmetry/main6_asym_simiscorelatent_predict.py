import pandas as pd
import numpy as np
from sklearn.manifold import TSNE, SpectralEmbedding
import matplotlib.pyplot as plt
import umap
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

lobe='frontal'
simi_method = 'corrdice'
subject_list = open('../../Data_files/Subjects_IDs_HCP_all_LR').read().splitlines()
np.random.seed(42)  # For reproducibility

'''load in 3 similarity matrices'''
similarity_score_corr = np.load('../dendrogram_'+lobe+'/cc_'+lobe+'_corr_affine_mask_mtx.npy')
similarity_score_mse = np.load('../dendrogram_'+lobe+'/cc_'+lobe+'_mse_affine_mask_mtx.npy')
similarity_score_dice = np.load('../dendrogram_'+lobe+'/cc_'+lobe+'_dice_affine_mask_mtx.npy')

df= pd.read_csv(lobe+'_clusterID_language_scores.csv',index_col=False)
# Step 1: Prepare data
cluster_ID_LR = df[['L', 'R']]
#     'Subject', 'ReadEng_Unadj', 'ReadEng_AgeAdj', 'PicVocab_Unadj', 'PicVocab_AgeAdj',
#     'Language_Task_Acc', 'Language_Task_Median_RT', 'Language_Task_Story_Acc',
#     'Language_Task_Story_Median_RT', 'Language_Task_Story_Avg_Difficulty_Level',
#     'Language_Task_Math_Acc', 'Language_Task_Math_Median_RT', 'Language_Task_Math_Avg_Difficulty_Level,PMAT24_A_CR, PMAT24_A_SI, PMAT24_A_RTCR'

language_scores = df['Handedness']

valid_indices = language_scores.notna()
cluster_ID_LR = cluster_ID_LR[valid_indices]
df = df[valid_indices]
language_scores = language_scores[valid_indices]
subjects_with_scores = df['Subject'].astype(str).tolist()


# Binarize handedness scores: 0 for left-handed, 1 for right-handed
language_scores = (language_scores >= 0).astype(int)


'''similarity measurement'''
if simi_method == 'corrmse':
    similarity_score = 0.5 * similarity_score_corr + 0.5 * similarity_score_mse
elif simi_method == 'corrdice':
    similarity_score = 0.5 * similarity_score_corr + 0.5 * similarity_score_dice
else:
    similarity_score = None
    print('Error! select true simi_method')


np.fill_diagonal(similarity_score, 1)
left_hemisphere = similarity_score[:1110, :]
right_hemisphere = similarity_score[1110:, :]
combined_features = np.concatenate((left_hemisphere, right_hemisphere), axis=1)



# similarity_score_embedded = TSNE(n_components=3, init='random', learning_rate=1000, perplexity=150, random_state=42).fit_transform(similarity_score)
similarity_score_embedded = SpectralEmbedding(n_components=5, affinity='nearest_neighbors',random_state=42).fit_transform(similarity_score)
# umap_model = umap.UMAP(n_components=50, min_dist=0.01, n_neighbors=30, random_state=42, metric='cosine')  #metric='cosine'
# similarity_score_embedded = umap_model.fit_transform(combined_features)

filtered_indices = []
for i, sub_h in enumerate(subject_list[:1110]):
    sub  = sub_h[:-2]
    if sub in subjects_with_scores:
        filtered_indices.append(i)

similarity_score_embedded = similarity_score_embedded[filtered_indices,:]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(similarity_score_embedded, language_scores, test_size=0.2, random_state=42)


# Fit a classification model (Logistic Regression as an example)
model = LogisticRegression(random_state=42)
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

# Cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cross_val_scores = cross_val_score(model, similarity_score_embedded, language_scores, cv=kf, scoring='accuracy')

mean_accuracy = np.mean(cross_val_scores)
std_accuracy = np.std(cross_val_scores)

print(f"Mean Accuracy (10-Fold CV): {mean_accuracy:.2f}")
print(f"Standard Deviation: {std_accuracy:.2f}")

'''Regression'''
# # Fit a regression model (Random Forest as an example)
# model = LinearRegression()
# # model = RandomForestRegressor(random_state=42)
# model.fit(X_train, y_train)
#
# # Predict and evaluate
# y_pred = model.predict(X_test)
# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)
# correlation, p_value = pearsonr(y_test, y_pred)
#
# print(f"Mean Squared Error: {mse:.2f}")
# print(f"Pearson Correlation Coefficient: {correlation:.2f} (p-value: {p_value:.2g})")
#
# print(f"R^2 Score: {r2:.2f}")
#
#
#
# # Define a custom scorer function
# def correlation_scorer(y_true, y_pred):
#     corr, _ = pearsonr(y_true, y_pred)
#     return corr
#
# # Create a scorer using make_scorer
# correlation_scorer_func = make_scorer(correlation_scorer)
#
# # Initialize cross-validation
# kf = KFold(n_splits=10, shuffle=True, random_state=42)
#
# # Use Random Forest or Linear Regression as the model
# model = LinearRegression()
# # model = RandomForestRegressor(random_state=42)
#
# # Use cross_val_score with the custom correlation scorer
# correlation_scores = cross_val_score(model, similarity_score_embedded, language_scores, cv=kf, scoring=correlation_scorer_func)
#
# # Evaluate the mean and standard deviation of the correlation scores
# mean_correlation = np.mean(correlation_scores)
# std_correlation = np.std(correlation_scores)
#
# print(f"Mean Pearson Correlation Coefficient (5-Fold CV): {mean_correlation:.2f}")
# print(f"Standard Deviation: {std_correlation:.2f}")


























































# sub_hemi_temporal_clusterID = pd.read_csv('sub_hemi_temporal_clusterID.csv', index_col=None)
# sub_hemi_temporal_clusterID['subjects'] = pd.Categorical(
#     sub_hemi_temporal_clusterID['subjects'],
#     categories=subject_list,
#     ordered=True
# )
#
# # Sort the DataFrame by the 'Subject' column
# sub_hemi_temporal_clusterID_sorted = sub_hemi_temporal_clusterID.sort_values('subjects')
#
# # Reset index if desired
# sub_hemi_temporal_clusterID_sorted = sub_hemi_temporal_clusterID_sorted.reset_index(drop=True)
#
#
# # Create a dictionary for subject to cluster mapping
# subject_to_cluster = sub_hemi_temporal_clusterID_sorted.set_index('subjects')['temporal'].to_dict()
#
# # Map each subject in the subject list to its cluster, fill missing with a default 'No Cluster' label
# cluster_labels = [subject_to_cluster.get(subject, 'No Cluster') for subject in subject_list]
#
# # Create a color map based on clusters
# unique_clusters = set(cluster_labels)
# # colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_clusters)))  # Exclude default 'No Cluster' from colormap
# # color_dict = {cluster: color for cluster, color in zip(unique_clusters, colors)}
#
# cmap = plt.cm.get_cmap('tab20', len(unique_clusters))  # Change to 'tab20', 'Set3', etc. for better contrast
# color_dict = {cluster: cmap(i) for i, cluster in enumerate(unique_clusters)}
#
# color_dict['No Cluster'] = 'gray'  # Assign gray for subjects with no cluster
#
# # Map each cluster label to its color
# cluster_colors = [color_dict[label] for label in cluster_labels]
#
# # Plot t-SNE with color coding
# plt.figure(figsize=(12, 8))
# scatter = plt.scatter(similarity_score_embedded[:, 0], similarity_score_embedded[:, 1],
#                       c=cluster_colors, alpha=0.7, s=50)
#
# # Create a legend with cluster colors
# handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=str(cluster))
#            for cluster, color in color_dict.items()]
# plt.legend(handles=handles, title="Clusters", loc='best', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
#
# plt.title('t-SNE Visualization Colored by Clusters')
# plt.xlabel('t-SNE Component 1')
# plt.ylabel('t-SNE Component 2')
# plt.grid(True)
# plt.tight_layout()  # Adjusts layout to fit everything nicely
#
# plt.show()






