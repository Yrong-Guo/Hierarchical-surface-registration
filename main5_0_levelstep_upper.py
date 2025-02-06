"""
Given the hierarchy, pairwise merge until the registration done.
A version for generation grid for registration issue

adapted to new HPC clusters

"""

import numpy as np
import sys
sys.path.append("..")
from test_deform import pairwise_reg_similarity

# Define dataset paths (update as needed)
MOVE_ROOT = '../Data_files/Subjects_IDs_HCP_moving'
TARGET_ROOT = '../Data_files/Subjects_IDs_HCP_target'

# Define similarity metric names and corresponding indices
SIMILARITY_METRICS = {
    "corr": 1,  # gcc (correlation)
    "mse": 0,   # Mean squared error
    "dice": 2,  # Dice coefficient
    "mi": 3     # Mutual information
}

# Run pairwise registration and similarity calculations
frontal_scores, parietal_scores, temporal_scores = pairwise_reg_similarity(
    move_root=MOVE_ROOT, target_root=TARGET_ROOT, test_mode=True)

# Store results in a dictionary
LOBES = {
    "frontal": frontal_scores,
    "parietal": parietal_scores,
    "temporal": temporal_scores
}

def compute_and_save_similarity_matrix(lobe, scores):
    """Computes and saves similarity matrices for all metrics."""
    for metric, index in SIMILARITY_METRICS.items():
        similarity_score = scores[index]

        # Compute size of the similarity matrix
        size = int((-1 + np.sqrt(1 + 4 * 2 * len(similarity_score))) / 2) + 1
        similarity_mtx = np.zeros((size, size))

        # Fill the upper triangle of the matrix
        pair_n = 0
        for i in range(size):
            for j in range(i + 1, size):
                similarity_mtx[i, j] = similarity_score[pair_n]
                pair_n += 1

        # Make the matrix symmetric
        similarity_mtx = similarity_mtx + similarity_mtx.T - np.diag(np.diag(similarity_mtx))

        # Adjust values if needed (only "corr" and "mse" need 1 - similarity transformation)
        if metric in ["corr", "mse"]:
            similarity_mtx = 1 - similarity_mtx

        # Save the similarity matrix
        save_path = f"dendrogram_{lobe}/cc_{lobe}_{metric}_affine_mask_mtx.npy"
        np.save(save_path, similarity_mtx)
        print(f"Saved: {save_path}")

# Compute and save similarity matrices for all lobes
for lobe, scores in LOBES.items():
    compute_and_save_similarity_matrix(lobe, scores)
