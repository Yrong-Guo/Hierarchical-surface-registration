'''register individual subject to 3 first template take turns in 3 level'''

from utils.hierarch_tools import leaf_in_cluster, hierarch_path_dict
from get_clusters_with_thre import leaf_in_cluster,get_clusters_with_thre
import pandas as pd
import numpy as np


'''settings'''
simi_method = 'corrdice'
log_dir = '/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/log'
code_dir = '/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code'

subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'
subjects_all = open(subject_list).read().splitlines()





# subject_templates = np.zeros((len(subjects_all),4)).astype('object')
# for i, lobe in enumerate(['frontal','parietal','temporal']):
#
#     merge_path = 'dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
#
#     # check 30 template threshold
#     if simi_method == 'corrdice':
#         if lobe == 'frontal':
#             cluster_thre = 0.38
#         elif lobe == 'parietal':
#             cluster_thre = 0.477
#         elif lobe == 'temporal':
#             cluster_thre = 0.365
#
#     ### TODO:frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
#     # get threshold template
#     temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=False )
#
#     '''get hierarchical path'''
#     # merge table
#     merge = pd.read_pickle(merge_path)
#     # cluster - subjects in
#     cluster_subject = leaf_in_cluster(merge_path)
#     # merge_higher = merge[merge['distance']>cluster_thre]
#
#     subjects_lobe = []
#     first_temps = []
#     for temp in temps_30:
#         subjects = cluster_subject[temp]
#         for sub in subjects:
#             subjects_lobe.append(sub)
#             first_temps.append(temp)
#
#     subjects_lobe = np.asarray(subjects_lobe)
#     first_temps = np.asarray(first_temps)
#
#     index = np.argsort(subjects_lobe)
#
#     subject_templates[:,i+1] = first_temps[index]
#
#     subject_templates[:,0] = subjects_lobe[index]




'''save subjects and their first template as dataframe'''

# subject_firsttemp = pd.DataFrame(subject_templates,columns=['subjects','frontal','parietal','temporal'])
# subject_firsttemp.to_csv('subject_first_templates/subject_firsttemp.csv',index_label=False)



'''registration code'''

subject_firsttemp = pd.read_csv('subject_first_templates/subject_firsttemp.csv')

with open('concate_bashcode/subject_reg/queue_subject_reg.sh', 'w') as f_queue:

    f_queue.write('#!/bin/bash -l\n'
        '#SBATCH --job-name=reground\n'
        '#SBATCH --output=output.array.%A.%a.out\n'
        '#SBATCH --array=0-'+str(len(subjects_all)-1)+'\n'
        '#SBATCH --nodes=1\n'
        '#SBATCH --chdir='+log_dir+'\n'
        '#SBATCH --mem-per-cpu=4000\n'
        '#SBATCH --time=0-3:00\n'
        '\n'
        'SAMPLE_LIST=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/subject_reg/subjects))\n'
        'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
        
        'TAR_LIST1=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/subject_reg/tar_frontal))\n'
        'TAR_FRONTAL=${TAR_LIST1[${SLURM_ARRAY_TASK_ID}]}\n'
        
        'TAR_LIST2=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/subject_reg/tar_parietal))\n'
        'TAR_PARIETAL=${TAR_LIST2[${SLURM_ARRAY_TASK_ID}]}\n'
        
        'TAR_LIST3=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/subject_reg/tar_temporal))\n'
        'TAR_TEMPORAL=${TAR_LIST3[${SLURM_ARRAY_TASK_ID}]}\n'
        '\n'
        'newmsm --inmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_FRONTAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_frontal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_frontal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/frontal1.${SAMPLE}.MSM.${TAR_FRONTAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_1;\n'
                                   
        'newmsm --inmesh=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/frontal1.${SAMPLE}.MSM.${TAR_FRONTAL}.sphere.reg.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_PARIETAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_parietal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_parietal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/parietal1.${SAMPLE}.MSM.${TAR_PARIETAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_1;\n'

        'newmsm --inmesh=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/parietal1.${SAMPLE}.MSM.${TAR_PARIETAL}.sphere.reg.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_TEMPORAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/temporal1.${SAMPLE}.MSM.${TAR_TEMPORAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_1;\n'

        'newmsm --inmesh=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/temporal1.${SAMPLE}.MSM.${TAR_TEMPORAL}.sphere.reg.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_FRONTAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_frontal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_frontal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/frontal2.${SAMPLE}.MSM.${TAR_FRONTAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_2;\n'
        
        'newmsm --inmesh=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/frontal2.${SAMPLE}.MSM.${TAR_FRONTAL}.sphere.reg.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_PARIETAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_parietal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_parietal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/parietal2.${SAMPLE}.MSM.${TAR_PARIETAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_2;\n'
        
        'newmsm --inmesh=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/parietal2.${SAMPLE}.MSM.${TAR_PARIETAL}.sphere.reg.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_TEMPORAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/temporal2.${SAMPLE}.MSM.${TAR_TEMPORAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_2;\n'

        'newmsm --inmesh=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/temporal2.${SAMPLE}.MSM.${TAR_TEMPORAL}.sphere.reg.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_FRONTAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_frontal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_frontal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/frontal3.${SAMPLE}.MSM.${TAR_FRONTAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_3;\n'
        
        'newmsm --inmesh=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/frontal3.${SAMPLE}.MSM.${TAR_FRONTAL}.sphere.reg.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_PARIETAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_parietal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_parietal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/parietal3.${SAMPLE}.MSM.${TAR_PARIETAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_3;\n'
        
        'newmsm --inmesh=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/parietal3.${SAMPLE}.MSM.${TAR_PARIETAL}.sphere.reg.surf.gii '
        '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
        '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii '
        '--refdata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR_TEMPORAL}.curv.affine.ico6.shape.gii '
        '--inweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii '
        '--refweight=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii '
        '-o /scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process/temporal3.${SAMPLE}.MSM.${TAR_TEMPORAL}. '
        '--conf=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/config_MSM_firsttemp_3;\n'

                  )

with open('concate_bashcode/subject_reg/subjects', 'w') as f:
    f.write('\n'.join(subject_firsttemp['subjects'].values)+'\n')

with open('concate_bashcode/subject_reg/tar_frontal', 'w') as f:
    f.write('\n'.join(subject_firsttemp['frontal'].values)+'\n')

with open('concate_bashcode/subject_reg/tar_parietal', 'w') as f:
    f.write('\n'.join(subject_firsttemp['parietal'].values)+'\n')

with open('concate_bashcode/subject_reg/tar_temporal', 'w') as f:
    f.write('\n'.join(subject_firsttemp['temporal'].values)+'\n')









