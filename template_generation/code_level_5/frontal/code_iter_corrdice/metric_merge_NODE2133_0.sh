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
wb_command -metric-math '(x0+x1+x2+x3+x4+x5+x6)/7' /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/NODE2133_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/128026.L.MSM.NODE2133_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/139637.L.MSM.NODE2133_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/677968.L.MSM.NODE2133_${iter_num}.transformed_and_reprojected.func.gii -var x3 /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/117122.L.MSM.NODE2133_${iter_num}.transformed_and_reprojected.func.gii -var x4 /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/117122.R.MSM.NODE2133_${iter_num}.transformed_and_reprojected.func.gii -var x5 /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/561444.L.MSM.NODE2133_${iter_num}.transformed_and_reprojected.func.gii -var x6 /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/660951.L.MSM.NODE2133_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-merge /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2133_frontal_merged.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/128026.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/139637.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/677968.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/117122.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/117122.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/561444.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/660951.L.frontal.ico6.shape.gii;
wb_command -metric-reduce /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2133_frontal_merged.shape.gii MAX /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2133_frontal_mask.shape.gii;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/NODE2133_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE2133_msmrefine/NODE2133.final.curv.affine.ico6.shape.gii
