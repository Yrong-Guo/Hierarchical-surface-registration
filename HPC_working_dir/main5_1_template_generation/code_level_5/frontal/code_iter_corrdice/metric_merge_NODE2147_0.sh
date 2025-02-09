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
wb_command -metric-math '(x0+x1+x2+x3)/4' /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/NODE2147_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/510225.R.MSM.NODE2147_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/510225.L.MSM.NODE2147_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/406432.L.MSM.NODE2147_${iter_num}.transformed_and_reprojected.func.gii -var x3 /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/406432.R.MSM.NODE2147_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-merge /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2147_frontal_merged.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/510225.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/510225.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/406432.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/406432.R.frontal.ico6.shape.gii;
wb_command -metric-reduce /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2147_frontal_merged.shape.gii MAX /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2147_frontal_mask.shape.gii;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/NODE2147_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/NODE2147.final.curv.affine.ico6.shape.gii
