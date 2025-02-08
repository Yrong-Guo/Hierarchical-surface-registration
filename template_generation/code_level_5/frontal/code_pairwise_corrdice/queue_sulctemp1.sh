#!/bin/bash -l
#SBATCH --job-name=sulctemp
#SBATCH --output=output.array.%A.%a
#SBATCH --array=0-32
#SBATCH --chdir=/HPC_work_dir/log
#SBATCH --mem-per-cpu=8000
#SBATCH --time=0-1:00
module load openblas
SAMPLE_LIST=($(</HPC_work_dir/code_pairwise_corrdice/templates_frontal_30))
SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}
bash /HPC_work_dir/code_pairwise_corrdice/code_sulctemp1_${SAMPLE}.sh
