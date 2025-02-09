reg_folder=/your_HPC_working_dir/concatenate_reg
ico_6=/your_HPC_working_dir/sunet.ico-6.surf.gii
output_dir=/your_HPC_working_dir/concatenate_process
output_dir_metrics=/your_HPC_working_dir/concatenate_process_metrics
wb_command -surface-sphere-project-unproject ${reg_folder}/parietal.NODE1856.MSM.NODE2217.sphere.reg.surf.gii ${ico_6} ${reg_folder}/parietal.NODE2217.MSM.NODE2218.sphere.reg.surf.gii ${output_dir}/parietal.NODE1856.to.NODE2218.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE1856.curv.affine.ico6.shape.gii ${output_dir}/parietal.NODE1856.to.NODE2218.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/parietal.NODE1856.to.NODE2218.MSMHT.func.gii -area-surfs ${output_dir}/parietal.NODE1856.to.NODE2218.sphere.concate.surf.gii ${ico_6}
