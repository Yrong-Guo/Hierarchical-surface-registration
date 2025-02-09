reg_folder=/your_HPC_working_dir/concatenate_reg
ico_6=/your_HPC_working_dir/sunet.ico-6.surf.gii
output_dir=/your_HPC_working_dir/concatenate_process
output_dir_metrics=/your_HPC_working_dir/concatenate_process_metrics
wb_command -surface-sphere-project-unproject ${reg_folder}/frontal.NODE2115.MSM.NODE2187.sphere.reg.surf.gii ${ico_6} ${reg_folder}/frontal.NODE2187.MSM.NODE2217.sphere.reg.surf.gii ${output_dir}/frontal.NODE2115.to.NODE2217.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2115.curv.affine.ico6.shape.gii ${output_dir}/frontal.NODE2115.to.NODE2217.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/frontal.NODE2115.to.NODE2217.MSMHT.func.gii -area-surfs ${output_dir}/frontal.NODE2115.to.NODE2217.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/frontal.NODE2115.to.NODE2217.sphere.concate.surf.gii ${ico_6} ${reg_folder}/frontal.NODE2217.MSM.NODE2218.sphere.reg.surf.gii ${output_dir}/frontal.NODE2115.to.NODE2218.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2115.curv.affine.ico6.shape.gii ${output_dir}/frontal.NODE2115.to.NODE2218.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/frontal.NODE2115.to.NODE2218.MSMHT.func.gii -area-surfs ${output_dir}/frontal.NODE2115.to.NODE2218.sphere.concate.surf.gii ${ico_6}
