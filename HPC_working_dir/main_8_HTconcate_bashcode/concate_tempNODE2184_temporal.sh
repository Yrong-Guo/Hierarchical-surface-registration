reg_folder=/your_HPC_working_dir/concatenate_reg
ico_6=/your_HPC_working_dir/sunet.ico-6.surf.gii
output_dir=/your_HPC_working_dir/concatenate_process
output_dir_metrics=/your_HPC_working_dir/concatenate_process_metrics
wb_command -surface-sphere-project-unproject ${reg_folder}/temporal.NODE2184.MSM.NODE2193.sphere.reg.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2193.MSM.NODE2199.sphere.reg.surf.gii ${output_dir}/temporal.NODE2184.to.NODE2199.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2184.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2184.to.NODE2199.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2184.to.NODE2199.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2184.to.NODE2199.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2184.to.NODE2199.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2199.MSM.NODE2204.sphere.reg.surf.gii ${output_dir}/temporal.NODE2184.to.NODE2204.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2184.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2184.to.NODE2204.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2184.to.NODE2204.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2184.to.NODE2204.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2184.to.NODE2204.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2204.MSM.NODE2209.sphere.reg.surf.gii ${output_dir}/temporal.NODE2184.to.NODE2209.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2184.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2184.to.NODE2209.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2184.to.NODE2209.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2184.to.NODE2209.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2184.to.NODE2209.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2209.MSM.NODE2216.sphere.reg.surf.gii ${output_dir}/temporal.NODE2184.to.NODE2216.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2184.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2184.to.NODE2216.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2184.to.NODE2216.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2184.to.NODE2216.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2184.to.NODE2216.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2216.MSM.NODE2218.sphere.reg.surf.gii ${output_dir}/temporal.NODE2184.to.NODE2218.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2184.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2184.to.NODE2218.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2184.to.NODE2218.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2184.to.NODE2218.sphere.concate.surf.gii ${ico_6}
