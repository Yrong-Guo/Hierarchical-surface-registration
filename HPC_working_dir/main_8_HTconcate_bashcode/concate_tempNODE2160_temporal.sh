reg_folder=/your_HPC_working_dir/concatenate_reg
ico_6=/your_HPC_working_dir/sunet.ico-6.surf.gii
output_dir=/your_HPC_working_dir/concatenate_process
output_dir_metrics=/your_HPC_working_dir/concatenate_process_metrics
wb_command -surface-sphere-project-unproject ${reg_folder}/temporal.NODE2160.MSM.NODE2201.sphere.reg.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2201.MSM.NODE2208.sphere.reg.surf.gii ${output_dir}/temporal.NODE2160.to.NODE2208.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2160.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2160.to.NODE2208.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2160.to.NODE2208.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2160.to.NODE2208.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2160.to.NODE2208.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2208.MSM.NODE2210.sphere.reg.surf.gii ${output_dir}/temporal.NODE2160.to.NODE2210.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2160.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2160.to.NODE2210.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2160.to.NODE2210.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2160.to.NODE2210.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2160.to.NODE2210.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2210.MSM.NODE2213.sphere.reg.surf.gii ${output_dir}/temporal.NODE2160.to.NODE2213.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2160.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2160.to.NODE2213.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2160.to.NODE2213.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2160.to.NODE2213.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2160.to.NODE2213.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2213.MSM.NODE2215.sphere.reg.surf.gii ${output_dir}/temporal.NODE2160.to.NODE2215.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2160.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2160.to.NODE2215.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2160.to.NODE2215.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2160.to.NODE2215.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2160.to.NODE2215.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2215.MSM.NODE2217.sphere.reg.surf.gii ${output_dir}/temporal.NODE2160.to.NODE2217.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2160.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2160.to.NODE2217.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2160.to.NODE2217.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2160.to.NODE2217.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/temporal.NODE2160.to.NODE2217.sphere.concate.surf.gii ${ico_6} ${reg_folder}/temporal.NODE2217.MSM.NODE2218.sphere.reg.surf.gii ${output_dir}/temporal.NODE2160.to.NODE2218.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/temporal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2160.curv.affine.ico6.shape.gii ${output_dir}/temporal.NODE2160.to.NODE2218.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/temporal.NODE2160.to.NODE2218.MSMHT.func.gii -area-surfs ${output_dir}/temporal.NODE2160.to.NODE2218.sphere.concate.surf.gii ${ico_6}
