'''
concatenate between-templates registration together

This is the latest version 2024.3.3_yourong
'''

import numpy as np
from utils.hierarch_tools import leaf_in_cluster, hierarch_path_dict
from utils.concatenate_function import concatenate_warps
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
import pandas as pd

'''settings'''
lobe = 'frontal'
simi_method = 'corrdice'
merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'


# on CREATE
work_dir = '/scratch/prj/cortical_imaging/Yourong/hierarch/combine/HTconcate'
log_dir = work_dir+'/log'
code_dir = work_dir+'/bash_code'
template_dir = '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask'


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
cluster_hie_dict_lobe = hierarch_path_dict(temps_30,merge_path)
# merge table
merge = pd.read_pickle(merge_path)
# cluster - subjects in
cluster_subject = leaf_in_cluster(merge_path)
# higher path than threshold
merge_higher = merge[merge['distance']>cluster_thre]



''' write the moving and target from temp to temp'''
# in parallel
f_mov = open('concate_bashcode/'+lobe+'_temp_move_list','w')
f_tar = open('concate_bashcode/'+lobe+'_temp_tar_list','w')

for ind in merge_higher.index:

    ''' write the moving and target from temp to temp'''
    f_mov.write(merge_higher.loc[ind]['subID1']+'\n')
    f_mov.write(merge_higher.loc[ind]['subID2']+'\n')
    f_tar.write(merge_higher.loc[ind]['mergeID']+'\n')
    f_tar.write(merge_higher.loc[ind]['mergeID']+'\n')

f_mov.close()
f_tar.close()

f_queue_reg = open('concate_bashcode/queue_reg_temps_'+lobe+'.sh','w')
f_queue_reg.write('#!/bin/bash -l\n'
                    '#SBATCH --job-name=reg_temp\n'
                    '#SBATCH --output=output.array.%A.%a.out\n'
                    '#SBATCH --array=0-'+str(len(merge_higher)*2-1)+'\n'
                    '#SBATCH --nodes=1\n'
                    '#SBATCH --chdir='+log_dir+'\n'
                    '#SBATCH --mem-per-cpu=4000\n'
                    '#SBATCH --time=0-3:00\n'
                    'module load openblas\n'
                    'MOVE_LIST=($(<'+code_dir+ '/' + lobe+'_temp_move_list))\n'
                    'MOV=${MOVE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    'TAR_LIST=($(<'+code_dir + '/' + lobe+'_temp_tar_list))\n'
                    'TAR=${TAR_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
                    ''
                    'newmsm --inmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                    '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                    '--indata='+template_dir+'/final_temps/${MOV}.curv.affine.ico6.shape.gii '
                    '--refdata='+template_dir+'/final_temps/${TAR}.curv.affine.ico6.shape.gii '
                    '--inweight='+template_dir+'/temp_lobe_mask/NODE2218_'+lobe+'_mask_smth.shape.gii '
                    '--refweight='+template_dir+'/temp_lobe_mask/NODE2218_'+lobe+'_mask_smth.shape.gii '
                    '-o '+work_dir+'/concatenate_reg/'+lobe+'.${MOV}.MSM.${TAR}. '
                    '--conf='+work_dir+'/config_MSM_concate;'
                  )
f_queue_reg.close()



'''concatenate code - -dont need to modify sphere not much distortion'''
# create name list
with open('concate_bashcode/'+lobe+'_30','w') as f_temp:
    f_temp.write('\n'.join(temps_30)+'\n')

# concatenate bash
for node in temps_30:

    hierarchical_path = cluster_hie_dict_lobe[node]

    f_concate = open('concate_bashcode/concate_temp'+node+'_'+lobe+'.sh','w')
    f_concate.write('reg_folder='+work_dir+'/concatenate_reg\n'
                    'ico_6=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii\n'
                    'output_dir='+work_dir+'/concatenate_process\n'
                    'output_dir_metrics='+work_dir+'/concatenate_process_metrics\n')

    for i, sub_temp in enumerate(hierarchical_path):
        if i == 1 :
            f_concate.write('wb_command -surface-sphere-project-unproject ${reg_folder}/'+lobe+'.'+node+'.MSM.'+hierarchical_path[i-1]+'.sphere.reg.surf.gii ${ico_6} ${reg_folder}/'+lobe+'.'+hierarchical_path[i-1]+'.MSM.'+hierarchical_path[i]+'.sphere.reg.surf.gii ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii\n'
                            'wb_command -metric-resample '+template_dir+'/final_temps/'+node+'.curv.affine.ico6.shape.gii ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.MSMHT.func.gii -area-surfs ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii ${ico_6}\n')
        elif i > 1:
            f_concate.write('wb_command -surface-sphere-project-unproject ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i-1]+'.sphere.concate.surf.gii ${ico_6} ${reg_folder}/'+lobe+'.'+hierarchical_path[i-1]+'.MSM.'+hierarchical_path[i]+'.sphere.reg.surf.gii ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii\n'
                            'wb_command -metric-resample '+template_dir+'/final_temps/'+node+'.curv.affine.ico6.shape.gii ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.MSMHT.func.gii -area-surfs ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii ${ico_6}\n')

f_concate.close()

# queue of the bash files
f_queue_concate = open('concate_bashcode/queue_concate_temps_'+lobe+'.sh','w')
f_queue_concate.write('#!/bin/bash -l\n'
                    '#SBATCH --job-name=tempconcate\n'
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









