#!/bin/bash -l
#SBATCH --job-name=regrounds
#SBATCH --output=output.array.%A.%a.out
#SBATCH --array=0-2219
#SBATCH --nodes=1
#SBATCH --chdir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/HTconcate/log
#SBATCH --mem-per-cpu=4000
#SBATCH --time=0-3:00

SAMPLE_LIST=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/subject_reg/subjects))
SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}
TAR_LIST1=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/subject_reg/tar_frontal))
TAR_FRONTAL=${TAR_LIST1[${SLURM_ARRAY_TASK_ID}]}
TAR_LIST2=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/subject_reg/tar_parietal))
TAR_PARIETAL=${TAR_LIST2[${SLURM_ARRAY_TASK_ID}]}
TAR_LIST3=($(</scratch/prj/cortical_imaging/Yourong/hierarch/combine/newtemp/bash_code/subject_reg/tar_temporal))
TAR_TEMPORAL=${TAR_LIST3[${SLURM_ARRAY_TASK_ID}]}

frontal_msk_smth=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_frontal_mask_smth.shape.gii
parietal_msk_smth=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_parietal_mask_smth.shape.gii
temporal_msk_smth=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii
ico_6=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii
config_path=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/HTconcate/bash_code/subject_reg
affined_curv_dir=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features
template_dir=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/HTconcate/concatenate_process_metrics
output_combineprocess=/scratch/prj/cortical_imaging/Yourong/hierarch/combine/HTconcate/combine_process


# Level 1
newmsm \
--inmesh=${ico_6} \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/frontal.${TAR_FRONTAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${frontal_msk_smth} \
--refweight=${frontal_msk_smth} \
-o ${output_combineprocess}/frontal1.${SAMPLE}.MSM.${TAR_FRONTAL}. \
--conf=${config_path}/config_MSM_firsttemp_1;

newmsm \
--inmesh=${output_combineprocess}/frontal1.${SAMPLE}.MSM.${TAR_FRONTAL}.sphere.reg.surf.gii \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/parietal.${TAR_PARIETAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${parietal_msk_smth} \
--refweight=${parietal_msk_smth} \
-o ${output_combineprocess}/parietal1.${SAMPLE}.MSM.${TAR_PARIETAL}. \
--conf=${config_path}/config_MSM_firsttemp_1;

newmsm \
--inmesh=${output_combineprocess}/parietal1.${SAMPLE}.MSM.${TAR_PARIETAL}.sphere.reg.surf.gii \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/temporal.${TAR_TEMPORAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${temporal_msk_smth} \
--refweight=${temporal_msk_smth} \
-o ${output_combineprocess}/temporal1.${SAMPLE}.MSM.${TAR_TEMPORAL}. \
--conf=${config_path}/config_MSM_firsttemp_1;



# Level 2
newmsm \
--inmesh=${output_combineprocess}/temporal1.${SAMPLE}.MSM.${TAR_TEMPORAL}.sphere.reg.surf.gii \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/frontal.${TAR_FRONTAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${frontal_msk_smth} \
--refweight=${frontal_msk_smth} \
-o ${output_combineprocess}/frontal2.${SAMPLE}.MSM.${TAR_FRONTAL}. \
--conf=${config_path}/config_MSM_firsttemp_2;

newmsm \
--inmesh=${output_combineprocess}/frontal2.${SAMPLE}.MSM.${TAR_FRONTAL}.sphere.reg.surf.gii \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/parietal.${TAR_PARIETAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${parietal_msk_smth} \
--refweight=${parietal_msk_smth} \
-o ${output_combineprocess}/parietal2.${SAMPLE}.MSM.${TAR_PARIETAL}. \
--conf=${config_path}/config_MSM_firsttemp_2;

newmsm \
--inmesh=${output_combineprocess}/parietal2.${SAMPLE}.MSM.${TAR_PARIETAL}.sphere.reg.surf.gii \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/temporal.${TAR_TEMPORAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${temporal_msk_smth} \
--refweight=${temporal_msk_smth} \
-o ${output_combineprocess}/temporal2.${SAMPLE}.MSM.${TAR_TEMPORAL}. \
--conf=${config_path}/config_MSM_firsttemp_2;



# Level 3
newmsm \
--inmesh=${output_combineprocess}/temporal2.${SAMPLE}.MSM.${TAR_TEMPORAL}.sphere.reg.surf.gii \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/frontal.${TAR_FRONTAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${frontal_msk_smth} \
--refweight=${frontal_msk_smth} \
-o ${output_combineprocess}/frontal3.${SAMPLE}.MSM.${TAR_FRONTAL}. \
--conf=${config_path}/config_MSM_firsttemp_3;

newmsm \
--inmesh=${output_combineprocess}/frontal3.${SAMPLE}.MSM.${TAR_FRONTAL}.sphere.reg.surf.gii \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/parietal.${TAR_PARIETAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${parietal_msk_smth} \
--refweight=${parietal_msk_smth} \
-o ${output_combineprocess}/parietal3.${SAMPLE}.MSM.${TAR_PARIETAL}. \
--conf=${config_path}/config_MSM_firsttemp_3;

newmsm \
--inmesh=${output_combineprocess}/parietal3.${SAMPLE}.MSM.${TAR_PARIETAL}.sphere.reg.surf.gii \
--refmesh=${ico_6} \
--indata=${affined_curv_dir}/${SAMPLE}.curv.affine.ico6.shape.gii \
--refdata=${template_dir}/temporal.${TAR_TEMPORAL}.to.NODE2218.MSMHT.func.gii \
--inweight=${temporal_msk_smth} \
--refweight=${temporal_msk_smth} \
-o ${output_combineprocess}/temporal3.${SAMPLE}.MSM.${TAR_TEMPORAL}. \
--conf=${config_path}/config_MSM_firsttemp_3;
