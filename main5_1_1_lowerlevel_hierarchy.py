import numpy as np
import pickle

import pandas as pd

from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
from wbtools_light_subtemp import msm_reg_template_2,generate_average_metric_command_unbiastemp,generate_average_metric_command,curv_warp_to_sulc


lobe = 'parietal'
simi_method = 'corrdice'
partition = 'cpu'
n_hemi = 2220
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'
sub_cluster_size = 25
create_work_dir='/scratch/prj/cortical_imaging/Yourong/hierarch/'+lobe+'_lobe/subtemps'
total_iter_num = 20
converge_thre = 0.006

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

temp_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True) ### frontal corrdice 0.38  ### parietal corrdice 0.477  ### temporal corrdice 0.365

cluster_leaf_dict = leaf_in_cluster(merge_path)



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
    nodes2, chain2 = break_down_node(sub2, df, max_size,min_size, chain.copy())

    # Combine results
    return nodes1 + nodes2, chain1 + chain2


# Example: Break down NODE2186
# final_nodes, node_chain = break_down_node('NODE2186', merge_path_df)


'''
for every cluster larger than sub_cluster_size break it down 
until they are smaller then sub_cluster_size
return their breakdown nodes.
'''
# subtemp_cnt = 0
final_node_all = []
for temp in temp_30:
    if len(cluster_leaf_dict[temp]) > 35:
        final_nodes, _ = break_down_node(temp, merge_path_df)
        final_node_all.append(final_nodes)
        # subtemp_cnt+=len(final_nodes)

subtemp_all = []
for final_node in final_node_all:
    for subtemp in final_node:
        subtemp_all.append(subtemp)


inter_templates = subtemp_all



'''average the transformed subject with in clusters to create sulc template 0'''
f_templist = open('code_level5/code_pairwise_'+simi_method+'/subtemplates_'+lobe,'w')

for temp in inter_templates:

    if 'NODE' in temp:  # exclude the individual subject not in any cluster in this level
        f_templist.write(temp+'\n')

        # first sulc temp
        with open('code_level5/code_pairwise_'+simi_method+'/code_sulctemp0_' + temp + '.sh', 'w') as output_sulctemp0:
            # add the leaves for this template, affined sulc path, merged ID, and output path, will output an averaged sulc.
            output_sulctemp0.write(generate_average_metric_command_unbiastemp(cluster_leaf_dict[temp],
                                                                          '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/affined_sulc',
                                                                          root_suffix='.sulc.affine.ico6.shape.gii',
                                                                          merge_id=temp,
                                                                          output_path=create_work_dir+'/'+simi_method+'_affine_mask',
                                                                          output_suffix='.sulctemp0.affine.ico6.shape.gii'
                                                                          ))
        # final sulc temp
        with open('code_level5/code_pairwise_'+simi_method+'/code_sulctemp_final_' + temp + '.sh', 'w') as output_sulctemp1:
            # add the leaves for this template, affined sulc path, merged ID, and output path, will output an averaged sulc.
            output_sulctemp1.write(generate_average_metric_command_unbiastemp(cluster_leaf_dict[temp],
                                                                          create_work_dir+'/'+simi_method+'_affine_mask/check'+temp+'_msmrefine',
                                                                          root_suffix='.MSM.'+temp+'.final.sulc.shape.gii',
                                                                          merge_id=temp,
                                                                          output_path=create_work_dir+'/'+simi_method+'_affine_mask',
                                                                          output_suffix='.sulctemp1.affine.ico6.shape.gii'
                                                                          ))
f_templist.close()


