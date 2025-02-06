"""
execute wb_command using python prepared as functions
1. merge process
2. apply deform and resample
"""
import subprocess
from subprocess import Popen
import os
from threading import Timer

import numpy as np
import os


"""Change affine_folder Change config"""
def msm_reg(sub1,sub2,merge_id,process_path,temp_path, work_dir, sub_dir,inter_templates,leaf_A, leaf_B, leaf_combine,lobe): # run 2 direction in parallel
    if not os.path.exists('msm_merge_files_'+lobe):
        os.makedirs('msm_merge_files_'+lobe)

    f = open('msm_merge_files_'+lobe+'/msm_merge_'+merge_id+'.sh', "w")
    f.write('#!/bin/bash\n'
            'temp_path='+temp_path+';\n'
            'ico6_path=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii;\n'
            'process_path='+process_path+';\n'
            'msmconfig_path=/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/'+lobe+'_lobe/level5_unbias_corrdice/msm_config/config_standard_MSM_strain_005;\n'
            'sub_dir='+sub_dir+';\n'
            'mkdir -p ${process_path}\n'
            '\n'                            
            'msm_ubuntu_v3 '+\
            '--inmesh=${ico6_path} '+\
            '--refmesh=${ico6_path} '+\
            '--indata=${temp_path}/'+sub1+'.curv.affine.ico6.shape.gii '+\
            '--refdata=${temp_path}/'+sub2+'.curv.affine.ico6.shape.gii '+\
            '-o ${process_path}/'+sub1+'.MSM.'+sub2+'. '+\
            '--conf=${msmconfig_path} &\n'+ \
            '\n'
            'msm_ubuntu_v3 '+\
            '--inmesh=${ico6_path} '+\
            '--refmesh=${ico6_path} '+\
            '--indata=${temp_path}/'+sub2+'.curv.affine.ico6.shape.gii '+\
            '--refdata=${temp_path}/'+sub1+'.curv.affine.ico6.shape.gii '+\
            '-o ${process_path}/'+sub2+'.MSM.'+sub1+'. '+\
            '--conf=${msmconfig_path} &\n'+ \
            'wait;\n'
            '\n' 
            'mv ${process_path}/' +sub1+ '.MSM.' +sub2+ '.sphere.reg.surf.gii ' + \
            '${process_path}/' +sub1+ '.MSM.' +sub2+ '.ico-6.sphere.surf.gii;\n'
            'mv ${process_path}/' +sub2+ '.MSM.' +sub1+ '.sphere.reg.surf.gii '+\
            '${process_path}/' +sub2+ '.MSM.' +sub1+ '.ico-6.sphere.surf.gii;\n'
            '\n' 
            'wb_command -surface-sphere-project-unproject ${ico6_path} ${process_path}/'+ sub1 + '.MSM.' + sub2 + '.ico-6.sphere.surf.gii '
            '${ico6_path} ${process_path}/'+ sub1 + '.MSM.' + sub2 + '.inv.ico-6.sphere.surf.gii;\n'
            'wb_command -surface-sphere-project-unproject ${ico6_path} ${process_path}/'+ sub2 + '.MSM.' + sub1 + '.ico-6.sphere.surf.gii '
            '${ico6_path} ${process_path}/'+ sub2 + '.MSM.' + sub1 + '.inv.ico-6.sphere.surf.gii;\n'
            'wb_command -surface-average ${process_path}/'+ sub1 + '.to.' + sub2 + '.avg.ico-6.sphere.surf.gii '
            '-surf ${process_path}/'+ sub2 + '.MSM.' + sub1 + '.inv.ico-6.sphere.surf.gii '
            '-surf ${process_path}/'+ sub1 + '.MSM.' + sub2 + '.ico-6.sphere.surf.gii;\n'
            'wb_command -surface-average ${process_path}/'+ sub2 + '.to.' + sub1 + '.avg.ico-6.sphere.surf.gii '
            '-surf ${process_path}/'+ sub1 + '.MSM.' + sub2 + '.inv.ico-6.sphere.surf.gii '
            '-surf ${process_path}/'+ sub2 + '.MSM.' + sub1 + '.ico-6.sphere.surf.gii;\n'
            'wb_command -surface-modify-sphere ${process_path}/'+ sub1 + '.to.' + sub2 + '.avg.ico-6.sphere.surf.gii '
            '100 ${process_path}/'+ sub1 + '.to.' + sub2 + '.avg.ico-6.sphere.surf.gii '
            '-recenter &\n'
            'wb_command -surface-modify-sphere ${process_path}/'+ sub2 + '.to.' + sub1 + '.avg.ico-6.sphere.surf.gii '
            '100 ${process_path}/'+ sub2 + '.to.' + sub1 + '.avg.ico-6.sphere.surf.gii '
            '-recenter &\n'
            'wait;\n'
            '\n'
            'wb_command -surface-average ${process_path}/'+ sub1 + '.to.' + sub2 + '.avg.mid.ico-6.sphere.surf.gii '
            '-surf ${process_path}/'+ sub1 + '.to.' + sub2 + '.avg.ico-6.sphere.surf.gii '
            '-surf ${ico6_path};\n'
            'wb_command -surface-average ${process_path}/'+ sub2 + '.to.' + sub1 + '.avg.mid.ico-6.sphere.surf.gii '
            '-surf ${process_path}/'+ sub2 + '.to.' + sub1 + '.avg.ico-6.sphere.surf.gii '
            '-surf ${ico6_path};\n'
            'wb_command -surface-modify-sphere ${process_path}/'+ sub1 + '.to.' + sub2 + '.avg.mid.ico-6.sphere.surf.gii '
            '100 ${process_path}/'+ sub1 + '.to.' + sub2 + '.avg.mid.ico-6.sphere.surf.gii '
            '-recenter &\n'
            'wb_command -surface-modify-sphere ${process_path}/'+ sub2 + '.to.' + sub1 + '.avg.mid.ico-6.sphere.surf.gii '
            '100 ${process_path}/'+ sub2 + '.to.' + sub1 + '.avg.mid.ico-6.sphere.surf.gii '
            '-recenter &\n'
            'wait;\n'
            '\n'
            + leaf_add_warp(sub1, sub2, merge_id, process_path, work_dir,inter_templates,leaf_A, leaf_B) +
            'wb_command -surface-average ${process_path}/'+ merge_id + '.dedriftwarp.ico-6.sphere.surf.gii '
            + generate_average_dedrift_warp_flag(leaf_combine, process_path, merge_id) + ';\n'
            'wb_command -surface-modify-sphere ${process_path}/' + merge_id + '.dedriftwarp.ico-6.sphere.surf.gii '
            '100 ${process_path}/'
             + merge_id + '.dedriftwarp.ico-6.sphere.surf.gii '
            '-recenter &\n'
            'wait;\n'
            '\n'
            'for leaf in ' + ' '.join(leaf_combine) + ';do '
            'wb_command -surface-sphere-project-unproject ${process_path}/${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii '
            '${ico6_path} '
            '${process_path}/'+ merge_id + '.dedriftwarp.ico-6.sphere.surf.gii '
            '${process_path}/${leaf}.to.' + merge_id + '.warp.dedrifted.ico-6.sphere.surf.gii;\n'
            '\n'
            'wb_command -metric-resample ${sub_dir}/${leaf}.curv.affine.ico6.shape.gii '
            '${process_path}/${leaf}.to.' + merge_id + '.warp.dedrifted.ico-6.sphere.surf.gii '
            '${ico6_path} '
            'ADAP_BARY_AREA ${process_path}/${leaf}.curv.newestwarp.ico6.shape.gii '
            '-area-surfs '
            '${process_path}/${leaf}.to.' + merge_id + '.warp.dedrifted.ico-6.sphere.surf.gii '
            '${ico6_path};\n'
            'done;\n'
            '\n'
            + generate_average_metric_command(leaf_combine, process_path, merge_id) + '\n'
            'wb_command -metric-palette ${temp_path}/' + merge_id + '.curv.affine.ico6.shape.gii MODE_AUTO_SCALE_PERCENTAGE -palette-name ROY-BIG-BL;\n'
)
    f.close()
    # metric resample -area-surfs sphere ....
    # + process_path + '${leaf}.to.' + merge_id + '.warp.dedrifted.ico-6.sphere.surf.gii '
    # '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii;\n '





