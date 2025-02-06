import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder

# Assuming you have a DataFrame `df` with columns 'left_cluster_id', 'right_cluster_id', and 'language_score'
df= pd.read_csv('temporal_asymmetry/temporal_clusterID_language_scores.csv',index_col=False)
# Step 1: Prepare data
X = df[['L', 'R']]

#     'Subject', 'ReadEng_Unadj', 'ReadEng_AgeAdj', 'PicVocab_Unadj', 'PicVocab_AgeAdj',
#     'Language_Task_Acc', 'Language_Task_Median_RT', 'Language_Task_Story_Acc',
#     'Language_Task_Story_Median_RT', 'Language_Task_Story_Avg_Difficulty_Level',
#     'Language_Task_Math_Acc', 'Language_Task_Math_Median_RT', 'Language_Task_Math_Avg_Difficulty_Level'
y = df['Language_Task_Math_Median_RT']


valid_indices = y.notna()
X = X[valid_indices]
y = y[valid_indices]

# Step 2: Encode categorical variables
encoder = OneHotEncoder(sparse=False)
X_encoded = encoder.fit_transform(X)

# Step 3: Split the data
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Step 4: Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Optional: Step 6: Interpret the coefficients
coefficients = model.coef_
features = encoder.get_feature_names_out(['L', 'R'])
coeff_df = pd.DataFrame(coefficients, index=features, columns=['Coefficient'])

print(coeff_df.sort_values(by='Coefficient', ascending=False))
