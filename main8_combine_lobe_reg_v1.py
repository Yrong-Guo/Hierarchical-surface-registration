'''
concatenate between-templates registration together
'''

import numpy as np
from utils.hierarch_tools import leaf_in_cluster, hierarch_path_dict
from utils.concatenate_function import concatenate_warps
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
import pandas as pd

'''settings'''
simi_method = 'corrdice'
log_dir = '/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/log'
code_dir='/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code'

subject_firsttemp = pd.read_csv('subject_first_templates/subject_firsttemp.csv')
subject_firsttemp_uq3 = subject_firsttemp[['frontal','temporal','parietal']].drop_duplicates()
subject_firsttemp_uq2 = subject_firsttemp[['frontal','temporal']].drop_duplicates()

subject_firsttemp_uq2['frontal'].to_csv('concate_bashcode/lobe2_frontal', sep='\n', index=False, header=False)
subject_firsttemp_uq2['temporal'].to_csv('concate_bashcode/lobe2_temporal', sep='\n', index=False, header=False)
subject_firsttemp_uq3['frontal'].to_csv('concate_bashcode/lobe3_frontal', sep='\n', index=False, header=False)
subject_firsttemp_uq3['temporal'].to_csv('concate_bashcode/lobe3_temporal', sep='\n', index=False, header=False)
subject_firsttemp_uq3['parietal'].to_csv('concate_bashcode/lobe3_parietal', sep='\n', index=False, header=False)

'''------------------------------------------Frontal lobe------------------------------------------------'''

lobe = 'frontal'
merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'

# check 30 template threshold
if simi_method == 'corrdice':
    if lobe == 'frontal':
        cluster_thre = 0.38
    elif lobe == 'parietal':
        cluster_thre = 0.477
    elif lobe == 'temporal':
        cluster_thre = 0.365

### TODO:frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
# get threshold template
temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )

'''get hierarchical path'''
# node - higher level path
cluster_hie_dict = hierarch_path_dict(temps_30,merge_path)
# merge table
merge = pd.read_pickle(merge_path)
# cluster - subjects in
cluster_subject = leaf_in_cluster(merge_path)
merge_higher = merge[merge['distance']>cluster_thre]

# higher level registration in parallel
f_mov = open('concate_bashcode/'+lobe+'_temp_move_list','w')
f_tar = open('concate_bashcode/'+lobe+'_temp_tar_list','w')

for ind in merge_higher.index:

    # '''from temp to temp''' TODO: concatenate in a reversed order of hierarchy
    f_mov.write(merge_higher.loc[ind]['subID1']+'\n')
    f_mov.write(merge_higher.loc[ind]['subID2']+'\n')
    f_tar.write(merge_higher.loc[ind]['mergeID']+'\n')
    f_tar.write(merge_higher.loc[ind]['mergeID']+'\n')
f_mov.close()
f_tar.close()


f_queue_reg = open('concate_bashcode/queue_reg_temps_' + lobe + '.sh', 'w')
f_queue_reg.write('#!/bin/bash -l\n'
                    '#SBATCH --job-name=reg_temp\n'
                    '#SBATCH --output=output.array.%A.%a.out\n'
                    '#SBATCH --array=0-' + str(len(merge_higher) * 2 - 1) + '\n'
                    '#SBATCH --nodes=1\n'
                    '#SBATCH --chdir=' + log_dir + '\n'
                    '#SBATCH --mem-per-cpu=4000\n'
                    '#SBATCH --time=0-3:00\n'
                    'module load openblas\n'
                    'MOVE_LIST=($(<' + code_dir + '/' + lobe + '_temp_move_list))\n'
                    'MOV=${MOVE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'TAR_LIST=($(<' + code_dir + '/' + lobe + '_temp_tar_list))\n'
                    'TAR=${TAR_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'newmsm --inmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                    '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                    '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${MOV}.curv.affine.ico6.shape.gii '
                    '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR}.curv.affine.ico6.shape.gii '
                    '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_' + lobe + '_mask_dil.shape.gii '
                    '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_' + lobe + '_mask_dil.shape.gii '
                    '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/' + lobe + '.${MOV}.MSM.${TAR}. '
                    '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_concate;'
                    )
f_queue_reg.close()