def generate_average_dedrift_warp_flag(leaf_combine,process_path,merge_id):
    '''
    function to generate -surf for wb_command -surface-average. The actual file of -surf is generated in leaf_add_warp()
    :param leaf_combine:
    :param process_path:
    :param merge_id:
    :return:
    '''
    dedrift_warps = np.asarray([])
    for i in leaf_combine:
        dedrift_warps = np.append(dedrift_warps,'-surf ${process_path}/'+i+'.to.'+merge_id+'.warp.inv.ico-6.sphere.surf.gii')
    dedrift_warps_new = ' '.join(dedrift_warps)
    return dedrift_warps_new

def generate_average_metric_command(leaf_combine,process_path,merge_id):
    command = 'wb_command -metric-math '
    metrics = np.asarray([])
    xs = np.asarray([])
    for i, leaf in enumerate(leaf_combine):
        metrics = np.append(metrics,'-var x'+str(i)+' ${process_path}/'+leaf+'.curv.newestwarp.ico6.shape.gii')
        xs = np.append(xs,'x'+str(i))
    metrics = ' '.join(metrics)
    expression = '+'.join(xs)
    command = command +'\'('+expression+')/'+str(len(leaf_combine))+ '\' ${temp_path}/'+merge_id+'.curv.affine.ico6.shape.gii'+' '+ metrics+';'
    return command

