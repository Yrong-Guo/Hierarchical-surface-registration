#!/bin/bash -l
#SBATCH --job-name=merge_NODE2181
#SBATCH --output=output.array.%A.%a
#SBATCH --array=0-0
#SBATCH --nodes=1
#SBATCH --chdir=/HPC_work_dir/log
#SBATCH --mem-per-cpu=4000
#SBATCH --time=0-3:00
module load openblas
bash /HPC_work_dir/code_iter_corrdice/metric_merge_NODE2181_1.sh -n 7
