import numpy as np
import os
import pandas as pd
from wbtools_main5 import msm_reg#,modify_sphere
from test_deform import pairwise_reg_similarity
from find_hierarch import cluster_CC
import nibabel as nib
from DDR_Coarse_STN import bilinearResampleSphereSurfImg, get_latlon_img,get_bi_inter
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre





'''
initialise
'''
lobe='temporal'
simi_method = 'corrdice'
code_dir = '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/msm_merge_files_'+lobe
log_dir = '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/log_higher'
"""================================Pairwise registration according to the dendrogram_'+lobe+'================================"""
# get hierarchy file
merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl' #TODO: change it back to '+lobe+', now is just testing code using frontal lobe

merge = pd.read_pickle(merge_path)

# templates 30
inter_templates = open('../../hierarc_hcp_distcorr/unbias/code_level5/'+lobe+'/template_list_'+simi_method+'/templates_'+lobe+'_30', "r").read().splitlines()

start_index = int(inter_templates[-1][4:])+1


# get leaves for each cluster
cluster_leaf_dict = leaf_in_cluster(merge_path=merge_path)

'''write the actual merging command for templates'''
for j in range(start_index, len(merge)):
# for i in np.asarray([29,37,44,46,47]+list(range(52,len(merge)))): # when need to redo some of them
    i = merge.iloc[[j]].index[0]
    print('merge ID '+ str(i))
    to_merge = merge.loc[[i]]
    A = str(to_merge['subID1'][i])
    B = str(to_merge['subID2'][i])
    combined = str(to_merge['mergeID'][i])
    if A[:4] != 'NODE':
        size_A = 1
    else:
        size_A = int(merge[merge['mergeID']==A]['cluster_size'])
    if B[:4] != 'NODE':
        size_B = 1
    else:
        size_B = int(merge[merge['mergeID']==B]['cluster_size'])


    '''# registration using msm'''
    '''# find the leaf nodes and the leaf nodes for its 2 branches given a combined node'''
    leaf_cluster_combined = cluster_leaf_dict[combined]
    if 'NODE' not in A:
        leaf_cluster_A = np.asarray([A])
    else:
        leaf_cluster_A = cluster_leaf_dict[A]
    if 'NODE' not in B:
        leaf_cluster_B = np.asarray([B])
    else:
        leaf_cluster_B = cluster_leaf_dict[B]

    """msm_reg bash creation"""
    msm_reg(A, B, combined,
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/hierarch_reg_process/',
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/',
            work_dir = '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/',
            sub_dir = '/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/',
            inter_templates=inter_templates,
            leaf_A=leaf_cluster_A,leaf_B=leaf_cluster_B,leaf_combine=leaf_cluster_combined,lobe=lobe)


""" cases can be merged in the same level"""
merge_higher_level = merge.iloc[start_index:]
merge_sort = merge_higher_level.sort_values(by='cluster_size')
levels = merge_sort['cluster_size'].unique()
num_levels = []
l=0 # level id
done_nodes = np.asarray([0])

# start record the QID for each job
main_code = open('msm_merge_files_'+lobe+'/submit_pairwise.sh','w') #TODO: later change the permission for this code

while done_nodes[0] != merge.iloc[-1]['mergeID']:
    num = 0
    done_nodes = np.asarray([]) # node doing in the current level
    f = open('msm_merge_files_'+lobe+'/level' + str(l) + '_list.txt', "w")
    for i in range(len(merge_sort)):
        merge_sort_sub = merge_sort.iloc[i]
        new_node = merge_sort_sub['mergeID']
        subA = str(merge_sort_sub['subID1'])
        subB = str(merge_sort_sub['subID2'])
        if (subA not in done_nodes) & (subB not in done_nodes):
            f.write(new_node + '\n')
            done_nodes = np.append(done_nodes,new_node)
            num = num+1
        else:
            f.close()
            # generate queue code for nan server
            q = open('msm_merge_files_'+lobe+'/queue' + str(l) + '.sh', "w")
            q.write(
                '#!/bin/bash -l\n'
                '#SBATCH --job-name=level' + str(l) + '\n'
                '#SBATCH --output=output.array.%A.%a\n'
                '#SBATCH --array=0-'+str(num-1)+'\n'
                '#SBATCH --nodes=2\n'
                '#SBATCH --chdir='+log_dir+'\n'
                '#SBATCH --mem-per-cpu=4000\n'
                '#SBATCH --time=0-10:00\n'
                'module load openblas\n'
                'SAMPLE_LIST=($(<'+code_dir+'/level' + str(l) + '_list.txt))\n'
                'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                'bash '+code_dir+'/msm_merge_${SAMPLE}.sh;\n'
            )
            q.close()

            if l<1:
                main_code.write(
                    'QID0_1=$(sbatch -p cpu '+code_dir+'/queue' + str(l) + '.sh)\n'
                    'QID0_1_id=$(echo ${QID0_1} | sed -n -e \'s/^.*job //p\')\n'
                )
            else:
                main_code.write(
                    'QID0_1=$(sbatch -p cpu -d $QID0_1_id '+code_dir+'/queue' + str(l) + '.sh)\n'
                    'QID0_1_id=$(echo ${QID0_1} | sed -n -e \'s/^.*job //p\')\n'
                )

            merge_sort = merge_sort.iloc[i:]
            l += 1
            num_levels.append(num)

            break

f.close()
# queue.for node 1108
q = open('msm_merge_files_'+lobe+'/queue' + str(l) + '.sh', "w")
q.write(
    '#!/bin/bash -l\n'
    '#SBATCH --job-name=level' + str(l) + '\n'
    '#SBATCH --output=output.array.%A.%a\n'
    '#SBATCH --array=0-'+str(num-1)+'\n'
    '#SBATCH --chdir='+log_dir+'\n'
    '#SBATCH --mem-per-cpu=8000\n'
    '#SBATCH --time=0-10:00\n'
    'module load openblas\n'
    'SAMPLE_LIST=($(<'+code_dir+'/level' + str(l) + '_list.txt))\n'
    'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
    'bash '+code_dir+'/msm_merge_${SAMPLE}.sh;\n'
)
q.close()

main_code.write(
    'QID0_1=$(sbatch -p cpu -d $QID0_1_id '+code_dir+'/queue' + str(l) + '.sh)\n'
    'QID0_1_id=$(echo ${QID0_1} | sed -n -e \'s/^.*job //p\')\n'
)

main_code.close()
num_levels.append(num)


print('Hierarchical running structure set!')