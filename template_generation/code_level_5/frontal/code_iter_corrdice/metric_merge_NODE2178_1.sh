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
wb_command -metric-math '(x0+x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11)/12' /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/NODE2178_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/100206.R.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/856968.R.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/146432.R.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x3 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/818859.R.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x4 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/204622.L.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x5 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/173132.R.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x6 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/856968.L.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x7 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/424939.R.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x8 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/123723.L.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x9 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/965771.R.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x10 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/121820.L.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii -var x11 /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/540436.L.MSM.NODE2178_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-math 'abs(x-y)' /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/difference.shape.gii -var x /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/NODE2178_${iter_num_last}.curv.affine.ico6.shape.gii -var y /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/NODE2178_${iter_num}.curv.affine.ico6.shape.gii;
diff=$(wb_command -metric-stats /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/difference.shape.gii -reduce MEAN -roi /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2178_frontal_mask.shape.gii);
echo $diff;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/NODE2178_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE2178_msmrefine/NODE2178.final.curv.affine.ico6.shape.gii
