reg_folder=/your_HPC_working_dir/concatenate_reg
ico_6=/your_HPC_working_dir/sunet.ico-6.surf.gii
output_dir=/your_HPC_working_dir/concatenate_process
output_dir_metrics=/your_HPC_working_dir/concatenate_process_metrics
wb_command -surface-sphere-project-unproject ${reg_folder}/temporal.NODE2166.MSM.NODE2190.sphere.reg.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2190.MSM.NODE2209.sphere.reg.surf.gii ${output_dir}/temporal.NODE2166.to.NODE2209.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2166.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2166.to.NODE2209.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2166.to.NODE2209.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2166.to.NODE2209.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2166.to.NODE2209.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2209.MSM.NODE2216.sphere.reg.surf.gii ${output_dir}/temporal.NODE2166.to.NODE2216.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2166.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2166.to.NODE2216.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2166.to.NODE2216.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2166.to.NODE2216.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2166.to.NODE2216.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2216.MSM.NODE2218.sphere.reg.surf.gii ${output_dir}/temporal.NODE2166.to.NODE2218.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2166.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2166.to.NODE2218.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2166.to.NODE2218.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2166.to.NODE2218.sphere.concate.surf.gii ${ico_6}
