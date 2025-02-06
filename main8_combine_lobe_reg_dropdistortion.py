'''
concatenate between-templates registration together
'''

import numpy as np
from utils.hierarch_tools import leaf_in_cluster, hierarch_path_dict
from utils.concatenate_function import concatenate_warps
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
import pandas as pd

'''settings'''
lobe = 'temporal'
simi_method = 'corrdice'

log_dir = '/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/log'
code_dir='/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code'

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
cluster_hie_dict_frontal = hierarch_path_dict(temps_30,merge_path)
# merge table
merge = pd.read_pickle(merge_path)
# cluster - subjects in
cluster_subject = leaf_in_cluster(merge_path)
merge_higher = merge[merge['distance']>cluster_thre]






'''get the dedrift warps'''

f_queue_dedrift = open('concate_bashcode/dedriftwarp_'+lobe+'.sh','w')
for temp in temps_30:
    command = 'wb_command -surface-average'
    sub_in_temp = cluster_subject[temp]


    output = '/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/dedriftwarp/' + lobe + '.' + temp + '.avg.surf.gii'

    rep_flag = ''
    for lf in sub_in_temp:
        rep_flag = rep_flag + ' ' + '-surf /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/' + lobe + '3.' + lf + '.MSM.' + temp + '.sphere.reg.surf.gii'

    command_text = command + ' ' + output + rep_flag+';\n'
    f_queue_dedrift.write(command_text)

f_queue_dedrift.close()



''' template registration code - fix the registration from the first template to the common space'''
# higher level registration in parallel
f_mov = open('concate_bashcode/'+lobe+'_temp_move_list','w')
f_tar = open('concate_bashcode/'+lobe+'_temp_tar_list','w')

for ind in merge_higher.index:
    # TODO later: from subject to temps
    # subjects = cluster_subject[node]
    # if '211720.L' in subjects:
    #     print(node)
    #     print(cluster_hie_dict_frontal[node])

    # '''from temp to temp''' TODO: concatenate in a reversed order of hierarchy
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
                    'ico_6=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii\n'
                    'if grep -Fxq "${MOV}" /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/'+lobe+'_30; then\n'
                    '   wb_command -surface-modify-sphere /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/dedriftwarp/'+lobe+'.${MOV}.avg.surf.gii 100 /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/dedriftwarp/'+lobe+'.${MOV}.avg.surf.gii -recenter;\n'
                    '   wb_command -surface-sphere-project-unproject ${ico_6} /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/dedriftwarp/'+lobe+'.${MOV}.avg.surf.gii ${ico_6} /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/dedriftwarp/'+lobe+'.${MOV}.avg.inv.surf.gii\n'
                    '   newmsm --inmesh=${ico_6} '
                    '--refmesh=${ico_6} '
                    '--trans=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/dedriftwarp/'+lobe+'.${MOV}.avg.inv.surf.gii '
                    '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${MOV}.curv.affine.ico6.shape.gii '
                    '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR}.curv.affine.ico6.shape.gii '
                    '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_'+lobe+'_mask_smth.shape.gii '
                    '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_'+lobe+'_mask_smth.shape.gii '
                    '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/'+lobe+'.${MOV}.MSM.${TAR}. '
                    '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_concate;\n'
                    'else\n'
                    '   newmsm --inmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                    '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                    '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${MOV}.curv.affine.ico6.shape.gii '
                    '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR}.curv.affine.ico6.shape.gii '
                    '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_'+lobe+'_mask_smth.shape.gii '
                    '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_'+lobe+'_mask_smth.shape.gii '
                    '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/'+lobe+'.${MOV}.MSM.${TAR}. '
                    '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_concate;\n'
                    'fi\n'
                  )
f_queue_reg.close()




'''*connection code? - once a lobe is registered, it might impact another lobe, change the other lobe back might also impact the first lobe'''


'''concatenate code - -dont need to modify sphere not much distortion'''
for node in temps_30:

    hierarchical_path = cluster_hie_dict_frontal[node]

    f_concate = open('concate_bashcode/concate_temp'+node+'_'+lobe+'.sh','w')
    f_concate.write('process_folder=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n'
                    'ico_6=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii\n'
                    'output_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n')

    for i, sub_temp in enumerate(hierarchical_path):
        if i == 1 :
            f_concate.write('wb_command -surface-sphere-project-unproject ${process_folder}/'+lobe+'.'+node+'.MSM.'+hierarchical_path[i-1]+'.sphere.reg.surf.gii ${ico_6} ${process_folder}/'+lobe+'.'+hierarchical_path[i-1]+'.MSM.'+hierarchical_path[i]+'.sphere.reg.surf.gii ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii\n')
        elif i > 1:
            f_concate.write('wb_command -surface-sphere-project-unproject ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i-1]+'.sphere.concate.surf.gii ${ico_6} ${process_folder}/'+lobe+'.'+hierarchical_path[i-1]+'.MSM.'+hierarchical_path[i]+'.sphere.reg.surf.gii ${output_dir}/'+lobe+'.'+node+'.to.'+hierarchical_path[i]+'.sphere.concate.surf.gii\n')

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











