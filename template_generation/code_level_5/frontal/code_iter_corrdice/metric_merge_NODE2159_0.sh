while getopts 'n:' flag; do
  case "${flag}" in
    n) iter_num="${OPTARG}" ;;
    *)
      echo "Usage: $0 [-n iter_num]"
      exit 1
      ;;
  esac
done
iter_num_last=$((${iter_num} - 1))
wb_command -metric-math '(x0+x1+x2+x3+x4+x5+x6+x7)/8' /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/NODE2159_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/200614.R.MSM.NODE2159_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/146937.R.MSM.NODE2159_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/513130.L.MSM.NODE2159_${iter_num}.transformed_and_reprojected.func.gii -var x3 /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/972566.L.MSM.NODE2159_${iter_num}.transformed_and_reprojected.func.gii -var x4 /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/111413.L.MSM.NODE2159_${iter_num}.transformed_and_reprojected.func.gii -var x5 /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/111413.R.MSM.NODE2159_${iter_num}.transformed_and_reprojected.func.gii -var x6 /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/128632.R.MSM.NODE2159_${iter_num}.transformed_and_reprojected.func.gii -var x7 /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/210617.R.MSM.NODE2159_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-merge /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2159_frontal_merged.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/200614.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/146937.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/513130.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/972566.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/111413.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/111413.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/128632.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/210617.R.frontal.ico6.shape.gii;
wb_command -metric-reduce /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2159_frontal_merged.shape.gii MAX /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2159_frontal_mask.shape.gii;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/NODE2159_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE2159_msmrefine/NODE2159.final.curv.affine.ico6.shape.gii