def leaf_add_warp(sub1,sub2,merge_id,process_path,work_dir,inter_templates,leaf_A,leaf_B):
    '''
    concatenate the last warp with the new one.
    calculate the inverse of registration (individual->current template) in the cluster
    Note for individual subject, don't need to concatenate, I just changed the file name
    :param sub1:
    :param sub2:
    :param merge_id:
    :param process_path:
    :param leaf_A:
    :param leaf_B:
    :return:
    '''
    command = 'work_dir='+work_dir+';\n'

    if 'NODE' in sub1:
        if sub1 in inter_templates:
            command = command + 'iter_num_=$(ls ${work_dir}/check' + sub1 + '_msmrefine/' + sub1 + '_*.curv.affine.ico6.shape.gii -rt | tail -n 1 | grep -Eo "_[0-9]+.curv")\n' \
                                                                                'iter_num=$(echo ${iter_num_} | grep -Eo "[0-9]+");\n'
            command = command + \
                      'for leaf in ' + ' '.join(leaf_A) + ';do ' \
                      + 'cp ${work_dir}/check' + sub1 + '_msmrefine/${leaf}.MSM.'+sub1+'_${iter_num}.sphere.reg.surf.gii ${process_path}/${leaf}.to.' + sub1 + '.warp.ico-6.sphere.surf.gii;\n' \
                      + 'wb_command -set-structure ${process_path}/${leaf}.to.' + sub1 + '.warp.ico-6.sphere.surf.gii CORTEX_LEFT;\n' \
                      + 'wb_command -surface-sphere-project-unproject ${process_path}/${leaf}.to.' + sub1 + '.warp.ico-6.sphere.surf.gii ' \
                      + '${ico6_path} ' \
                        '${process_path}/' + sub1 + '.to.' + sub2 + '.avg.mid.ico-6.sphere.surf.gii ' \
                        '${process_path}/${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii;\n'
        else:
            command = command+\
                      'for leaf in ' + ' '.join(leaf_A) + ';do '\
                      +'wb_command -surface-sphere-project-unproject ${process_path}/${leaf}.to.' + sub1 + '.warp.ico-6.sphere.surf.gii '\
                      +'${ico6_path} '\
                      '${process_path}/' +sub1 + '.to.' + sub2 + '.avg.mid.ico-6.sphere.surf.gii '\
                      '${process_path}/${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii;\n'

    else:
        command = command+\
                  'for leaf in ' + ' '.join(leaf_A) + ';do '\
                  +'mv ${process_path}/' + sub1 + '.to.' + sub2 + '.avg.mid.ico-6.sphere.surf.gii ' \
                  '${process_path}/${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii;\n'
    command = command \
              +'wb_command -surface-sphere-project-unproject ${ico6_path} '\
              '${process_path}/${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii '\
              '${ico6_path} '\
              '${process_path}/${leaf}.to.' + merge_id + '.warp.inv.ico-6.sphere.surf.gii;\n'\
              +'done;\n\n'


    if 'NODE' in sub2:
        if sub2 in inter_templates:
            command = command + 'iter_num_=$(ls ${work_dir}/check' + sub2 + '_msmrefine/' + sub2 + '_*.curv.affine.ico6.shape.gii -rt | tail -n 1 | grep -Eo "_[0-9]+.curv")\n' \
                                                                                'iter_num=$(echo ${iter_num_} | grep -Eo "[0-9]+");\n'
            command = command + \
                      'for leaf in ' + ' '.join(leaf_B) + ';do ' \
                      + 'cp ${work_dir}/check' + sub2 + '_msmrefine/${leaf}.MSM.' + sub2 + '_${iter_num}.sphere.reg.surf.gii ${process_path}/${leaf}.to.' + sub2 + '.warp.ico-6.sphere.surf.gii;\n' \
                      + 'wb_command -set-structure ${process_path}/${leaf}.to.' + sub1 + '.warp.ico-6.sphere.surf.gii CORTEX_LEFT;\n' \
                      + 'wb_command -surface-sphere-project-unproject ${process_path}/${leaf}.to.' + sub2 + '.warp.ico-6.sphere.surf.gii ' \
                      + '${ico6_path} ' \
                        '${process_path}/' + sub2 + '.to.' + sub1 + '.avg.mid.ico-6.sphere.surf.gii ' \
                        '${process_path}/${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii;\n'
        else:
            command = command + \
                      'for leaf in ' + ' '.join(leaf_B) + ';do ' \
                      + 'wb_command -surface-sphere-project-unproject ${process_path}/${leaf}.to.' + sub2 + '.warp.ico-6.sphere.surf.gii ' \
                      + '${ico6_path} ' \
                        '${process_path}/' + sub2 + '.to.' + sub1 + '.avg.mid.ico-6.sphere.surf.gii ' \
                        '${process_path}/${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii;\n'
    else:
        command = command+\
                  'for leaf in ' + ' '.join(leaf_B) + ';do '\
                  +'mv ${process_path}/' + sub2 + '.to.' + sub1 + '.avg.mid.ico-6.sphere.surf.gii ' \
                  '${process_path}/${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii;\n'
    command = command \
              + 'wb_command -surface-sphere-project-unproject ${ico6_path} ' \
              + process_path + '${leaf}.to.' + merge_id + '.warp.ico-6.sphere.surf.gii ' \
              + '${ico6_path} ' \
              + process_path + '${leaf}.to.' + merge_id + '.warp.inv.ico-6.sphere.surf.gii;\n' \
              + 'done;\n'
    return command

