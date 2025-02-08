#!/bin/bash -l
#SBATCH --job-name=reg_NODE1951
#SBATCH --output=output.array.%A.%a
#SBATCH --array=0-5
#SBATCH --nodes=1
#SBATCH --chdir=/HPC_work_dir/log
#SBATCH --mem-per-cpu=4000
#SBATCH --time=0-24:00
module load openblas
SAMPLE_LIST=($(</HPC_work_dir/code_iter_corrdice/cluster_reg_NODE1951.txt))
SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}
bash /HPC_work_dir/code_iter_corrdice/msm_inter_refine_1.sh -n 7 -m ${SAMPLE} -t NODE1951
