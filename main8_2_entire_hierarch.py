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




'''registration code'''

# load subject's first template
subject_firsttemp = pd.read_csv('subject_first_templates/subject_firsttemp.csv')

with open('concate_bashcode/all_reg/queue_subject_to_top.sh', 'w') as f_queue:

    f_queue.write('#!/bin/bash -l\n'
        '#SBATCH --job-name=reg_all\n'
        '#SBATCH --output=output.array.%A.%a.out\n'
        '#SBATCH --array=0-'+str(len(subjects_all)-1)+'\n'
        '#SBATCH --nodes=1\n'
        '#SBATCH --chdir='+log_dir+'\n'
        '#SBATCH --mem-per-cpu=4000\n'
        '#SBATCH --time=0-3:00\n'
        '\n'
        'SAMPLE_LIST=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/all_reg/subjects))\n'
        'SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}\n'
        
        'TAR_LIST1=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/all_reg/tar_frontal))\n'
        'TAR_FRONTAL=${TAR_LIST1[${SLURM_ARRAY_TASK_ID}]}\n'
        
        'TAR_LIST2=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/all_reg/tar_parietal))\n'
        'TAR_PARIETAL=${TAR_LIST2[${SLURM_ARRAY_TASK_ID}]}\n'
        
        'TAR_LIST3=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/all_reg/tar_temporal))\n'
        'TAR_TEMPORAL=${TAR_LIST3[${SLURM_ARRAY_TASK_ID}]}\n'
        '\n'
        'process_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_process\n'
        'ico_6=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii\n'
        'result_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/concatenate_result\n'
        '\n'
        'wb_command -surface-sphere-project-unproject ${process_dir}/temporal3.${SAMPLE}.MSM.${TAR_TEMPORAL}.sphere.reg.surf.gii ${ico_6} ${process_dir}/frontal.${TAR_FRONTAL}.to.NODE2218.sphere.concate.surf.gii ${result_dir}/${SAMPLE}.frontal.MSMHT.reg.surf.gii\n'
        'wb_command -surface-sphere-project-unproject ${result_dir}/${SAMPLE}.frontal.MSMHT.reg.surf.gii ${ico_6} ${process_dir}/parietal.${TAR_PARIETAL}.to.NODE2218.sphere.concate.surf.gii ${result_dir}/${SAMPLE}.frontal.parietal.MSMHT.reg.surf.gii\n'
        'wb_command -surface-sphere-project-unproject ${result_dir}/${SAMPLE}.frontal.parietal.MSMHT.reg.surf.gii ${ico_6} ${process_dir}/temporal.${TAR_TEMPORAL}.to.NODE2218.sphere.concate.surf.gii ${result_dir}/${SAMPLE}.frontal.parietal.temporal.MSMHT.reg.surf.gii\n'
        'wb_command -metric-resample /scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${SAMPLE}.curv.affine.ico6.shape.gii ${result_dir}/${SAMPLE}.frontal.parietal.temporal.MSMHT.reg.surf.gii ${ico_6} ADAP_BARY_AREA ${result_dir}/${SAMPLE}.frontal.parietal.temporal.MSMHT.shape.gii -area-surfs ${result_dir}/${SAMPLE}.frontal.parietal.temporal.MSMHT.reg.surf.gii ${ico_6}\n'
                  )

with open('concate_bashcode/all_reg/subjects', 'w') as f:
    f.write('\n'.join(subject_firsttemp['subjects'].values)+'\n')

with open('concate_bashcode/all_reg/tar_frontal', 'w') as f:
    f.write('\n'.join(subject_firsttemp['frontal'].values)+'\n')

with open('concate_bashcode/all_reg/tar_parietal', 'w') as f:
    f.write('\n'.join(subject_firsttemp['parietal'].values)+'\n')

with open('concate_bashcode/all_reg/tar_temporal', 'w') as f:
    f.write('\n'.join(subject_firsttemp['temporal'].values)+'\n')