def deform_dedrift_resample(sub1,sub2,merge_id,size_sub1, size_sub2,process_path,affine_path, leaf_A, leaf_B, leaf_combine):
    f = open('deform_dedrift_resample_msm_2.sh', "w")
    f.write('#!/bin/bash\n'
            'wb_dir=/home/yg21/Downloads/workbench/bin_linux64/;\n'
            'wb_command -surface-sphere-project-unproject /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            +process_path+sub1+'.MSM.'+sub2+'.ico-6.sphere.surf.gii '
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            +process_path+sub1+'.MSM.'+sub2+'.inv.ico-6.sphere.surf.gii;\n'
            'wb_command -surface-sphere-project-unproject /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            +process_path+sub2+'.MSM.'+sub1+'.ico-6.sphere.surf.gii '
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            +process_path+sub2+'.MSM.'+sub1+'.inv.ico-6.sphere.surf.gii;\n'
            'wb_command -surface-average '+process_path+sub1+'.to.'+sub2+'.avg.ico-6.sphere.surf.gii '
            '-surf '+process_path+sub2+'.MSM.'+sub1+'.inv.ico-6.sphere.surf.gii '
            '-surf '+process_path+sub1+'.MSM.'+sub2+'.ico-6.sphere.surf.gii;\n'
            'wb_command -surface-average '+process_path+sub2+'.to.'+sub1+'.avg.ico-6.sphere.surf.gii '
            '-surf '+process_path+sub1+'.MSM.'+sub2+'.inv.ico-6.sphere.surf.gii '
            '-surf '+process_path+sub2+'.MSM.'+sub1+'.ico-6.sphere.surf.gii;\n'
            'wb_command -surface-modify-sphere '+process_path+sub1+'.to.'+sub2+'.avg.ico-6.sphere.surf.gii '
            '100 '
            +process_path+sub1+'.to.'+sub2+'.avg.ico-6.sphere.surf.gii '
            '-recenter;\n'
            'wb_command -surface-modify-sphere '+process_path+sub2+'.to.'+sub1+'.avg.ico-6.sphere.surf.gii '
            '100 '
            +process_path+sub2+'.to.'+sub1+'.avg.ico-6.sphere.surf.gii '
            '-recenter;\n'
            'wb_command -surface-average '+process_path+sub1+'.to.'+sub2+'.avg.mid.ico-6.sphere.surf.gii '
            '-surf '+process_path+sub1+'.to.'+sub2+'.avg.ico-6.sphere.surf.gii '
            '-surf /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii;\n'
            'wb_command -surface-average '+process_path+sub2+'.to.'+sub1+'.avg.mid.ico-6.sphere.surf.gii '
            '-surf '+process_path+sub2+'.to.'+sub1+'.avg.ico-6.sphere.surf.gii '
            '-surf /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii;\n'
            'wb_command -surface-modify-sphere '+process_path+sub1+'.to.'+sub2+'.avg.mid.ico-6.sphere.surf.gii '
            '100 '
            +process_path+sub1+'.to.'+sub2+'.avg.mid.ico-6.sphere.surf.gii '
            '-recenter;\n'
            'wb_command -surface-modify-sphere '+process_path+sub2+'.to.'+sub1+'.avg.mid.ico-6.sphere.surf.gii '
            '100 '
            +process_path+sub2+'.to.'+sub1+'.avg.mid.ico-6.sphere.surf.gii '
            '-recenter;\n'
            # 'for leaf in '+' '.join(leaf_A)+';do '
            # 'wb_command -surface-sphere-project-unproject '+process_path+'${leaf}.to.'+sub1+'.warp.ico-6.sphere.surf.gii '
            # '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            # +process_path+sub1+'.to.'+sub2+'.avg.mid.ico-6.sphere.surf.gii '
            # +process_path+'${leaf}.to.'+merge_id+'.warp.ico-6.sphere.surf.gii;\n'
            # 'wb_command -surface-sphere-project-unproject /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            # +process_path+'${leaf}.to.'+merge_id+'.warp.ico-6.sphere.surf.gii '
            # '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            # +process_path+'${leaf}.to.'+merge_id+'.warp.inv.ico-6.sphere.surf.gii;\n'
            # 'done;\n'
            # 'for leaf in '+' '.join(leaf_B)+';do '
            # 'wb_command -surface-sphere-project-unproject '+process_path+'${leaf}.to.'+sub2+'.warp.ico-6.sphere.surf.gii '
            # '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            # +process_path+sub2+'.to.'+sub1+'.avg.mid.ico-6.sphere.surf.gii '
            # +process_path+'${leaf}.to.'+merge_id+'.warp.ico-6.sphere.surf.gii;\n'
            # 'wb_command -surface-sphere-project-unproject /scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            # +process_path+'${leaf}.to.'+merge_id+'.warp.ico-6.sphere.surf.gii '
            # '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            # +process_path+'${leaf}.to.'+merge_id+'.warp.inv.ico-6.sphere.surf.gii;\n'
            # 'done;\n'
            +leaf_add_warp(sub1,sub2,merge_id,process_path,leaf_A,leaf_B)+
            'wb_command -surface-average '+process_path+merge_id+'.dedriftwarp.ico-6.sphere.surf.gii '
            +generate_average_dedrift_warp_flag(leaf_combine,process_path,merge_id)+';\n'
            'wb_command -surface-modify-sphere '+process_path+merge_id+'.dedriftwarp.ico-6.sphere.surf.gii '
            '100 '
            +process_path+merge_id+'.dedriftwarp.ico-6.sphere.surf.gii '
            '-recenter;\n'
            'for leaf in ' + ' '.join(leaf_combine) + ';do '
            'wb_command -surface-sphere-project-unproject '+process_path+'${leaf}.to.'+merge_id+'.warp.ico-6.sphere.surf.gii '
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            + process_path + merge_id + '.dedriftwarp.ico-6.sphere.surf.gii '
            +process_path+'${leaf}.to.'+merge_id+'.warp.dedrifted.ico-6.sphere.surf.gii;\n'
            'wb_command -metric-resample '
            +affine_path+'${leaf}.sulc.affine.ico6.shape.gii '
            +process_path+'${leaf}.to.'+merge_id+'.warp.dedrifted.ico-6.sphere.surf.gii '
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii '
            'ADAP_BARY_AREA '+process_path+'${leaf}.sulc.newestwarp.ico6.shape.gii '
            '-area-surfs '
            +process_path+'${leaf}.to.'+merge_id+'.warp.dedrifted.ico-6.sphere.surf.gii '
            '/scratch/prj/cortical_imaging_dhcp/Yourong/hierarch/sunet.ico-6.surf.gii;\n '
            'done;\n'
            +generate_average_metric_command(leaf_combine,process_path,merge_id,affine_path)+'\n'
            'wb_command -metric-palette '+affine_path+''+merge_id+'.sulc.affine.ico6.shape.gii MODE_AUTO_SCALE_PERCENTAGE -palette-name ROY-BIG-BL;\n'
    )
    f.close()




def wb_metric_mean_std(leaf_combine, root_path , root_suffix, merge_output, mean_output, std_output):
    command = 'wb_command -metric-merge '+merge_output+' '
    metrics = np.asarray([])
    for i, leaf in enumerate(leaf_combine):
        metrics = np.append(metrics,'-metric '+root_path+'/'+leaf+root_suffix)
    metrics = ' '.join(metrics)
    command = command+metrics+';\n'
    command
    return command