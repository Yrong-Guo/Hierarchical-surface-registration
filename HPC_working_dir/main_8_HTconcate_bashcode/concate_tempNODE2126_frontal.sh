reg_folder=/your_HPC_working_dir/concatenate_reg
ico_6=/your_HPC_working_dir/sunet.ico-6.surf.gii
output_dir=/your_HPC_working_dir/concatenate_process
output_dir_metrics=/your_HPC_working_dir/concatenate_process_metrics
wb_command -surface-sphere-project-unproject ${reg_folder}/frontal.NODE2126.MSM.NODE2196.sphere.reg.surf.gii ${ico_6} ${reg_folder}/frontal.NODE2196.MSM.NODE2206.sphere.reg.surf.gii ${output_dir}/frontal.NODE2126.to.NODE2206.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2126.curv.affine.ico6.shape.gii ${output_dir}/frontal.NODE2126.to.NODE2206.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/frontal.NODE2126.to.NODE2206.MSMHT.func.gii -area-surfs ${output_dir}/frontal.NODE2126.to.NODE2206.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/frontal.NODE2126.to.NODE2206.sphere.concate.surf.gii ${ico_6} ${reg_folder}/frontal.NODE2206.MSM.NODE2214.sphere.reg.surf.gii ${output_dir}/frontal.NODE2126.to.NODE2214.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2126.curv.affine.ico6.shape.gii ${output_dir}/frontal.NODE2126.to.NODE2214.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/frontal.NODE2126.to.NODE2214.MSMHT.func.gii -area-surfs ${output_dir}/frontal.NODE2126.to.NODE2214.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/frontal.NODE2126.to.NODE2214.sphere.concate.surf.gii ${ico_6} ${reg_folder}/frontal.NODE2214.MSM.NODE2215.sphere.reg.surf.gii ${output_dir}/frontal.NODE2126.to.NODE2215.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2126.curv.affine.ico6.shape.gii ${output_dir}/frontal.NODE2126.to.NODE2215.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/frontal.NODE2126.to.NODE2215.MSMHT.func.gii -area-surfs ${output_dir}/frontal.NODE2126.to.NODE2215.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/frontal.NODE2126.to.NODE2215.sphere.concate.surf.gii ${ico_6} ${reg_folder}/frontal.NODE2215.MSM.NODE2216.sphere.reg.surf.gii ${output_dir}/frontal.NODE2126.to.NODE2216.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2126.curv.affine.ico6.shape.gii ${output_dir}/frontal.NODE2126.to.NODE2216.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/frontal.NODE2126.to.NODE2216.MSMHT.func.gii -area-surfs ${output_dir}/frontal.NODE2126.to.NODE2216.sphere.concate.surf.gii ${ico_6}
wb_command -surface-sphere-project-unproject ${output_dir}/frontal.NODE2126.to.NODE2216.sphere.concate.surf.gii ${ico_6} ${reg_folder}/frontal.NODE2216.MSM.NODE2218.sphere.reg.surf.gii ${output_dir}/frontal.NODE2126.to.NODE2218.sphere.concate.surf.gii
wb_command -metric-resample /your_HPC_working_dir/frontal_lobe/level5_unbias_corrdice/corrdice_affine_mask/final_temps/NODE2126.curv.affine.ico6.shape.gii ${output_dir}/frontal.NODE2126.to.NODE2218.sphere.concate.surf.gii ${ico_6} ADAP_BARY_AREA ${output_dir_metrics}/frontal.NODE2126.to.NODE2218.MSMHT.func.gii -area-surfs ${output_dir}/frontal.NODE2126.to.NODE2218.sphere.concate.surf.gii ${ico_6}
