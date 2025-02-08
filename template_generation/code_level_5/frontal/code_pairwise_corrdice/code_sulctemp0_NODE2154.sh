mkdir -p /HPC_work_dir/corrdice_affine_mask/checkNODE2154_msmrefine/;
wb_command -metric-math '(x0+x1+x2+x3+x4)/5' /HPC_work_dir/corrdice_affine_mask/checkNODE2154_msmrefine/NODE2154.sulctemp0.affine.ico6.shape.gii -var x0 /HPC_work_dir/affined_sulc/917255.L.sulc.affine.ico6.shape.gii -var x1 /HPC_work_dir/affined_sulc/342129.R.sulc.affine.ico6.shape.gii -var x2 /HPC_work_dir/affined_sulc/199958.L.sulc.affine.ico6.shape.gii -var x3 /HPC_work_dir/affined_sulc/211720.L.sulc.affine.ico6.shape.gii -var x4 /HPC_work_dir/affined_sulc/199958.R.sulc.affine.ico6.shape.gii &
wait;
