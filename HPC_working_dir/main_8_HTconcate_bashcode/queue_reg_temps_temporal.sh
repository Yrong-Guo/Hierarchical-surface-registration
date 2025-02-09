#!/bin/bash -l
#SBATCH --job-name=reg_temp
#SBATCH --output=output.array.%A.%a.out
#SBATCH --array=0-67
#SBATCH --nodes=1
#SBATCH --chdir=/your_HPC_working_dir/log
#SBATCH --mem-per-cpu=4000
#SBATCH --time=0-3:00
module load openblas
MOVE_LIST=($(</your_HPC_working_dir/bash_code/temporal_temp_move_list))
MOV=${MOVE_LIST[${SLURM_ARRAY_TASK_ID}]}
TAR_LIST=($(</your_HPC_working_dir/bash_code/temporal_temp_tar_list))
TAR=${TAR_LIST[${SLURM_ARRAY_TASK_ID}]}
newmsm --inmesh=/your_HPC_working_dir/sunet.ico-6.surf.gii --refmesh=/your_HPC_working_dir/sunet.ico-6.surf.gii --indata=/your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${MOV}.curv.affine.ico6.shape.gii --refdata=/your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/${TAR}.curv.affine.ico6.shape.gii --inweight=/your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii --refweight=/your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/temp_lobe_mask/NODE2218_temporal_mask_smth.shape.gii -o /your_HPC_working_dir/concatenate_reg/temporal.${MOV}.MSM.${TAR}. --conf=/your_HPC_working_dir/config_MSM_concate;