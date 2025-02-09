#!/bin/bash
while getopts 'n:m:t:' flag; do
  case "${flag}" in
    n) iter_num="${OPTARG}" ;;
    m) mov_id="${OPTARG}" ;;
    t) tar_id="${OPTARG}" ;;
    *)
      echo "Usage: $0 [-n iter_num] [-m mov_id] [-t tar_id]"
      exit 1
      ;;
  esac
done
iter_num_last=$((${iter_num} - 1))
create_work_dir=/HPC_work_dir
newmsm --inmesh=/HPC_work_dir/sunet.ico-6.surf.gii --refmesh=/HPC_work_dir/sunet.ico-6.surf.gii --indata=/HPC_work_dir/affined_features/${mov_id}.curv.affine.ico6.shape.gii --refdata=${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${tar_id}_${iter_num_last}.curv.affine.ico6.shape.gii -o ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}_${iter_num}. --conf=${create_work_dir}/msm_config/config_standard_MSM_strain_005 &
wait;
rm ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}_${iter_num}.sphere.LR.reg.surf.gii;
rm -r ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}_${iter_num}.logdir;
