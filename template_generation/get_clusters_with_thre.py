import numpy as np
import pandas as pd

#
# # initialization
# cluster_thre = 0.29 # mse 20 cluster0.2646 28 0.25   # corr 30 cluster 0.34 <5out   0.248 30 cluster   0.29 10 cluster
# subjects = open('Data_files/Subjects_IDs_HCP_hierarch_' + str(0), "r").read().splitlines()
#
# # get the merging pass of the
# merge = pd.read_pickle('dendrogram/mergeprocess_frontal_corrmse_affine_mask_complete_0.pkl')
# merge_thresh = merge[merge['distance']<cluster_thre]
# Nodes = np.asarray(merge_thresh['mergeID'])
#
# # for each subject/ node, see if they exist in subIDs if exist, then it is not a single cluster
# subID1 = np.asarray(merge_thresh['subID1'])
# subID2 = np.asarray(merge_thresh['subID2'])
# cnt = 0
# for node in Nodes:
#     if (node not in subID1) & (node not in subID2):
#         cnt+=1
#         print(node + ', size = '+str(merge_thresh[merge_thresh['mergeID']==node]['cluster_size'].to_numpy()[0]))
#
# for sub in subjects:
#     if (sub not in subID1) & (sub not in subID2):
#         cnt += 1
#         print(sub)
#
# print(cnt)



def leaf_in_cluster(merge_path = None):
    """

    :param node: string id e.g. 'NODE001' '110234'
    :param merge_path: path of the merge file
    :return: leaf_id the string np array of leaves of give node
    """

    # get the merging pass of the
    merge = pd.read_pickle(merge_path)
    leaf_id = {}
    for i in range(len(merge)):
        nodeid = merge.loc[[i]]
        if 'NODE' in nodeid['subID1'].values[0]: # if branch 1 is a node
            leaf_id[nodeid['mergeID'].values[0]] = leaf_id[nodeid['subID1'].values[0]] # add previous saved branch dict to it
        else:
            leaf_id[nodeid['mergeID'].values[0]] = np.asarray(nodeid['subID1']) # add it self to it
        if 'NODE' in nodeid['subID2'].values[0]:
            leaf_id[nodeid['mergeID'].values[0]] = np.append(leaf_id[nodeid['mergeID'].values[0]],leaf_id[nodeid['subID2'].values[0]])
        else:
            leaf_id[nodeid['mergeID'].values[0]] = np.append(leaf_id[nodeid['mergeID'].values[0]], np.asarray(nodeid['subID2']))
    return leaf_id
