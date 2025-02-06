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
subject_list = open('../Data_files/Subjects_IDs_HCP_all_LR').read().splitlines()
df_surf_area_temporal_ratio = pd.read_csv('surf_area_temporal_ratio.csv')
df_leftrate = pd.read_csv(lobe+'_lobe_freq_result_30.csv')
df_language_scores= pd.read_csv('temporal_asymmetry/'+lobe+'_clusterID_language_scores.csv',index_col=False)
temporal_mask = nb.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/main5_levelstep/temporal_asymmetry/NODE2218_temporal_mask.shape.gii').darrays[0].data
temporal_indices = np.where(temporal_mask==1)[0]


# Filter rows where both 'ReadEng_AgeAdj' and 'PicVocab_AgeAdj' are not None (or NaN)
filtered_df = df_language_scores[df_language_scores['ReadEng_AgeAdj'].notna() & df_language_scores['PicVocab_AgeAdj'].notna()]

# Extract the 'Subject' column from the filtered DataFrame
subjects = filtered_df['Subject'].tolist()
filtered_language_score = filtered_df[['']]
for i, sub in enumerate(subjects):
    nb.load('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT_concate/asymmetry/101410.temporal_curv_asymmind.MSMHTtop_ico6.shape.gii')