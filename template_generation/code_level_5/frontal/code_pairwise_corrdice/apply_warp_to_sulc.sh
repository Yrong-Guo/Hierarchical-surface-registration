#!/bin/bash
while getopts 'm:t:' flag; do
  case "${flag}" in
    m) mov_id="${OPTARG}" ;;
    t) tar_id="${OPTARG}" ;;
    *)
      echo "Usage: $0 [-m mov_id] [-t tar_id]"
      exit 1
      ;;
  esac
done
create_work_dir=/HPC_work_dir
WARP=$(ls ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}*.sphere.reg.surf.gii -tr | tail -n 1);
wb_command -metric-resample /HPC_work_dir/affined_sulc/${mov_id}.sulc.affine.ico6.shape.gii ${WARP} /HPC_work_dir/sunet.ico-6.surf.gii ADAP_BARY_AREA ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}.final.sulc.shape.gii -area-surfs ${WARP} /HPC_work_dir/sunet.ico-6.surf.gii;
