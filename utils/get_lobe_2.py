"""
extract frontal lobe, temporal lobe... from HCP aparc registered to msmsulc global template
generate a mask
not fit for pairwise registration!!!
edited by Yourong Guo 2022.05.18
"""
import nibabel as nib
import numpy as np
from operator import itemgetter

'load in an image'
# img = nib.load(
#     '/home/yg21/YourongGuo/normativemodel/code3_tohcptemp/DDR_Coarse_tohcptemp/DDR_Coarse/Deformation_results/100206.DDR.L.sulc.affine.ico6.shape.gii').darrays[0].data
# img_header = nib.load(
#     '/home/yg21/YourongGuo/normativemodel/code3_tohcptemp/DDR_Coarse_tohcptemp/DDR_Coarse/Deformation_results/100206.DDR.L.sulc.affine.ico6.shape.gii')

"""name the lobe"""
# lobe = 'parietal'

def get_lobe(lobe = None,id = None, aparc_dir='/home/yg21/YourongGuo/normativemodel/hierarc_hcp/rotated_lobe_label/',aparc_suffix = '.L.aparc.affine.ico6.label.gii'):
    regions = nib.load(aparc_dir +'/'+ id + aparc_suffix)
    # region_dict = regions.labeltable.get_labels_as_dict()  # key into the LabelTable’s labels
    # region_dict_new = dict(zip(region_dict.values(), region_dict.keys()))

    'lobe'
    frontal_lobe = [27,26,2,3,24,17,18,19,20,23,12,32,14,28]
    parietal_lobe = [22,31,29,25,10,8]+[11,5,21,13] # (parietal + occipital+ 8__inferiorparietal)
    temporal_lobe = [34,30,1,15,7,33,16,6,9] +[35]# temporal + insula 35
    brain = frontal_lobe+parietal_lobe+temporal_lobe
    # temporal_lobe_1 = [34, 30, 1, 15, 7, 33, 16, 6, 9]  # temporal + insula 35

    #save masks and ids of different lobes in dictionary
    masks = {}
    ROI_IDs = {}
    for lobe in ['frontal','parietal','temporal','brain']:
        regions_mask = regions.darrays[0].data
        ROI_id = np.asarray([])

        if lobe == 'frontal':
            lobeid = frontal_lobe
        elif lobe == 'parietal':
            lobeid = parietal_lobe
        elif lobe == 'temporal':
            lobeid = temporal_lobe
        elif lobe == 'brain':
            lobeid = brain

        for item in lobeid:
            ROI_id = np.append(ROI_id, np.where(regions_mask == item))
            ROI_id = ROI_id.astype('int32')

        regions_mask = np.zeros((regions_mask.shape))
        regions_mask[ROI_id] = 1
        # reshape to column
        regions_mask = np.reshape(regions_mask, (-1, 1))

        masks[lobe] = regions_mask
        ROI_IDs[lobe] = ROI_id

    '''turn on when making mask'''
    # img_header.darrays[0].data = regions_mask
    # nib.save(img_header, '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/'+id+'.parietalmask.ico6.shape.gii')
    return ROI_IDs, masks

# img_header.darrays[0].data = regions_mask
#
# nib.save(img_header, '/home/yg21/YourongGuo/normativemodel/medialwall/unionmove.L.ico-6.shape.gii')

''' MAIN get frontal lobe affined mask for every subject'''
# subjects = open('../Data_files/Subjects_IDs_HCP_hierarch_0', "r").read().splitlines()
# for sub in subjects:
#     get_lobe(lobe = 'frontal',id = sub)






def get_lobe_1(lobe = None):
    """
    For global registration where your lobe masks don't need to be deformed
    :param lobe:
    :return:
    """
    # regions = nib.load('/home/yg21/YourongGuo/normativemodel/medialwall/group.aparc.HCP.no_residual.L.ico-6.label.gii')
    regions = nib.load('/home/yg21/YourongGuo/normativemodel/medialwall/group.aparc.HCP.no_residual.L.ico-6.label.gii')
    region_dict = regions.labeltable.get_labels_as_dict()  # key into the LabelTable’s labels
    # region_dict_new = dict(zip(region_dict.values(), region_dict.keys()))

    'lobe'
    frontal_lobe = [27,26,2,3,24,17,18,19,20,23,12,32,14,28]
    parietal_lobe = [22,31,29,25,10,8]
    temporal_lobe = [34,30,1,15,7,33,16,6]+[11,5,21,13,9] # temporal + occipital + (8__inferiorparietal) +35 insula

    regions_mask = regions.darrays[0].data
    ROI_id = np.asarray([])
    if lobe == 'frontal':
        lobeid = frontal_lobe
    elif lobe == 'parietal':
        lobeid = parietal_lobe
    elif lobe == 'temporal':
        lobeid = temporal_lobe
    for item in lobeid:
        ROI_id = np.append(ROI_id, np.where(regions_mask==item))

    '''turn on when making mask'''
    # regions_mask = np.zeros((regions_mask.shape))
    # regions_mask[ROI_id.astype('int32')] = 1

    return ROI_id.astype('int32')