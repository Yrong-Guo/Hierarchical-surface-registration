mkdir -p /HPC_work_dir/corrdice_affine_mask/checkNODE1951_msmrefine/;
wb_command -metric-math '(x0+x1+x2+x3+x4+x5)/6' /HPC_work_dir/corrdice_affine_mask/checkNODE1951_msmrefine/NODE1951.sulctemp1.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE1951_msmrefine/130720.L.MSM.NODE1951.final.sulc.shape.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE1951_msmrefine/176239.R.MSM.NODE1951.final.sulc.shape.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE1951_msmrefine/221319.R.MSM.NODE1951.final.sulc.shape.gii -var x3 /HPC_work_dir/corrdice_affine_mask/checkNODE1951_msmrefine/139637.R.MSM.NODE1951.final.sulc.shape.gii -var x4 /HPC_work_dir/corrdice_affine_mask/checkNODE1951_msmrefine/130114.L.MSM.NODE1951.final.sulc.shape.gii -var x5 /HPC_work_dir/corrdice_affine_mask/checkNODE1951_msmrefine/130114.R.MSM.NODE1951.final.sulc.shape.gii &
wait;
