"""
Given the hierarchy, pairwise merge until the registration done.
A version for generation grid for registration issue

the start point is sulc affined to msmsulc template
//1. pairwise affine(rotation) register subject within one cluster, and average the transformation to create a unbias registration for template. The pairwise registration was based on sulcal depth
//2. apply unbias transformation for every subject

> because the subjects are already rigidly registered to msmsulc template, skip the part of pairwise affine. Directly average and create template 0
3. average the transformed subject with in clusters to form sulc template 0
4. sulcal depth at start point register to sulc template 0 using MSM_strain
--- --- --- start the iteration
5. curvature at start point apply the warp of MSMstrain output
6. average the deformed curvature -> create new curvature template
7. curvature at start point apply the warp of new curvature template (done by MSM transformed and projected)
8. average the deformed curvature -> create new curvature template
9. calculate the difference of curvature template in frontal lobe (or other masks in later step)
iterate between


run
queue_sulctemp0.sh
queue_sulctemp1_reg.sh

create folders
log
msm_config
corrdice_affine_mask save process for each template

"""

import pandas as pd
from utils.wbtools_light import msm_reg_template_2,generate_average_metric_command_unbiastemp,generate_average_metric_command,curv_warp_to_sulc#,modify_sphere
from main5_levelstep.HPC_working_dir.main5_1_template_generation.get_clusters_with_thre import leaf_in_cluster

level = 0
lobe = 'frontal'
simi_method = 'corrdice'
create_work_dir = '/HPC_work_dir'
converge_thre=0.005
total_iter_num=10

"""================================ iterative registration to 30 cluster templates================================"""
'''load in the merge process files'''
merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'


merge_file = pd.read_pickle(merge_path)

"""get entire hierarchy or partial hierarchy"""
merge = merge_file  # entire hierarchy
# merge = merge_example

cluster_leaf_dict = leaf_in_cluster(merge_path=merge_path) # get leaf dictionary for each node

inter_templates = open('code_level5/'+lobe+'_save/template_list_'+simi_method+'/templates_'+lobe+'_30', "r").read().splitlines()




'''3. average the transformed subject with in clusters to create sulc template 0'''
f_templist = open('code_level5/code_pairwise_'+simi_method+'/templates_'+lobe+'_30','w')

for temp in inter_templates:

    if 'NODE' in temp:  # exclude the individual subject not in any cluster in this level
        f_templist.write(temp+'\n')

        with open('code_level5/code_pairwise_'+simi_method+'/code_sulctemp0_' + temp + '.sh', 'w') as output_sulctemp0:
            # add the leaves for this template, affined sulc path, merged ID, and output path, will output an averaged sulc.
            output_sulctemp0.write(generate_average_metric_command_unbiastemp(cluster_leaf_dict[temp],
                                                                          '/HPC_work_dir/affined_sulc',
                                                                          root_suffix='.sulc.affine.ico6.shape.gii',
                                                                          merge_id=temp,
                                                                          output_path=create_work_dir+'/'+simi_method+'_affine_mask',
                                                                          output_suffix='.sulctemp0.affine.ico6.shape.gii'
                                                                          ))
f_templist.close()


# write the queue, process all 30+ templates in parallel
with open("code_level5/code_pairwise_"+simi_method+"/queue_sulctemp0.sh", "w") as output:
    output.write(
        '#!/bin/bash -l' + '\n'
        '#SBATCH --job-name=sulctemp\n'
        '#SBATCH --output=output.array.%A.%a' + '\n'
        '#SBATCH --array=0-' + str(len(inter_templates) - 1) + '\n'
        '#SBATCH --chdir=' + create_work_dir + '/log' + '\n'
        '#SBATCH --mem-per-cpu=8000' + '\n'
        '#SBATCH --time=0-1:00' + '\n'
        'module load openblas' + '\n'
        'SAMPLE_LIST=($(<' + create_work_dir + '/code_pairwise_'+simi_method+'/templates_'+lobe+'_30))' + '\n'
        'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}' + '\n'
        'bash ' + create_work_dir + '/code_pairwise_'+simi_method+'/code_sulctemp0_${SAMPLE}.sh' + '\n')




'''warp the sulc map according to the final warp of curvature !!!this step is after the iteration'''
curv_warp_to_sulc(create_work_dir,simi_method)

