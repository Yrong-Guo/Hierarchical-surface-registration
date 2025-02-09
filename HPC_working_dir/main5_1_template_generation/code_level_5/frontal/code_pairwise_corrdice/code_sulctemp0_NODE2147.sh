mkdir -p /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/;
wb_command -metric-math '(x0+x1+x2+x3)/4' /HPC_work_dir/corrdice_affine_mask/checkNODE2147_msmrefine/NODE2147.sulctemp0.affine.ico6.shape.gii -var x0 /HPC_work_dir/affined_sulc/510225.R.sulc.affine.ico6.shape.gii -var x1 /HPC_work_dir/affined_sulc/510225.L.sulc.affine.ico6.shape.gii -var x2 /HPC_work_dir/affined_sulc/406432.L.sulc.affine.ico6.shape.gii -var x3 /HPC_work_dir/affined_sulc/406432.R.sulc.affine.ico6.shape.gii &
wait;
