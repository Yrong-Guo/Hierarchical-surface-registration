reg_folder=/your_HPC_working_dir/concatenate_reg
ico_6=/your_HPC_working_dir/sunet.ico-6.surf.gii
output_dir=/your_HPC_working_dir/concatenate_process
output_dir_metrics=/your_HPC_working_dir/concatenate_process_metrics
wb_command -surface-sphere-project-unproject ${reg_folder}/parietal.NODE2187.MSM.NODE2194.sphere.reg.surf.gii ${ico_6} ${reg_folder}/parietal.NODE2194.MSM.NODE2205.sphere.reg.surf.gii ${output_dir}/parietal.NODE2187.to.NODE2205.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2187.curv.affine.ico6.shape.gii ${output_dir}/parietal.NODE2187.to.NODE2205.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/parietal.NODE2187.to.NODE2205.MSMHT.func.gii -area-surfs ${output_dir}/parietal.NODE2187.to.NODE2205.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/parietal.NODE2187.to.NODE2205.sphere.concate.surf.gii ${ico_6} ${reg_folder}/parietal.NODE2205.MSM.NODE2209.sphere.reg.surf.gii ${output_dir}/parietal.NODE2187.to.NODE2209.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2187.curv.affine.ico6.shape.gii ${output_dir}/parietal.NODE2187.to.NODE2209.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/parietal.NODE2187.to.NODE2209.MSMHT.func.gii -area-surfs ${output_dir}/parietal.NODE2187.to.NODE2209.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/parietal.NODE2187.to.NODE2209.sphere.concate.surf.gii ${ico_6} ${reg_folder}/parietal.NODE2209.MSM.NODE2215.sphere.reg.surf.gii ${output_dir}/parietal.NODE2187.to.NODE2215.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2187.curv.affine.ico6.shape.gii ${output_dir}/parietal.NODE2187.to.NODE2215.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/parietal.NODE2187.to.NODE2215.MSMHT.func.gii -area-surfs ${output_dir}/parietal.NODE2187.to.NODE2215.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/parietal.NODE2187.to.NODE2215.sphere.concate.surf.gii ${ico_6} ${reg_folder}/parietal.NODE2215.MSM.NODE2216.sphere.reg.surf.gii ${output_dir}/parietal.NODE2187.to.NODE2216.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2187.curv.affine.ico6.shape.gii ${output_dir}/parietal.NODE2187.to.NODE2216.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/parietal.NODE2187.to.NODE2216.MSMHT.func.gii -area-surfs ${output_dir}/parietal.NODE2187.to.NODE2216.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/parietal.NODE2187.to.NODE2216.sphere.concate.surf.gii ${ico_6} ${reg_folder}/parietal.NODE2216.MSM.NODE2218.sphere.reg.surf.gii ${output_dir}/parietal.NODE2187.to.NODE2218.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/parietal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2187.curv.affine.ico6.shape.gii ${output_dir}/parietal.NODE2187.to.NODE2218.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/parietal.NODE2187.to.NODE2218.MSMHT.func.gii -area-surfs ${output_dir}/parietal.NODE2187.to.NODE2218.sphere.concate.surf.gii ${ico_6}
