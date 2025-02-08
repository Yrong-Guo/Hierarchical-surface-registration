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
wb_command -metric-math '(x0+x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24+x25+x26+x27+x28+x29+x30+x31+x32+x33+x34+x35)/36' /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/NODE2168_${iter_num}.curv.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/786569.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/287248.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/552544.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x3 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/671855.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x4 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/737960.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x5 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/130720.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x6 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/151930.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x7 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/654350.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x8 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/128127.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x9 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/990366.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x10 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/155231.L.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x11 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/214221.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x12 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/523032.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x13 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/186040.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x14 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/197348.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x15 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/371843.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x16 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/157336.L.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x17 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/186444.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x18 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/108121.L.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x19 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/153227.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x20 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/155231.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x21 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/200917.L.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x22 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/153126.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x23 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/571548.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x24 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/165840.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x25 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/578158.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x26 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/520228.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x27 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/926862.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x28 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/165840.L.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x29 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/695768.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x30 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/138130.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x31 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/158136.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x32 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/131217.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x33 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/206828.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x34 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/169545.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii -var x35 /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/816653.R.MSM.NODE2168_${iter_num}.transformed_and_reprojected.func.gii;
wb_command -metric-merge /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2168_frontal_merged.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/786569.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/287248.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/552544.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/671855.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/737960.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/130720.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/151930.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/654350.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/128127.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/990366.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/155231.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/214221.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/523032.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/186040.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/197348.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/371843.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/157336.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/186444.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/108121.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/153227.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/155231.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/200917.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/153126.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/571548.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/165840.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/578158.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/520228.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/926862.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/165840.L.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/695768.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/138130.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/158136.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/131217.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/206828.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/169545.R.frontal.ico6.shape.gii -metric /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/816653.R.frontal.ico6.shape.gii;
wb_command -metric-reduce /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2168_frontal_merged.shape.gii MAX /HPC_work_dir/frontal_lobe/rotated_deformed_frontal_lobe_corrdice/NODE2168_frontal_mask.shape.gii;

cp /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/NODE2168_${iter_num}.curv.affine.ico6.shape.gii /HPC_work_dir/corrdice_affine_mask/checkNODE2168_msmrefine/NODE2168.final.curv.affine.ico6.shape.gii