# write the queue, process all 30+ templates in parallel
with open("code_level5/code_pairwise_"+simi_method+"/queue_sulctemp0.sh", "w") as output:
    output.write(
        '#!/bin/bash -l' + '\n'
        '#SBATCH --job-name=sulctemp\n'
        '#SBATCH --output=output.array.%A.%a.out' + '\n'
        '#SBATCH --array=0-' + str(len(inter_templates) - 1) + '\n'
        '#SBATCH --chdir=' + create_work_dir + '/log' + '\n'
        '#SBATCH --mem-per-cpu=3000' + '\n'
        '#SBATCH --time=0-0:10' + '\n'
        'module load openblas' + '\n'
        'SAMPLE_LIST=($(<' + create_work_dir + '/code_pairwise_'+simi_method+'/subtemplates_'+lobe+'))' + '\n'
        'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}' + '\n'
        'create_work_dir='+create_work_dir+'\n'
        'target_path="${create_work_dir}/corrdice_affine_mask/check${SAMPLE}_msmrefine"\n'
        '# Check if the target file or directory exists\n'
        'if [ -e "$target_path" ]; then\n'
        '    echo "Target path $target_path already exists. Exiting script."\n'
        '    exit 0\n'
        'fi\n'
        'bash ' + create_work_dir + '/code_pairwise_'+simi_method+'/code_sulctemp0_${SAMPLE}.sh' + '\n')

# write the queue, process all 30+ templates in parallel
with open("code_level5/code_pairwise_"+simi_method+"/queue_sulctemp_final.sh", "w") as output:
    output.write(
        '#!/bin/bash -l' + '\n'
        '#SBATCH --job-name=sulctemp\n'
        '#SBATCH --output=output.array.%A.%a.out' + '\n'
        '#SBATCH --array=0-' + str(len(inter_templates) - 1) + '\n'
        '#SBATCH --chdir=' + create_work_dir + '/log' + '\n'
        '#SBATCH --mem-per-cpu=3000' + '\n'
        '#SBATCH --time=0-0:05' + '\n'
        'module load openblas' + '\n'
        'SAMPLE_LIST=($(<' + create_work_dir + '/code_pairwise_'+simi_method+'/subtemplates_'+lobe+'))' + '\n'
        'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}' + '\n'
        'create_work_dir='+create_work_dir+'\n'
        'target_path="${create_work_dir}/corrdice_affine_mask/check${SAMPLE}_msmrefine/${SAMPLE}.final.sulc.affine.ico6.shape.gii"\n'
        '# Check if the target file or directory exists\n'
        'if [ -f "$target_path" ]; then\n'
        '    echo "Target path $target_path already exists. Exiting script."\n'
        '    exit 0\n'
        'fi\n'
        'bash ' + create_work_dir + '/code_pairwise_'+simi_method+'/code_sulctemp_final_${SAMPLE}.sh' + '\n')



# get the moving list and target list (reg subjects to their folding templates)
f_sub = open('code_level5/code_pairwise_'+simi_method+'/sulcreg_move_list','w')
f_sub_tar = open('code_level5/code_pairwise_'+simi_method+'/sulcreg_tar_list','w')
sulcreg_move_list = []
sulcreg_tar_list = []
cnt = 0
for temp in inter_templates:
    if 'NODE' in temp: # exclude the individual subject not in any cluster in this level
        for n, sub in enumerate(cluster_leaf_dict[temp]): # subjects in this cluster
            f_sub.write(sub+'\n')
            cnt+=1
            f_sub_tar.write(temp+'\n')
            sulcreg_move_list.append(sub)
            sulcreg_tar_list.append(temp)
f_sub.close()
f_sub_tar.close()

subject_first_templates = pd.DataFrame(np.concatenate((np.asarray(sulcreg_move_list).reshape(-1,1),np.asarray(sulcreg_tar_list).reshape(-1,1)), axis=1), columns=['subjects','templates'])

subject_first_templates.to_csv(f'subject_firsttemp_subtemps_{lobe}.csv', index=False, index_label=None)


"""-------------------------------------------------------------------------------------------------
30s iter for curvature would be ok? but difference of templates <0.007
order: parallel registration -> merge -> parallel registration -> merge -> parallel registration...
----------------------------------------------------------------------------------------------------
"""

