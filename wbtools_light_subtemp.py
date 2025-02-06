import numpy as np



def generate_average_metric_command_unbiastemp(leaf_combine,root_path,root_suffix='.L.sulc.newestwarp.ico6.shape.gii', merge_id=None,output_path=None,output_suffix='.sulc.affine.ico6.shape.gii'):
    command = 'mkdir -p '+ output_path +'/check' + merge_id + '_msmrefine/;\n'
    command = command+'wb_command -metric-math '
    metrics = np.asarray([])
    xs = np.asarray([])
    for i, leaf in enumerate(leaf_combine):
        metrics = np.append(metrics,'-var x'+str(i)+' ' + root_path + '/' +leaf + root_suffix)
        xs = np.append(xs,'x'+str(i))
    metrics = ' '.join(metrics)
    expression = '+'.join(xs)
    command = command +'\'('+expression+')/'+str(len(leaf_combine))+ '\' '+output_path+'/check' + merge_id + '_msmrefine/' + merge_id + output_suffix+' '+ metrics+' &\n'
    command = command+'wait;\n'
    return command




def curv_warp_to_sulc(create_work_dir,simi_method):
    f = open('code_level5/code_pairwise_'+simi_method+'/apply_warp_to_sulc.sh', "w")
    f.write('#!/bin/bash\n'
            'while getopts \'m:t:\' flag; do\n'
            '  case \"${flag}\" in\n'
            '    m) mov_id=\"${OPTARG}\" ;;\n'
            '    t) tar_id=\"${OPTARG}\" ;;\n'
            '    *)\n'
            '      echo \"Usage: $0 [-m mov_id] [-t tar_id]\"\n'
            '      exit 1\n'
            '      ;;\n'
            '  esac\n'
            'done\n'
            'create_work_dir=' + str(create_work_dir) + '\n'
            'WARP=$(ls ${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}*.sphere.reg.surf.gii -tr | tail -n 1);\n'
            'wb_command -metric-resample /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/affined_sulc/${mov_id}.sulc.affine.ico6.shape.gii '
            '${WARP} '
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            'ADAP_BARY_AREA '
            '${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}.final.sulc.shape.gii '
            '-area-surfs '
            '${WARP} '
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii;\n')
    f.close()





def msm_reg_template_2(create_work_dir,firstreg,iter_num,lobe,simi_method): # run 2 direction in parallel
    '''
    The hierarch_reg_process was corrmse_affine_mask_frontal
    :param A:
    :param combined:
    :param firstreg:
    :param iter_num:
    :return:
    '''

    if firstreg==1:
        f = open('code_level5/code_iter_'+simi_method+'/msm_inter_refine_'+str(iter_num)+'.sh', "w")
        f.write('#!/bin/bash\n'
                'while getopts \'m:t:\' flag; do\n'
                '  case \"${flag}\" in\n'
                '    m) mov_id=\"${OPTARG}\" ;;\n'
                '    t) tar_id=\"${OPTARG}\" ;;\n'
                '    *)\n'
                '      echo \"Usage: $0 [-m mov_id] [-t tar_id]\"\n'
                '      exit 1\n'
                '      ;;\n'
                '  esac\n'
                'done\n'
                'create_work_dir='+str(create_work_dir)+'\n'
                'newmsm '
                '--inmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii ' 
                '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/affined_sulc/${mov_id}.sulc.affine.ico6.shape.gii '
                '--refdata=${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${tar_id}.sulctemp0.affine.ico6.shape.gii '
                '-o ${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}. '
                '--conf=${create_work_dir}/msm_config/config_standard_MSM_strain_005 &\n'
                'wait;\n'
                'rm ${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.LR.reg.surf.gii;\n'
                'rm -r ${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.logdir;\n'
                'if [ ! -d "/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'" ];then\n'
                '    mkdir /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+';\n'
                'fi \n'
                'wb_command -metric-resample /scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${mov_id}.curv.affine.ico6.shape.gii '
                '${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.reg.surf.gii '
                '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                'ADAP_BARY_AREA '
                '${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}_0.transformed_and_reprojected.func.gii '
                '-area-surfs '
                '${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.reg.surf.gii '
                '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii;\n'
                'wb_command -metric-resample /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_'+lobe+'_lobe/${mov_id}.'+lobe+'.ico6.shape.gii '
                '${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.reg.surf.gii '
                '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                'ADAP_BARY_AREA '
                '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'/${mov_id}.'+lobe+'.ico6.shape.gii '
                '-area-surfs '
                '${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM_sulc.${tar_id}.sphere.reg.surf.gii '
                '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii;\n'
                'wb_command -metric-math '
                '\'round(x)\' /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'/${mov_id}.'+lobe+'.ico6.shape.gii '
                '-var x /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'/${mov_id}.'+lobe+'.ico6.shape.gii;')

    else:
        f = open('code_level5/code_iter_'+simi_method+'/msm_inter_refine_'+str(iter_num)+'.sh', "w")
        f.write('#!/bin/bash\n'
                'while getopts \'n:m:t:\' flag; do\n'
                '  case \"${flag}\" in\n'
                '    n) iter_num=\"${OPTARG}\" ;;\n'
                '    m) mov_id=\"${OPTARG}\" ;;\n'
                '    t) tar_id=\"${OPTARG}\" ;;\n'
                '    *)\n'
                '      echo \"Usage: $0 [-n iter_num] [-m mov_id] [-t tar_id]\"\n'
                '      exit 1\n'
                '      ;;\n'
                '  esac\n'
                'done\n'
                'iter_num_last=$((${iter_num} - 1))\n'
                'create_work_dir='+str(create_work_dir)+'\n'
                'newmsm '
                '--inmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                '--refmesh=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
                '--indata=/scratch/prj/cortical_imaging_dhcp/Yourong/affined_features/${mov_id}.curv.affine.ico6.shape.gii '
                '--refdata=${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${tar_id}_${iter_num_last}.curv.affine.ico6.shape.gii '
                '-o ${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}_${iter_num}. '
                '--conf=${create_work_dir}/msm_config/config_standard_MSM_strain_005 &\n'
                'wait;\n'
                'rm ${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}_${iter_num}.sphere.LR.reg.surf.gii;\n'
                'rm -r ${create_work_dir}/'+simi_method+'_affine_mask/check${tar_id}_msmrefine/${mov_id}.MSM.${tar_id}_${iter_num}.logdir;\n'
                )
    f.close()


def generate_average_metric_command(leaf_combine,root_path,merge_id,affine_path,file_suffix,firstreg,iter_num,lobe,create_work_dir,simi_method):
    command = 'while getopts \'n:\' flag; do\n'+\
                '  case \"${flag}\" in\n'+\
                '    n) iter_num=\"${OPTARG}\" ;;\n'+\
                '    *)\n'+\
                '      echo \"Usage: $0 [-n iter_num]\"\n'+\
                '      exit 1\n'+\
                '      ;;\n'+\
                '  esac\n'+\
                'done\n'+ \
                'iter_num_last=$((${iter_num} - 1))\n'
    command = command+'wb_command -metric-math '
    metrics = np.asarray([])
    xs = np.asarray([])
    msks = []
    for i, leaf in enumerate(leaf_combine):
        metrics = np.append(metrics,'-var x'+str(i)+' '+root_path+leaf+'.MSM.'+merge_id+file_suffix)
        xs = np.append(xs,'x'+str(i))
    metrics = ' '.join(metrics)
    expression = '+'.join(xs)
    command = command +'\'('+expression+')/'+str(len(leaf_combine))+ '\' '+affine_path+''+merge_id+ '_${iter_num}.curv.affine.ico6.shape.gii'+' '+ metrics+';\n'
    if firstreg != 1:
        command = command + 'wb_command -metric-math \'abs(x-y)\' '+create_work_dir+'/'+simi_method+'_affine_mask/check'+merge_id+'_msmrefine/difference.shape.gii '+\
                '-var x '+create_work_dir+'/'+simi_method+'_affine_mask/check'+merge_id+'_msmrefine/'+merge_id+'_${iter_num_last}.curv.affine.ico6.shape.gii '+\
                '-var y '+create_work_dir+'/'+simi_method+'_affine_mask/check'+merge_id+'_msmrefine/'+merge_id+'_${iter_num}.curv.affine.ico6.shape.gii;\n'+\
                'diff=$(wb_command -metric-stats '+create_work_dir+'/'+simi_method+'_affine_mask/check'+merge_id+'_msmrefine/difference.shape.gii -reduce MEAN -roi /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'/'+merge_id+'_'+lobe+'_mask.shape.gii);\n'+\
                'echo $diff;\n'
    if firstreg == 1:
        for i,leaf in enumerate(leaf_combine):
            msks = np.append(msks,
                             '-metric /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'/' + leaf + '.'+lobe+'.ico6.shape.gii')
            msks = ' '.join(msks)
        command = command + 'wb_command -metric-merge /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'/'+merge_id+'_'+lobe+'_merged.shape.gii '+msks+';\n'
        command = command + 'wb_command -metric-reduce /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'/'+merge_id+'_'+lobe+'_merged.shape.gii MAX /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/rotated_deformed_'+lobe+'_lobe_'+simi_method+'/'+merge_id+'_'+lobe+'_mask.shape.gii;\n'
    output = affine_path+''+merge_id+ '_${iter_num}.curv.affine.ico6.shape.gii'
    return command, output



def wb_metric_mean_std(leaf_combine, root_path , root_suffix, merge_output, mean_output, std_output):
    command = 'wb_command -metric-merge '+merge_output+' '
    metrics = np.asarray([])
    for i, leaf in enumerate(leaf_combine):
        metrics = np.append(metrics,'-metric '+root_path+'/'+leaf+root_suffix)
    metrics = ' '.join(metrics)
    command = command+metrics+';\n'
    command
    return command


def wb_metric_mean_std(leaf_combine, root_path , root_suffix, merge_output, mean_output, std_output):
    command = 'wb_command -metric-merge '+merge_output+' '
    metrics = np.asarray([])
    for i, leaf in enumerate(leaf_combine):
        metrics = np.append(metrics,'-metric '+root_path+'/'+leaf+root_suffix)
    metrics = ' '.join(metrics)
    command = command+metrics+';\n'
    command
    return command