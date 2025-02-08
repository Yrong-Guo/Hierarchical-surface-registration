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
wb_command -metric-math '(x0+x1+x2)/3' /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/NODE1910_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/212419.R.MSM.NODE1910_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/127933.R.MSM.NODE1910_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/135629.R.MSM.NODE1910_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-math 'abs(x-y)' /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/difference.shape.gii -var x /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/NODE1910_${iter_num_last}.curv.affine.ico6.shape.gii -var y /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/NODE1910_${iter_num}.curv.affine.ico6.shape.gii;
diff=$(wb_command -metric-stats /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/difference.shape.gii -reduce MEAN -roi /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE1910_frontal_mask.shape.gii);
echo $diff;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/NODE1910_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/NODE1910.final.curv.affine.ico6.shape.gii