'''concatenate code - -dont need to modify sphere not much distortion'''
for node in temps_30:

    hierarchical_path = cluster_hie_dict[node]

    f_concate = open('concate_bashcode/concate_temp'+node+'_'+lobe+'.sh','w')
    f_concate.write('process_folder=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n'
                    'ico_6=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii\n'
                    'output_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n')

    for i, sub_temp in enumerate(hierarchical_path):
        if i == 1 :
            f_concate.write('wb_command -surface-sphere-project-unproject ${process_folder}/'+lobe+'.'+node+'.MSM.'+hierarchical_path[i-1]+'.sphere.reg.surf.gii ${ico_6} ${process_folder}/'+lobe+'.'+hierarchical_path[i-1]+'.MSM.'+hierarchical_path[i]+'.sphere.reg.surf.gii ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii\n')
        elif (i > 1) & (i < (len(hierarchical_path)-1)):
            f_concate.write('wb_command -surface-sphere-project-unproject ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i-1]+'.sphere.concate.surf.gii ${ico_6} ${process_folder}/'+lobe+'.'+hierarchical_path[i-1]+'.MSM.'+hierarchical_path[i]+'.sphere.reg.surf.gii ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii\n')
        elif i == (len(hierarchical_path)-1):
            f_concate.write('wb_command -surface-sphere-project-unproject ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i-1]+'.sphere.concate.surf.gii ${ico_6} ${process_folder}/'+lobe+'.'+hierarchical_path[i-1]+'.MSM.'+hierarchical_path[i]+'.sphere.reg.surf.gii ${output_dir}/'+lobe+'_'+node+'.sphere.concate.surf.gii\n')
f_concate.close()


f_queue_concate = open('concate_bashcode/queue_concate_temps_'+lobe+'.sh','w')
f_queue_concate.write('#!/bin/bash -l\n'
                    '#SBATCH --job-name=conc_temp\n'
                    '#SBATCH --output=output.array.%A.%a.out\n'
                    '#SBATCH --array=0-'+str(len(temps_30)-1)+'\n'
                    '#SBATCH --nodes=1\n'
                    '#SBATCH --chdir='+log_dir+'\n'
                    '#SBATCH --mem-per-cpu=4000\n'
                    '#SBATCH --time=0-1:00\n'
                    '\n'
                    'SAMPLE_LIST=($(<'+code_dir + '/' + lobe+'_30))\n'
                    'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'bash '+code_dir+'/concate_temp${SAMPLE}_'+lobe+'.sh\n'
                  )

f_queue_concate.close()

with open('concate_bashcode/'+lobe+'_30','w') as f_temp:
    f_temp.write('\n'.join(temps_30)+'\n')





'''------------------------------------------Temporal lobe------------------------------------------------'''
lobe = 'temporal'
merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'

# check 30 template threshold
if simi_method == 'corrdice':
    if lobe == 'frontal':
        cluster_thre = 0.38
    elif lobe == 'parietal':
        cluster_thre = 0.477
    elif lobe == 'temporal':
        cluster_thre = 0.365

### TODO:frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
# get threshold template
temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )

'''get hierarchical path'''
# node - higher level path
cluster_hie_dict = hierarch_path_dict(temps_30,merge_path)
# merge table
merge = pd.read_pickle(merge_path)
# cluster - subjects in
cluster_subject = leaf_in_cluster(merge_path)
merge_higher = merge[merge['distance']>cluster_thre]

# higher level registration in parallel

mov = []
tar = []
pre = []

for ind in subject_firsttemp_uq2.index:
    node_1 = subject_firsttemp_uq2.loc[ind]['frontal']
    node_2 = subject_firsttemp_uq2.loc[ind]['temporal']
    f_concate = open('concate_bashcode/concate_temp_'+ node_1 +'.'+ node_2 + '_' + lobe + '.sh', 'w')
    f_concate.write(
    'process_folder=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n'
    'ico_6=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii\n'
    'output_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n')
    hierarchical_path = cluster_hie_dict[node_2]
    for i, sub_temp in enumerate(hierarchical_path):
        if i == 1:
            f_concate.write(
                'wb_command -surface-sphere-project-unproject ${process_folder}/frontal_'+node_1+'.' + lobe + '.' + node_2 + '.MSM.' +
                hierarchical_path[i - 1] + '.sphere.reg.surf.gii ${ico_6} ${process_folder}/frontal_'+node_1+'.' + lobe + '.' +
                hierarchical_path[i - 1] + '.MSM.' + hierarchical_path[
                    i] + '.sphere.reg.surf.gii ${output_dir}/frontal_'+node_1+'.' + lobe + '.' + node_2 + '.to.' + hierarchical_path[
                    i] + '.sphere.concate.surf.gii\n')
        elif (i > 1) & (i < (len(hierarchical_path) - 1)):
            f_concate.write('wb_command -surface-sphere-project-unproject ${output_dir}/frontal_'+node_1+'.' + lobe + '.' + node_2 + '.to.' +
                            hierarchical_path[i - 1] + '.sphere.concate.surf.gii ${ico_6} ${process_folder}/frontal_'+node_1+'.' + lobe + '.' +
                            hierarchical_path[i - 1] + '.MSM.' + hierarchical_path[
                                i] + '.sphere.reg.surf.gii ${output_dir}/frontal_'+node_1+'.' + lobe + '.' + node_2 + '.to.' + hierarchical_path[
                                i] + '.sphere.concate.surf.gii\n')
        elif i == (len(hierarchical_path) - 1):
            f_concate.write('wb_command -surface-sphere-project-unproject ${output_dir}/frontal_'+node_1+'.' + lobe + '.' + node_2 + '.to.' +
                            hierarchical_path[i - 1] + '.sphere.concate.surf.gii ${ico_6} ${process_folder}/frontal_'+node_1+'.' + lobe + '.' +
                            hierarchical_path[i - 1] + '.MSM.' + hierarchical_path[
                                i] + '.sphere.reg.surf.gii ${output_dir}/frontal_'+node_1+'.'+lobe+'_'+node_2+'.sphere.concate.surf.gii\n')

    mov = mov+[node_2]+hierarchical_path[:-1].tolist()
    tar = tar+hierarchical_path.tolist()
    pre = pre+[node_1]*(len(hierarchical_path))

f_concate.close()
pre = np.asarray(pre).reshape(-1,1)
tar = np.asarray(tar).reshape(-1,1)
mov = np.asarray(mov).reshape(-1,1)
df_temporal_list = pd.DataFrame(np.concatenate([pre,mov,tar],axis=1),columns=['pre','mov','tar'])
df_temporal_list = df_temporal_list.drop_duplicates()

df_temporal_list['mov'].to_csv('concate_bashcode/'+lobe+'_temp_move_list', sep='\n', index=False, header=False)
df_temporal_list['tar'].to_csv('concate_bashcode/'+lobe+'_temp_tar_list', sep='\n', index=False, header=False)
df_temporal_list['pre'].to_csv('concate_bashcode/'+lobe+'_temp_pre_list', sep='\n', index=False, header=False)


# registration
f_queue_reg = open('concate_bashcode/queue_reg_temps_' + lobe + '.sh', 'w')
f_queue_reg.write('#!/bin/bash -l\n'
                    '#SBATCH --job-name=reg_temp\n'
                    '#SBATCH --output=output.array.%A.%a.out\n'
                    '#SBATCH --array=0-' + str(len(df_temporal_list) - 1) + '\n'
                    '#SBATCH --nodes=1\n'
                    '#SBATCH --chdir=' + log_dir + '\n'
                    '#SBATCH --mem-per-cpu=4000\n'
                    '#SBATCH --time=0-3:00\n'
                    'module load openblas\n'
                    'MOVE_LIST=($(<' + code_dir + '/' + lobe + '_temp_move_list))\n'
                    'MOV=${MOVE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'TAR_LIST=($(<' + code_dir + '/' + lobe + '_temp_tar_list))\n'
                    'TAR=${TAR_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'PRE1_LIST=($(<' + code_dir + '/' + lobe + '_temp_pre_list))\n'
                    'PRE1=${PRE1_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'output_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n'
                    'newmsm --inmesh=${output_dir}/frontal_${PRE1}.sphere.concate.surf.gii '
                    '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                    '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${MOV}.curv.affine.ico6.shape.gii '
                    '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR}.curv.affine.ico6.shape.gii '
                    '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_' + lobe + '_mask_dil.shape.gii '
                    '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_' + lobe + '_mask_dil.shape.gii '
                    '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/frontal_${PRE1}.' + lobe + '.${MOV}.MSM.${TAR}. '
                    '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_concate;'
                    )
f_queue_reg.close()





f_queue_concate = open('concate_bashcode/queue_concate_temps_'+lobe+'.sh','w')
f_queue_concate.write('#!/bin/bash -l\n'
                    '#SBATCH --job-name=conc_temp\n'
                    '#SBATCH --output=output.array.%A.%a.out\n'
                    '#SBATCH --array=0-'+str(len(subject_firsttemp_uq2)-1)+'\n'
                    '#SBATCH --nodes=1\n'
                    '#SBATCH --chdir='+log_dir+'\n'
                    '#SBATCH --mem-per-cpu=4000\n'
                    '#SBATCH --time=0-1:00\n'
                    '\n'
                    'F_LIST=($(<'+code_dir + '/lobe2_frontal))\n'
                    'FRONTAL=${F_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'T_LIST=($(<'+code_dir + '/lobe2_temporal))\n'
                    'TEMPORAL=${T_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'bash '+code_dir+'/concate_temp_${FRONTAL}.${TEMPORAL}_' + lobe + '.sh\n'
                  )

f_queue_concate.close()

with open('concate_bashcode/'+lobe+'_30','w') as f_temp:
    f_temp.write('\n'.join(temps_30)+'\n')







'''------------------------------------------Parietal lobe------------------------------------------------'''
lobe = 'parietal'
merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'

# check 30 template threshold
if simi_method == 'corrdice':
    if lobe == 'frontal':
        cluster_thre = 0.38
    elif lobe == 'parietal':
        cluster_thre = 0.477
    elif lobe == 'temporal':
        cluster_thre = 0.365

### TODO:frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
# get threshold template
temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )

