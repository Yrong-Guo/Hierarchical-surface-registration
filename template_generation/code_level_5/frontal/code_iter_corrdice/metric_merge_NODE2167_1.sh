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
wb_command -metric-math '(x0+x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24+x25)/26' /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/NODE2167_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/164131.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/386250.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/884064.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x3 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/303119.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x4 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/628248.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x5 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/957974.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x6 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/872562.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x7 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/519950.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x8 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/100206.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x9 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/173334.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x10 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/103515.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x11 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/168341.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x12 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/485757.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x13 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/397760.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x14 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/886674.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x15 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/192136.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x16 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/987074.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x17 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/390645.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x18 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/663755.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x19 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/137936.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x20 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/137936.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x21 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/161327.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x22 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/104012.L.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x23 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/911849.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x24 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/161327.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii -var x25 /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/548250.R.MSM.NODE2167_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-math 'abs(x-y)' /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/difference.shape.gii -var x /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/NODE2167_${iter_num_last}.curv.affine.ico6.shape.gii -var y /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/NODE2167_${iter_num}.curv.affine.ico6.shape.gii;
diff=$(wb_command -metric-stats /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/difference.shape.gii -reduce MEAN -roi /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2167_frontal_mask.shape.gii);
echo $diff;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/NODE2167_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE2167_msmrefine/NODE2167.final.curv.affine.ico6.shape.gii