# get the moving list and target list (reg subjects to their folding templates)
f_sub = open('code_level5/code_pairwise_'+simi_method+'/sulcreg_move_list','w')
f_sub_tar = open('code_level5/code_pairwise_'+simi_method+'/sulcreg_tar_list','w')

for temp in inter_templates:
    if 'NODE' in temp: # exclude the individual subject not in any cluster in this level
        for n, sub in enumerate(cluster_leaf_dict[temp]): # subjects in this cluster
            f_sub.write(sub+'\n')
            f_sub_tar.write(temp+'\n')
f_sub.close()
f_sub_tar.close()

mov_list = open('code_level5/code_pairwise_'+simi_method+'/sulcreg_move_list').read().splitlines()
f_queue_pairwise = open('code_level5/code_pairwise_'+simi_method+'/queue_applywarp_sulc.sh','w')
f_queue_pairwise.write(
    '#!/bin/bash -l'+'\n'
    '#SBATCH --job-name=warpsulc\n'
    '#SBATCH --output=output.array.%A.%a'+'\n'
    '#SBATCH --array=0-'+str(len(mov_list)-1)+'\n'
    '#SBATCH --nodes=1\n'
    '#SBATCH --chdir='+create_work_dir+'/log'+'\n'
    '#SBATCH --mem-per-cpu=3000'+'\n'
    '#SBATCH --time=0-2:00'+'\n'
    '#SBATCH --mail-user=yourong.guo@kcl.ac.uk\n'
    '\n'
    'module load openblas'+'\n'
    'SAMPLE_LIST=($(<'+create_work_dir+'/code_pairwise_'+simi_method+'/sulcreg_move_list))'+'\n'
    'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}'+'\n'
    'TAR_LIST=($(<'+create_work_dir+'/code_pairwise_'+simi_method+'/sulcreg_tar_list))'+'\n'
    'TAR=${TAR_LIST[${SLURM_ARRAY_TASK_ID}]}'+'\n'
    'bash '+create_work_dir+'/code_pairwise_'+simi_method+'/apply_warp_to_sulc.sh -m ${SAMPLE} -t ${TAR}\n'
)
f_queue_pairwise.close()

'''merge the warped sulc to generate final sulc templates'''
for temp in inter_templates:

    if 'NODE' in temp:  # exclude the individual subject not in any cluster in this level

        with open('code_level5/code_pairwise_'+simi_method+'/code_sulctemp1_' + temp + '.sh', 'w') as output_sulctemp0:
            # add the leaves for this template, affined sulc path, merged ID, and output path, will output an averaged sulc.
            output_sulctemp0.write(generate_average_metric_command_unbiastemp(cluster_leaf_dict[temp],
                                                                          create_work_dir+'/'+simi_method+'_affine_mask/check'+temp+'_msmrefine',
                                                                          root_suffix='.MSM.'+temp+'.final.sulc.shape.gii',
                                                                          merge_id=temp,
                                                                          output_path=create_work_dir+'/'+simi_method+'_affine_mask',
                                                                          output_suffix='.sulctemp1.affine.ico6.shape.gii'
                                                                          ))