'''get hierarchical path'''
# node - higher level path
cluster_hie_dict = hierarch_path_dict(temps_30,merge_path)
# merge table
merge = pd.read_pickle(merge_path)
# cluster - subjects in
cluster_subject = leaf_in_cluster(merge_path)
merge_higher = merge[merge['distance']>cluster_thre]

# higher level registration in parallel
mov = []
tar = []
pre = []
pre2 = []

for ind in subject_firsttemp_uq3.index:
    node_1 = subject_firsttemp_uq3.loc[ind]['frontal']
    node_2 = subject_firsttemp_uq3.loc[ind]['temporal']
    node_3 = subject_firsttemp_uq3.loc[ind]['parietal']
    f_concate = open('concate_bashcode/concate_temp_'+ node_1 +'.'+ node_2 +'.'+ node_3 + '_' + lobe + '.sh', 'w')
    f_concate.write(
    'process_folder=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n'
    'ico_6=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii\n'
    'output_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n')
    hierarchical_path = cluster_hie_dict[node_3]
    for i, sub_temp in enumerate(hierarchical_path):
        if i == 1:
            f_concate.write(
                'wb_command -surface-sphere-project-unproject ${process_folder}/frontal_'+node_1+'.temporal_'+node_2+'.' + lobe + '.' + node_3 + '.MSM.' +
                hierarchical_path[i - 1] + '.sphere.reg.surf.gii ${ico_6} ${process_folder}/frontal_'+node_1+'.temporal_'+node_2+'.' + lobe + '.' +
                hierarchical_path[i - 1] + '.MSM.' + hierarchical_path[
                    i] + '.sphere.reg.surf.gii ${output_dir}/frontal_'+node_1+'.temporal_'+node_2+'.' + lobe + '.' + node_3 + '.to.' + hierarchical_path[
                    i] + '.sphere.concate.surf.gii\n')
        elif (i > 1) & (i < (len(hierarchical_path) - 1)):
            f_concate.write('wb_command -surface-sphere-project-unproject ${output_dir}/frontal_'+node_1+'.temporal_'+node_2+'.' + lobe + '.' + node_3 + '.to.' +
                            hierarchical_path[i - 1] + '.sphere.concate.surf.gii ${ico_6} ${process_folder}/frontal_'+node_1+'.temporal_'+node_2+'.' + lobe + '.' +
                            hierarchical_path[i - 1] + '.MSM.' + hierarchical_path[
                                i] + '.sphere.reg.surf.gii ${output_dir}/frontal_'+node_1+'.temporal_'+node_2+'.' + lobe + '.' + node_3 + '.to.' + hierarchical_path[
                                i] + '.sphere.concate.surf.gii\n')
        elif i == (len(hierarchical_path) - 1):
            f_concate.write('wb_command -surface-sphere-project-unproject ${output_dir}/frontal_'+node_1+'.temporal_'+node_2+'.' + lobe + '.' + node_3 + '.to.' +
                            hierarchical_path[i - 1] + '.sphere.concate.surf.gii ${ico_6} ${process_folder}/frontal_'+node_1+'.temporal_'+node_2+'.' + lobe + '.' +
                            hierarchical_path[i - 1] + '.MSM.' + hierarchical_path[
                                i] + '.sphere.reg.surf.gii ${output_dir}/frontal_'+node_1+'.temporal_'+node_2+'.'+lobe+'_'+node_3+'.sphere.concate.surf.gii\n')

    mov = mov+[node_3]+hierarchical_path[:-1].tolist()
    tar = tar+hierarchical_path.tolist()
    pre = pre+[node_1]*(len(hierarchical_path))
    pre2 = pre2+[node_2]*(len(hierarchical_path))


