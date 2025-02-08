mkdir -p /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/;
wb_command -metric-math '(x0+x1+x2)/3' /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/NODE1910.sulctemp1.affine.ico6.shape.gii -var x0 /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/212419.R.MSM.NODE1910.final.sulc.shape.gii -var x1 /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/127933.R.MSM.NODE1910.final.sulc.shape.gii -var x2 /HPC_work_dir/corrdice_affine_mask/checkNODE1910_msmrefine/135629.R.MSM.NODE1910.final.sulc.shape.gii &
wait;
