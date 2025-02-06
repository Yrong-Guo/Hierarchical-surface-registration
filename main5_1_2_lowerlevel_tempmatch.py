import numpy as np
import pickle
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
from wbtools_light_subtemp import msm_reg_template_2,generate_average_metric_command_unbiastemp,generate_average_metric_command,curv_warp_to_sulc
from utils.similarity_assess_func import corr_similarity, DiceFun
import nibabel as nb
import matplotlib.pyplot as plt
import pandas as pd



lobe = 'temporal'
simi_method = 'corrdice'
partition = 'cpu'
n_hemi = 2220
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'
sub_cluster_size = 25
create_work_dir='/scratch/prj/cortical_imaging/Yourong/hierarch/'+lobe+'_lobe/subtemps'
len_dataset = 246    # 246 for RICE subjects

merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl' #TODO: change it back to '+lobe+', now is just testing code using frontal lobe
f = open(merge_path,'rb')
merge_path_df = pickle.load(f)

if lobe == 'temporal':
    exclude_cluster = np.asarray(['NODE2066', 'NODE2107', 'NODE2119', 'NODE2137', 'NODE2144'])
    cluster_thre = 0.365
elif lobe == 'parietal':
    exclude_cluster = np.asarray(['NODE1856'])
    cluster_thre = 0.477
elif lobe == 'frontal':
    exclude_cluster = np.asarray(['NODE1910', 'NODE2115', 'NODE2147'])
    cluster_thre = 0.38

temp_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True)

cluster_leaf_dict = leaf_in_cluster(merge_path)


# subtemp_sizes = []
# for subtemp in temp_30:
#     subtemp_sizes.append(len(cluster_leaf_dict[subtemp]))
# plt.hist(subtemp_sizes, bins=50, edgecolor='black')
# plt.show()



'''break down large node test'''
def break_down_node(node, df, max_size=30, min_size = 6, chain=None):
    if chain is None:
        chain = []

    # Find the row where this node was created
    row = df[df['mergeID'] == node]

    if row.empty:
        # Base case: Node is not found, this might be a base sub-cluster
        return [node], chain

    # Get the cluster size
    cluster_size = row['cluster_size'].values[0]

    if cluster_size <= max_size:
        # Base case: If cluster size is already <= max_size, return this node
        return [node], chain

    # Recursively break down the node
    sub1 = row['subID1'].values[0]
    sub2 = row['subID2'].values[0]

    # Get sizes of the subclusters
    size1 = df[df['mergeID'] == sub1]['cluster_size'].values[0] if not df[df['mergeID'] == sub1].empty else 1
    size2 = df[df['mergeID'] == sub2]['cluster_size'].values[0] if not df[df['mergeID'] == sub2].empty else 1

    # Add current node to the chain
    chain.append(node)

    # Evaluate sub-cluster sizes
    if size1 < min_size or size2 < min_size:
        # Avoid splitting if one resulting cluster would be too small
        return [node], chain

    # Recur for both sub-nodes
    nodes1, chain1 = break_down_node(sub1, df, max_size, min_size, chain.copy())
    nodes2, chain2 = break_down_node(sub2, df, max_size, min_size, chain.copy())

    # Combine results
    return nodes1 + nodes2, chain1 + chain2


# Example: Break down NODE2186
# final_nodes, node_chain = break_down_node('NODE2186', merge_path_df)


'''
for every cluster larger than sub_cluster_size break it down 
until they are smaller then sub_cluster_size
return their breakdown nodes.
output temp_remain: node that are small enough and don't need to subdivided
       subtemp_all: sub templates
       subtemp_maintemp: sub-templates' original main temp 
'''
# subtemp_cnt = 0
temp_remain = []
final_node_all = []
final_node_all_maintemp = []

for temp in temp_30:
    if len(cluster_leaf_dict[temp]) > 35:
        final_nodes, _ = break_down_node(temp, merge_path_df)
        final_node_all.append(final_nodes)
        final_node_all_maintemp.append([temp]*len(final_nodes))
        # subtemp_cnt+=len(final_nodes)

    else:
        temp_remain.append(temp)
# # save the templates remain the same as a txt
# with open('temp_remain_'+lobe,'w') as f:
#     f.write('\n'.join(temp_remain)+ '\n')


f_move = open(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/match_subtemps/{lobe}_sulcreg_move_list','w')
f_tar = open(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/match_subtemps/{lobe}_sulcreg_tar_list','w')
for temp in temp_remain:
    subject_in_temp = cluster_leaf_dict[temp]
    for sub in subject_in_temp:
        f_move.write(sub+ '\n')
        f_tar.write(temp+ '\n')
f_move.close()
f_tar.close()




# flatten

subtemp_all = []
subtemp_maintemp = []
for i, final_node in enumerate(final_node_all):
    for j, subtemp in enumerate(final_node):
        subtemp_all.append(subtemp)
        subtemp_maintemp.append(final_node_all_maintemp[i][j])

subtemp_maintemp_table = np.concatenate((np.asarray(subtemp_all).reshape(-1,1),np.asarray(subtemp_maintemp).reshape(-1,1)),axis=1)
np.save(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/match_subtemps/subtemp_maintemp_table_{lobe}.npy',subtemp_maintemp_table)

'''After registration, start accessing simiarity

'''
temp_for_match_hcp = subtemp_all+temp_remain

# save the templates remain the same as a txt
with open('/home/yg21/YourongGuo/normativemodel/hierarc_hcp/match_subtemps/subtemp_all_'+lobe,'w') as f:
    f.write('\n'.join(temp_for_match_hcp)+ '\n')


# get all subjects first (sub)templates

sulcreg_move_list = []
sulcreg_tar_list = []
cnt = 0
for temp in temp_for_match_hcp:
    if 'NODE' in temp: # exclude the individual subject not in any cluster in this level
        for n, sub in enumerate(cluster_leaf_dict[temp]): # subjects in this cluster

            sulcreg_move_list.append(sub)
            sulcreg_tar_list.append(temp)


subject_first_templates = pd.DataFrame(np.concatenate((np.asarray(sulcreg_move_list).reshape(-1,1),np.asarray(sulcreg_tar_list).reshape(-1,1)), axis=1), columns=['subjects','templates'])

subject_first_templates.to_csv(f'subject_firsttemp_subtemps_{lobe}.csv', index=False, index_label=None)





subtemp_sizes = []
for subtemp in temp_for_match_hcp:
    subtemp_sizes.append(len(cluster_leaf_dict[subtemp]))
plt.hist(subtemp_sizes, bins=50, edgecolor='black')
plt.show()






#
# corr_hcptemp_otherdata_mtx = np.zeros((len(subtemp_all)+len(temp_remain),len_dataset))
# for i,sub_hcp in enumerate(temp_for_match_hcp):
#     sub_hcp_temp_img = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/final_temp/{lobe}/{sub_hcp}.curv.affine.ico6.shape.gii').darrays[0].data
#     lobe_mask = nb.load(f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/msm_HT/lobe_msk/{lobe}/{sub_hcp}_{lobe}_mask.shape.gii').darrays[0].data
#     for j,sub_neo in enumerate(temp_for_match_hcp):
#         sub_neo_temp_img = nb.load(
#             f'/home/yg21/YourongGuo/normativemodel/hierarc_hcp/matching_neonate_Temps/{lobe}_lobe/Neo_{sub_neo}.msm_unbiased.HCP_{sub_hcp}.curv.affine.ico6.shape.gii').darrays[0].data
#         corr_hcptemp_otherdata_mtx[i,j]=corr_similarity(sub_hcp_temp_img,sub_neo_temp_img,lobe_mask)