f_concate.close()

pre = np.asarray(pre).reshape(-1,1)
pre2 = np.asarray(pre2).reshape(-1,1)
tar = np.asarray(tar).reshape(-1,1)
mov = np.asarray(mov).reshape(-1,1)
df_temporal_list = pd.DataFrame(np.concatenate([pre,pre2,mov,tar],axis=1),columns=['pre','pre2','mov','tar'])
df_temporal_list = df_temporal_list.drop_duplicates()
df_temporal_list['mov'].to_csv('concate_bashcode/'+lobe+'_temp_move_list', sep='\n', index=False, header=False)
df_temporal_list['tar'].to_csv('concate_bashcode/'+lobe+'_temp_tar_list', sep='\n', index=False, header=False)
df_temporal_list['pre'].to_csv('concate_bashcode/'+lobe+'_temp_pre_list', sep='\n', index=False, header=False)
df_temporal_list['pre2'].to_csv('concate_bashcode/'+lobe+'_temp_pre2_list', sep='\n', index=False, header=False)


# registration
f_queue_reg = open('concate_bashcode/queue_reg_temps_' + lobe + '.sh', 'w')
f_queue_reg.write('#!/bin/bash -l\n'
                    '#SBATCH --job-name=reg_temp\n'
                    '#SBATCH --output=output.array.%A.%a.out\n'
                    '#SBATCH --array=0-' + str(len(df_temporal_list)-1) + '\n'
                    '#SBATCH --nodes=1\n'
                    '#SBATCH --chdir=' + log_dir + '\n'
                    '#SBATCH --mem-per-cpu=4000\n'
                    '#SBATCH --time=0-3:00\n'
                    'module load openblas\n'
                    'MOVE_LIST=($(<' + code_dir + '/' + lobe + '_temp_move_list))\n'
                    'MOV=${MOVE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'TAR_LIST=($(<' + code_dir + '/' + lobe + '_temp_tar_list))\n'
                    'TAR=${TAR_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'PRE1_LIST=($(<' + code_dir + '/' + lobe + '_temp_pre_list))\n'
                    'PRE1=${PRE1_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'PRE2_LIST=($(<' + code_dir + '/' + lobe + '_temp_pre2_list))\n'
                    'PRE2=${PRE2_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'output_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n'
                    'newmsm --inmesh=${output_dir}/frontal_${PRE1}.temporal_${PRE2}.sphere.concate.surf.gii '
                    '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                    '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${MOV}.curv.affine.ico6.shape.gii '
                    '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR}.curv.affine.ico6.shape.gii '
                    '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_' + lobe + '_mask_dil.shape.gii '
                    '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/' + lobe + '_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_' + lobe + '_mask_dil.shape.gii '
                    '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/frontal_${PRE1}.temporal_${PRE2}.' + lobe + '.${MOV}.MSM.${TAR}. '
                    '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_concate;'
                    )
