mkdir -p /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/;
wb_command -metric-math '(x0+x1+x2)/3' /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/NODE1910.sulctemp0.affine.ico6.shape.gii -var x0 /HPC_work_dir/affined_sulc/212419.R.sulc.affine.ico6.shape.gii -var x1 /HPC_work_dir/affined_sulc/127933.R.sulc.affine.ico6.shape.gii -var x2 /HPC_work_dir/affined_sulc/135629.R.sulc.affine.ico6.shape.gii &
wait;