# write the queue, process all 30+ templates in parallel
with open("code_level5/code_pairwise_"+simi_method+"/queue_sulctemp1.sh", "w") as output:
    output.write(
        '#!/bin/bash -l' + '\n'
        '#SBATCH --job-name=sulctemp\n'
        '#SBATCH --output=output.array.%A.%a' + '\n'
        '#SBATCH --array=0-' + str(len(inter_templates) - 1) + '\n'
        '#SBATCH --chdir=' + create_work_dir + '/log' + '\n'
        '#SBATCH --mem-per-cpu=8000' + '\n'
        '#SBATCH --time=0-1:00' + '\n'
        'module load openblas' + '\n'
        'SAMPLE_LIST=($(<' + create_work_dir + '/code_pairwise_'+simi_method+'/templates_'+lobe+'_30))' + '\n'
        'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}' + '\n'
        'bash ' + create_work_dir + '/code_pairwise_'+simi_method+'/code_sulctemp1_${SAMPLE}.sh' + '\n')












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
for temp in inter_templates:
    if 'NODE' in temp:
        total.write('nohup bash submit_code_'+temp+'.sh > log_'+temp+'.txt &\n')
        each=open('code_level5/code_iter_'+simi_method+'/submit_code_'+temp+'.sh','w')

        each.write('#!/bin/bash -l\n'
                    'if  QID0_1=$(sbatch -p cpu '+create_work_dir+'/code_iter_'+simi_method+'/queue_'+temp+'_0.sh 2>&1); then\n'
                    '    QID0_1_id=$(echo ${QID0_1} | sed -n -e \'s/^.*job //p\')\n'
                    '    echo "Job submitted successfully with ID $QID0_1_id"\n'
                    'else\n'
                    '    echo "Job submission failed"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    'if  QID0_2=$(sbatch -p cpu -d $QID0_1_id '+create_work_dir+'/code_iter_'+simi_method+'/queue_merge'+temp+'_0.sh 2>&1); then\n'
                    '    QID0_2_id=$(echo ${QID0_2} | sed -n -e \'s/^.*job //p\')\n'
                    '    echo "Job submitted successfully with ID $QID0_2_id"\n'
                    'else\n'
                    '    echo "Job submission failed"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    '# second registration and second template\n'
                    'if  QID1_1=$(sbatch -p cpu -d $QID0_2_id '+create_work_dir+'/code_iter_'+simi_method+'/queue_'+temp+'_1.sh 2>&1); then\n'
                    '    QID1_1_id=$(echo ${QID1_1} | sed -n -e \'s/^.*job //p\')\n'
                    '    echo "Job submitted successfully with ID $QID1_1_id"\n'
                    'else\n'
                    '    echo "Job submission failed"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    'if  QID1_2=$(sbatch -p cpu -d $QID1_1_id '+create_work_dir+'/code_iter_'+simi_method+'/queue_merge'+temp+'_1.sh 2>&1); then\n'
                    '    QID1_2_id=$(echo ${QID1_2} | sed -n -e \'s/^.*job //p\')\n'
                    '    echo "Job submitted successfully with ID $QID1_2_id"\n'
                    'else\n'
                    '    echo "Job submission failed"\n'
                    '    exit 1\n'
                    'fi\n'
                    '\n'
                    'sleep_time=120 # seconds\n'
                    '# check to see if job is running\n'
                    'status=`squeue -u $USER_NAME | grep $QID1_2_id`\n'
                    '# while $status is not empty\n'
                    'while [ -n "$status" ]\n'
                    '    do\n'
                    '        sleep $sleep_time\n'
                    '        status=`squeue -u $USER_NAME | grep $QID1_2_id`\n'
                    '    done\n'
                    'iter=1\n'
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
                    '    if  QID1_1=$(sbatch -p cpu '+create_work_dir+'/code_iter_'+simi_method+'/queue_'+temp+'_${iter}.sh 2>&1); then\n'
                    '        QID1_1_id=$(echo ${QID1_1} | sed -n -e \'s/^.*job //p\')\n'
                    '        echo "Job submitted successfully with ID $QID1_1_id"\n'
                    '    else\n'
                    '        echo "Job submission failed"\n'
                    '        exit 1\n'
                    '    fi\n'
                    '\n'
                    '    if  QID1_2=$(sbatch -p cpu -d $QID1_1_id '+create_work_dir+'/code_iter_'+simi_method+'/queue_merge'+temp+'_${iter}.sh 2>&1); then\n'
                    '        QID1_2_id=$(echo ${QID1_2} | sed -n -e \'s/^.*job //p\')\n'
                    '        echo "Job submitted successfully with ID $QID1_2_id"\n'
                    '    else\n'
                    '        echo "Job submission failed"\n'
                    '        exit 1\n'
                    '    fi\n'
                    '\n'
                    '    echo "iter ${iter}: job submitted!"\n'
                    '    # check to see if job is running\n'
                    '    status=`squeue -u $USER_NAME | grep $QID1_2_id`\n'
                    '    # while $status is not empty\n'
                    '    while [ -n "$status" ]\n'
                    '        do\n'
                    '            sleep $sleep_time\n'
                    '            status=`squeue -u $USER_NAME | grep $QID1_2_id`\n'
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




# print('Hierarchical running structure set!')