f_queue_reg.close()







f_queue_concate = open('concate_bashcode/queue_concate_temps_'+lobe+'.sh','w')
f_queue_concate.write('#!/bin/bash -l\n'
                    '#SBATCH --job-name=conc_temp\n'
                    '#SBATCH --output=output.array.%A.%a.out\n'
                    '#SBATCH --array=0-'+str(len(subject_firsttemp_uq3)-1)+'\n'
                    '#SBATCH --nodes=1\n'
                    '#SBATCH --chdir='+log_dir+'\n'
                    '#SBATCH --mem-per-cpu=4000\n'
                    '#SBATCH --time=0-1:00\n'
                    '\n'
                    'F_LIST=($(<'+code_dir + '/lobe2_frontal))\n'
                    'FRONTAL=${F_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'T_LIST=($(<'+code_dir + '/lobe2_temporal))\n'
                    'TEMPORAL=${T_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'P_LIST=($(<'+code_dir + '/lobe2_parietal))\n'
                    'PARIETAL=${P_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'bash '+code_dir+'/concate_temp_${FRONTAL}.${TEMPORAL}.${PARIETAL}_' + lobe + '.sh\n'
                  )

f_queue_concate.close()

with open('concate_bashcode/'+lobe+'_30','w') as f_temp:
    f_temp.write('\n'.join(temps_30)+'\n')





