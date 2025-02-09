#!/bin/bash -l
#SBATCH --job-name=warpsulc
#SBATCH --output=output.array.%A.%a
#SBATCH --array=0-2219
#SBATCH --nodes=1
#SBATCH --chdir=/HPC_work_dir/log
#SBATCH --mem-per-cpu=3000
#SBATCH --time=0-2:00
#SBATCH --mail-user=yourong.guo@kcl.ac.uk

module load openblas
SAMPLE_LIST=($(</HPC_work_dir/code_pairwise_corrdice/sulcreg_move_list))
SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}
TAR_LIST=($(</HPC_work_dir/code_pairwise_corrdice/sulcreg_tar_list))
TAR=${TAR_LIST[${SLURM_ARRAY_TASK_ID}]}
bash /HPC_work_dir/code_pairwise_corrdice/apply_warp_to_sulc.sh -m ${SAMPLE} -t ${TAR}