for iter_num in range(2): # first iteration is different from the later iterations
    if iter_num == 0:
        firstreg = 1
    else:
        firstreg = 0

    #  registration code for each subjects, different from first iteration to later iterations
    msm_reg_template_2(create_work_dir, firstreg, iter_num, lobe,simi_method)

    for temp in inter_templates:
        if 'NODE' in temp:
            leaves = cluster_leaf_dict[temp]

            """write wb_command -metric-math for each iteration"""
            with open("code_level5/code_iter_"+simi_method+"/metric_merge_" + temp + '_'+str(iter_num)+".sh", "w") as output:
                command, output_file = generate_average_metric_command(leaves,
                                                create_work_dir + '/'+simi_method+'_affine_mask/check' + temp + '_msmrefine/',
                                                temp,
                                                create_work_dir + '/'+simi_method+'_affine_mask/check' + temp + '_msmrefine/',
                                                '_${iter_num}.transformed_and_reprojected.func.gii',
                                                firstreg=firstreg, iter_num=iter_num, lobe=lobe,
                                                create_work_dir=create_work_dir,
                                                simi_method = simi_method)
                output.write(command+'\n')
                # copy the latest template as final template
                output.write('cp '+output_file+' '+create_work_dir+'/'+simi_method+'_affine_mask/check' + temp + '_msmrefine/'+''+temp+ '.final.curv.affine.ico6.shape.gii\n')



"""write command for parallel run for each iteration"""
for iter_num in range(total_iter_num):  # first iteration is different from the later iterations

    for temp in inter_templates:
        if 'NODE' in temp:
            leaves = cluster_leaf_dict[temp]

            """write subject list for a temp"""
            with open("code_level5/code_iter_"+simi_method+"/cluster_reg_"+temp+".txt", "w") as output:
                for leaf in leaves:
                    output.write(str(leaf)+'\n')  # run these leaves altogether in parallel manner TODO: maybe 1108 leaves all run in parallel

            # with open("code_level5/code_iter_'+simi_method+'/cluster_merge_" + temp + '_' + str(iter_num) + ".txt", "w") as output:
            #     output.write(create_work_dir+'/code_iter_'+simi_method+'/metric_merge_'+temp+'_'+str(iter_num)+'.sh\n')

            if iter_num == 0:
                """write queue parallel run for REG"""
                with open("code_level5/code_iter_"+simi_method+"/queue_" + temp + '_' + str(iter_num) + ".sh","w") as output:
                    output.write(
                        '#!/bin/bash -l' + '\n'
                        '#SBATCH --job-name=reg_' + temp + '\n'
                        '#SBATCH --output=output.array.%A.%a' + '\n'
                        '#SBATCH --array=0-' + str(len(leaves) - 1) + '\n'
                        '#SBATCH --nodes=1\n'
                        '#SBATCH --chdir=' + create_work_dir + '/log' + '\n'
                        '#SBATCH --mem-per-cpu=4000' + '\n'
                        '#SBATCH --time=0-24:00' + '\n'
                        'module load openblas' + '\n'
                        'SAMPLE_LIST=($(<' + create_work_dir + '/code_iter_'+simi_method+'/cluster_reg_'+temp+'.txt))' + '\n'
                        'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}' + '\n'
                        'bash ' + create_work_dir + '/code_iter_'+simi_method+'/msm_inter_refine_0.sh -m ${SAMPLE} -t ' + temp + '\n')

                """write queue parallel run for MERGE"""
                with open("code_level5/code_iter_"+simi_method+"/queue_merge" + temp + '_' + str(iter_num) + ".sh", "w") as output:
                    output.write(
                        '#!/bin/bash -l' + '\n'
                        '#SBATCH --job-name=merge_'+temp+ '\n'
                        '#SBATCH --output=output.array.%A.%a' + '\n'
                        '#SBATCH --array=0-0' + '\n'
                        '#SBATCH --nodes=1\n'
                        '#SBATCH --chdir='+create_work_dir+'/log' + '\n'
                        '#SBATCH --mem-per-cpu=4000' + '\n'
                        '#SBATCH --time=0-3:00' + '\n'
                        'module load openblas' + '\n'
                        'bash ' + create_work_dir + '/code_iter_'+simi_method+'/metric_merge_' + temp + '_0.sh -n ' + str(iter_num) + '\n')

            else:
                """write queue parallel run for REG"""
                with open("code_level5/code_iter_"+simi_method+"/queue_" + temp + '_' + str(iter_num) + ".sh", "w") as output:
                    output.write(
                        '#!/bin/bash -l'+'\n'
                        '#SBATCH --job-name=reg_'+temp+'\n'
                        '#SBATCH --output=output.array.%A.%a'+'\n'
                        '#SBATCH --array=0-'+str(len(leaves)-1)+'\n'
                        '#SBATCH --nodes=1\n'
                        '#SBATCH --chdir='+create_work_dir+'/log'+'\n'
                        '#SBATCH --mem-per-cpu=4000'+'\n'
                        '#SBATCH --time=0-24:00'+'\n'
                        'module load openblas'+'\n'
                        'SAMPLE_LIST=($(<'+create_work_dir+'/code_iter_'+simi_method+'/cluster_reg_'+temp+'.txt))'+'\n'
                        'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}'+'\n'
                        'bash ' + create_work_dir + '/code_iter_'+simi_method+'/msm_inter_refine_1.sh -n '+str(iter_num)+' -m ${SAMPLE} -t ' + temp + '\n')

                """write queue parallel run for MERGE"""
                with open("code_level5/code_iter_"+simi_method+"/queue_merge" + temp + '_' + str(iter_num) + ".sh", "w") as output:
                    output.write(
                        '#!/bin/bash -l' + '\n'
                        '#SBATCH --job-name=merge_'+temp+ '\n'
                        '#SBATCH --output=output.array.%A.%a' + '\n'
                        '#SBATCH --array=0-0' + '\n'
                        '#SBATCH --nodes=1\n'
                        '#SBATCH --chdir='+create_work_dir+'/log' + '\n'
                        '#SBATCH --mem-per-cpu=4000' + '\n'
                        '#SBATCH --time=0-3:00' + '\n'
                        'module load openblas' + '\n'
                        'bash ' + create_work_dir + '/code_iter_'+simi_method+'/metric_merge_' + temp + '_1.sh -n ' + str(iter_num) + '\n')



