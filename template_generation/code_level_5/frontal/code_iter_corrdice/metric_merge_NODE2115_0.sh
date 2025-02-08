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
wb_command -metric-math '(x0+x1+x2)/3' /HPC_work_dir/corrdice_affine_mask/checkNODE2115_msmrefine/NODE2115_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE2115_msmrefine/116221.L.MSM.NODE2115_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE2115_msmrefine/165032.L.MSM.NODE2115_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE2115_msmrefine/248339.L.MSM.NODE2115_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-merge /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2115_frontal_merged.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/116221.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/165032.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/248339.L.frontal.ico6.shape.gii;
wb_command -metric-reduce /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2115_frontal_merged.shape.gii MAX /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2115_frontal_mask.shape.gii;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE2115_msmrefine/NODE2115_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE2115_msmrefine/NODE2115.final.curv.affine.ico6.shape.gii
