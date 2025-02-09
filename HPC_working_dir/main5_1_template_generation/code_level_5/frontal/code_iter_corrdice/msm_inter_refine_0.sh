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
newmsm --inmesh=/HPC_work_dir/sunet.ico-6.surf.gii --refmesh=/HPC_work_dir/sunet.ico-6.surf.gii --indata=/HPC_work_dir/affined_sulc/${mov_id}.sulc.affine.ico6.shape.gii --refdata=${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${tar_id}.sulctemp0.affine.ico6.shape.gii -o ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}. --conf=${create_work_dir}/msm_config/config_standard_MSM_strain_005 &
wait;
rm ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.LR.reg.surf.gii;
rm -r ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.logdir;
if [ ! -d "/HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice" ];then
    mkdir /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice;
fi 
wb_command -metric-resample /HPC_work_dir/affined_features/${mov_id}.curv.affine.ico6.shape.gii ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.reg.surf.gii /HPC_work_dir/sunet.ico-6.surf.gii ADAP_BARY_AREA ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}_0.transformed_and_reprojected.func.gii -area-surfs ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.reg.surf.gii /HPC_work_dir/sunet.ico-6.surf.gii;
wb_command -metric-resample /HPC_work_dir/frontal_lobe/rotated_frontal_lobe/${mov_id}.frontal.ico6.shape.gii ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.reg.surf.gii /HPC_work_dir/sunet.ico-6.surf.gii ADAP_BARY_AREA /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/${mov_id}.frontal.ico6.shape.gii -area-surfs ${create_work_dir}/corrdice_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.reg.surf.gii /HPC_work_dir/sunet.ico-6.surf.gii;
wb_command -metric-math 'round(x)' /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/${mov_id}.frontal.ico6.shape.gii -var x /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/${mov_id}.frontal.ico6.shape.gii;