'''create submit code_for every cluster template'''
total=open("code_level5/code_iter_"+simi_method+"/submit_total_list.txt", "w")

#TODO: QID_2=$(echo ${QID} | sed -n -e 's/^.*job //p')
for cnt, temp in enumerate(inter_templates):
    # Change partition every 10 iterations
    if cnt % 10 == 0 and cnt != 0:
        if partition == "cpu":
            partition = "robinson_gpu"
        else:
            partition = "cpu"
    if 'NODE' in temp:
        total.write('nohup bash submit_code_'+temp+'.sh > log_'+temp+'.txt &\n')
        each=open('code_level5/code_iter_'+simi_method+'/submit_code_'+temp+'.sh','w')


        each.write('#!/bin/bash -l\n'
                   'create_work_dir='+create_work_dir+'\n'
                   'target_path="${create_work_dir}/corrdice_affine_mask/check'+temp+'_msmrefine/'+temp+'.final.curv.affine.ico6.shape.gii"\n'
                    '# Check if the target file or directory exists\n'
                    'if [ -f "$target_path" ]; then\n'
                    '    echo "Target path $target_path already exists. Exiting script."\n'
                    '    exit 0\n'
                    'fi\n'
                   
                    'if  QID0_1=$(sbatch -p '+partition+' '+create_work_dir+'/code_iter_'+simi_method+'/queue_'+temp+'_0.sh 2>&1); then\n'
                    '    QID0_1_id=$(echo ${QID0_1} | sed -n -e \'s/^.*job //p\')\n'
                    '    echo "Job submitted successfully with ID $QID0_1_id"\n'
                    'else\n'
                    '    echo "Job submission failed"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    'if  QID0_2=$(sbatch -p '+partition+' -d $QID0_1_id '+create_work_dir+'/code_iter_'+simi_method+'/queue_merge'+temp+'_0.sh 2>&1); then\n'
                    '    QID0_2_id=$(echo ${QID0_2} | sed -n -e \'s/^.*job //p\')\n'
                    '    echo "Job submitted successfully with ID $QID0_2_id"\n'
                    'else\n'
                    '    echo "Job submission failed"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    '# second registration and second template\n'
                    'if  QID1_1=$(sbatch -p '+partition+' -d $QID0_2_id '+create_work_dir+'/code_iter_'+simi_method+'/queue_'+temp+'_1.sh 2>&1); then\n'
                    '    QID1_1_id=$(echo ${QID1_1} | sed -n -e \'s/^.*job //p\')\n'
                    '    echo "Job submitted successfully with ID $QID1_1_id"\n'
                    'else\n'
                    '    echo "Job submission failed"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    'if  QID1_2=$(sbatch -p '+partition+' -d $QID1_1_id '+create_work_dir+'/code_iter_'+simi_method+'/queue_merge'+temp+'_1.sh 2>&1); then\n'
                    '    QID1_2_id=$(echo ${QID1_2} | sed -n -e \'s/^.*job //p\')\n'
                    '    echo "Job submitted successfully with ID $QID1_2_id"\n'
                    'else\n'
                    '    echo "Job submission failed"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    'sleep_time=300 # seconds\n'
                    '# check to see if job is running\n'
                    'status=`squeue -u k21065258 | grep $QID1_2_id`\n'
                    '# while $status is not empty\n'
                    'while [ -n "$status" ]\n'
                    '    do\n'
                    '        sleep $sleep_time\n'
                    '        status=`squeue -u k21065258 | grep $QID1_2_id`\n'
                    '    done\n'
                    '\n'
                    'iter=1\n'
                    'sleep $sleep_time\n'
                    'diff=$(tail -n 1 '+create_work_dir+'/log/output.array.${QID1_2_id}.0)\n'
                    'echo "diff: ${diff}"\n'
                    'thre='+str(converge_thre)+'\n'
                    'while [ `echo "$diff > $thre" | bc` -eq 1 ]\n'
                    '    do\n'
                    '    # do registration if the difference map is greater than '+str(converge_thre)+'\n'
                    '    ((iter++))\n'
                    '    echo "iter: ${iter} start"\n'
                    '\n'
                    '\n'
                    '\n'
                    '    if  QID1_1=$(sbatch -p '+partition+' '+create_work_dir+'/code_iter_'+simi_method+'/queue_'+temp+'_${iter}.sh 2>&1); then\n'
                    '        QID1_1_id=$(echo ${QID1_1} | sed -n -e \'s/^.*job //p\')\n'
                    '        echo "Job submitted successfully with ID $QID1_1_id"\n'
                    '    else\n'
                    '        echo "Job submission failed"\n'
                    '        exit 1\n'
                    '    fi\n'
                    '\n'
                    '    if  QID1_2=$(sbatch -p '+partition+' -d $QID1_1_id '+create_work_dir+'/code_iter_'+simi_method+'/queue_merge'+temp+'_${iter}.sh 2>&1); then\n'
                    '        QID1_2_id=$(echo ${QID1_2} | sed -n -e \'s/^.*job //p\')\n'
                    '        echo "Job submitted successfully with ID $QID1_2_id"\n'
                    '    else\n'
                    '        echo "Job submission failed"\n'
                    '        exit 1\n'
                    '    fi\n'
                    '\n'
                    '    echo "iter ${iter}: job submitted!"\n'
                    '    # check to see if job is running\n'
                    '    status=`squeue -u k21065258 | grep $QID1_2_id`\n'
                    '    # while $status is not empty\n'
                    '    while [ -n "$status" ]\n'
                    '        do\n'
                    '            sleep $sleep_time\n'
                    '            status=`squeue -u k21065258 | grep $QID1_2_id`\n'
                    '        done\n'
                    '    # update diff\n'
                    '    sleep $sleep_time\n'
                    '    diff=$(tail -n 1 '+create_work_dir+'/log/output.array.${QID1_2_id}.0)\n'
                    '    echo "diff: ${diff}"\n'
                    '    echo "iter: ${iter} done"\n'
                    '    done\n'
                    'echo "iteration finished!"'

                   )
        each.close()
total.close()







