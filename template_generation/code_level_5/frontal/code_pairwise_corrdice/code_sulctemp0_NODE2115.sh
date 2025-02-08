mkdir -p /HPC_work_dir/corrdice_affine_mask/checkNODE2115_msmrefine/;
wb_command -metric-math '(x0+x1+x2)/3' /HPC_work_dir/corrdice_affine_mask/checkNODE2115_msmrefine/NODE2115.sulctemp0.affine.ico6.shape.gii -var x0 /HPC_work_dir/affined_sulc/116221.L.sulc.affine.ico6.shape.gii -var x1 /HPC_work_dir/affined_sulc/165032.L.sulc.affine.ico6.shape.gii -var x2 /HPC_work_dir/affined_sulc/248339.L.sulc.affine.ico6.shape.gii &
wait;
