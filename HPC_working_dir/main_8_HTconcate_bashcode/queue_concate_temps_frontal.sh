#!/bin/bash -l
#SBATCH --job-name=tempconcate
#SBATCH --output=output.array.%A.%a.out
#SBATCH --array=0-32
#SBATCH --nodes=1
#SBATCH --chdir=/your_HPC_working_dir/log
#SBATCH --mem-per-cpu=4000
#SBATCH --time=0-1:00

SAMPLE_LIST=($(</your_HPC_working_dir/bash_code/frontal_30))
SAMPLE=${SAMPLE_LIST[${SLURM_ARRAY_TASK_ID}]}
bash /your_HPC_working_dir/bash_code/concate_temp${SAMPLE}_frontal.sh
