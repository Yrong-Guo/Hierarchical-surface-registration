#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chang
"""
import copy

import nibabel
import nibabel as nb
from nibabel.filebasedimages import FileBasedHeader
from nibabel.gifti import GiftiImage, GiftiDataArray, GiftiCoordSystem, GiftiMetaData,  GiftiNVPairs
import os

# os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import numpy as np
from DDR_Dataloader_2 import MRIImages
import torch
from torch.utils.data import DataLoader
# import torch.nn as nn
from get_save_deffor_sphere import get_defformed_sphere
import nibabel as nib
from DDR_Coarse_Models import DDR_Coarse
from sklearn.feature_selection import mutual_info_regression
from DDR_Funs import LossFuns, loss_smooth,DiceFun
from utils.get_lobe_2 import get_lobe
from DDR_upsample import upsample_control
from find_hierarch import cluster_CC
from load_similarity import find_pairs_to_merge
import pickle
from itertools import islice
from line_profiler import LineProfiler


def pairwise_reg_similarity(level=None, move_root=None, move_root_rev=None, target_root=None, target_root_rev=None,test_mode = False,continue_run=False,continue_idx=None, profile=False):

    if profile:
        return pairwise_reg_similarity_profiled(level, move_root, move_root_rev, target_root, target_root_rev,
                                                test_mode, continue_run, continue_idx)
    else:
        return pairwise_reg_similarity_original(level, move_root, move_root_rev, target_root, target_root_rev,
                                                test_mode, continue_run, continue_idx)


def pairwise_reg_similarity_profiled(level=None, move_root=None, move_root_rev=None, target_root=None, target_root_rev=None, test_mode=False, continue_run=False, continue_idx=None):
    profiler = LineProfiler()

    # Add the functions to be profiled
    profiler.add_function(get_lobe)
    profiler.add_function(LossFuns)
    profiler.add_function(mutual_info_regression)
    profiler.add_function(DiceFun)
    profiler.add_function(upsample_control)
    profiler.add_function(DDR_Coarse)

    # Wrap the entire function in the profiler
    pairwise_reg_similarity_original_wrapped = profiler(pairwise_reg_similarity_original)

    # Call the wrapped function
    result = pairwise_reg_similarity_original_wrapped(level, move_root, move_root_rev, target_root, target_root_rev, test_mode, continue_run, continue_idx)

    # Print the profiling statistics
    profiler.print_stats()

    return result

def pairwise_reg_similarity_original(level=None, move_root=None, move_root_rev=None, target_root=None, target_root_rev=None, test_mode=False, continue_run=False, continue_idx=None):
    # ... (rest of your original function code)

    """ hyper-parameters """
    # ver_dic = {0: 12, 1: 42, 2: 162, 3: 642, 4: 2562, 5: 10242, 6: 40962}

    batch_size = 1
    in_channels = 2
    out_channels = 0

    num_feat = [32, 64, 128, 256, 512]

    data_ico = 6  # input data ico

    labels_ico_coar = 6  # 5  # labels ico

    control_ico_coar = 2  # ico 2

    num_neigh_coar = 80  # 600 #int(ver_dic[labels_ico_coar]/2)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 'cpu'#
    # print("The device is '{}' ".format(device))
    ################################################################


    # Define the base model
    model_coarse = DDR_Coarse(in_ch=in_channels, out_ch=out_channels, num_features=num_feat,
                            device=device, num_neigh=num_neigh_coar, data_ico=data_ico,
                            labels_ico=labels_ico_coar, control_ico=control_ico_coar).to(device)

    # Load model weights for each fold
    fold_paths = [
        '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/copy/fold1_1/best_models_coarse/best_val_model_coarse.pkl',
        '/home/yg21/YourongGuo/normativemodel/code2_fold/DDR_Coarse/trained_models/new/fold2/best_models_coarse/best_val_model_coarse.pkl',
        '/home/yg21/YourongGuo/normativemodel/code2_fold/DDR_Coarse/trained_models/new/fold3/best_models_coarse/best_val_model_coarse.pkl',
        '/home/yg21/YourongGuo/normativemodel/code2_fold/DDR_Coarse/trained_models/new/fold4/best_models_coarse/best_val_model_coarse.pkl',
        '/home/yg21/YourongGuo/normativemodel/code2_fold/DDR_Coarse/trained_models/new/fold5/best_models_coarse/best_val_model_coarse.pkl'
    ]

    models = []
    for fold_path in fold_paths:
        model = copy.deepcopy(model_coarse)
        model.load_state_dict(torch.load(fold_path))
        model.eval()
        models.append(model)



    test_dataset = MRIImages(move_root, target_root)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size,
                                 shuffle=False, pin_memory=True)
    # print('Number of Test Images = ', len(test_dataloader))

    edge_i = torch.LongTensor(np.load('../DDR_files/edge_index_6.npy')).to(device)




    def test_val_coarse(dataloader, edge_i, control_ico, data_ico,continue_run=False,continue_idx=0):
        test_losses_mse_1 = torch.zeros((len(dataloader), 1))
        test_losses_gcc_1 = torch.zeros((len(dataloader), 1))
        test_MI_1 = np.zeros((len(dataloader), 1))
        test_DICE_1 = torch.zeros((len(dataloader), 1))

        test_losses_mse_2 = torch.zeros((len(dataloader), 1))
        test_losses_gcc_2 = torch.zeros((len(dataloader), 1))
        test_MI_2 = np.zeros((len(dataloader), 1))
        test_DICE_2 = torch.zeros((len(dataloader), 1))

        test_losses_mse_3 = torch.zeros((len(dataloader), 1))
        test_losses_gcc_3 = torch.zeros((len(dataloader), 1))
        test_MI_3 = np.zeros((len(dataloader), 1))
        test_DICE_3 = torch.zeros((len(dataloader), 1))


        with torch.no_grad():
            for batch_idx, (moving_ims, target_ims, moving_id, target_id) in enumerate(islice(dataloader, continue_idx, None), start=continue_idx):
                moving_ims, target_ims = (moving_ims.squeeze(0)).to(device), (target_ims.squeeze(0)).to(device)

                moving_id = moving_id[0]
                target_id = target_id[0]

                # TODO:change aparc!!! if trying to fit in the templates established, will need only the moving image lobar mask
                # lobe_roi_moving, lobe_mask_moving = get_lobe(id = moving_id,aparc_dir='/home/yg21/YourongGuo/normativemodel/code/affined_aparc',aparc_suffix='.aparc.affine.ico6.label.gii')
                # lobe_roi_target, _ = get_lobe(id = target_id,aparc_dir='/home/yg21/YourongGuo/normativemodel/code/affined_aparc',aparc_suffix='.aparc.affine.ico6.label.gii')

                lobe_roi_moving, lobe_mask_moving = get_lobe(id = moving_id,aparc_dir='/home/yg21/YourongGuo/normativemodel/HCP_1200/UKB_sulc/affined_UKB',aparc_suffix='.aparc.affine.ico6.label.gii')
                lobe_roi_target = copy.deepcopy(lobe_roi_moving)   # when match UKB to template, use only the UKB mask - this is to calculate similarity within only the UKB defined frontal/parietal/temporal lobes


                # need to move moving mask to GPU device
                for key, value in lobe_mask_moving.items():
                    lobe_mask_moving[key] = torch.from_numpy(lobe_mask_moving[key]).to(device)
                # lobe_mask_moving = torch.from_numpy(lobe_mask_moving).to(device)

                '''average folds prediction'''
                # load model for fold1
                # make prediction - warp the feature and mask
                def_control_ico_test_1 = models[0](moving_ims, target_ims, edge_i)

                # load model for fold2
                def_control_ico_test_2 = models[1](moving_ims, target_ims, edge_i)

                # load model for fold3
                def_control_ico_test_3 = models[2](moving_ims, target_ims, edge_i)

                # load model for fold4
                def_control_ico_test_4 = models[3](moving_ims, target_ims, edge_i)

                # load model for fold5
                def_control_ico_test_5 = models[4](moving_ims, target_ims, edge_i)

                # average the control grid and upsample
                def_control_ico_test = (def_control_ico_test_1 + def_control_ico_test_2 + def_control_ico_test_3 + def_control_ico_test_4 + def_control_ico_test_5) / 5

                # upsampling
                predictions1_test, def_control_ico_test, warped_mask = upsample_control(moving_ims, lobe_mask_moving,
                                                                                        control_ico, data_ico,
                                                                                        def_control_ico_test, device)


                # predictions1_test, def_control_ico_test, _, warped_mask = model_coarse(moving_ims, target_ims, edge_i,lobe_mask_moving)  # first model

                if test_mode:
                    img_header = nib.load('/home/yg21/YourongGuo/normativemodel/code3_tohcptemp/DDR_Coarse_tohcptemp/DDR_Coarse/Deformation_results/100206.DDR.L.sulc.affine.ico6.shape.gii')
                    img_header.darrays[0].data = predictions1_test.squeeze().to('cpu').numpy()
                    nib.save(img_header, '/home/yg21/YourongGuo/normativemodel/medialwall/'+moving_id+'.DDR.'+target_id[-8:]+'.L.ico-6.shape.gii')


                '''-----------------------------------------------------------------similarity scores for different lobes-----------------------------------------------------------------'''
                warped_mask_moving = {}
                for key, value in warped_mask.items():
                    warped_mask_moving[key] = warped_mask[key].cpu()
                # warped_mask_moving = warped_mask.cpu()

                '''frontal'''
                warped_mask_moving_frontal = warped_mask_moving['frontal'].numpy()
                lobe_roi = np.union1d(np.where(warped_mask_moving_frontal == 1)[0],lobe_roi_target['frontal']) # union of the two moving lobe mask and target lobe mask
                predictions1_test_lobe = predictions1_test[lobe_roi]  # take the lobe from the deformed moving image
                target_ims_lobe = target_ims[lobe_roi]
                # scores
                test_losses_gcc_1[batch_idx, :], test_losses_mse_1[batch_idx, :] = LossFuns(predictions1_test_lobe/10,target_ims_lobe/10)  # .to('cpu')   # /10 because the normalisation was done by normalising everyting in [-13,16]..... still need to refine this
                test_MI_1[batch_idx, :] = mutual_info_regression((predictions1_test_lobe/10).to('cpu').numpy().reshape(-1,1),(target_ims_lobe/10).to('cpu').numpy().reshape(-1))
                test_DICE_1[batch_idx, :] = DiceFun(predictions1_test_lobe,target_ims_lobe)


                '''parietal'''
                warped_mask_moving_frontal = warped_mask_moving['parietal'].numpy()
                lobe_roi = np.union1d(np.where(warped_mask_moving_frontal == 1)[0],lobe_roi_target['parietal']) # union of the two moving lobe mask and target lobe mask
                predictions1_test_lobe = predictions1_test[lobe_roi]  # take the lobe from the deformed moving image
                target_ims_lobe = target_ims[lobe_roi]
                # scores
                test_losses_gcc_2[batch_idx, :], test_losses_mse_2[batch_idx, :] = LossFuns(predictions1_test_lobe/10,target_ims_lobe/10)  # .to('cpu')   # /10 because the normalisation was done by normalising everyting in [-13,16]..... still need to refine this
                test_MI_2[batch_idx, :] = mutual_info_regression((predictions1_test_lobe/10).to('cpu').numpy().reshape(-1,1),(target_ims_lobe/10).to('cpu').numpy().reshape(-1))
                test_DICE_2[batch_idx, :] = DiceFun(predictions1_test_lobe,target_ims_lobe)


                '''temporal'''
                warped_mask_moving_frontal = warped_mask_moving['temporal'].numpy()
                lobe_roi = np.union1d(np.where(warped_mask_moving_frontal == 1)[0],lobe_roi_target['temporal']) # union of the two moving lobe mask and target lobe mask
                predictions1_test_lobe = predictions1_test[lobe_roi]  # take the lobe from the deformed moving image
                target_ims_lobe = target_ims[lobe_roi]
                # scores
                test_losses_gcc_3[batch_idx, :], test_losses_mse_3[batch_idx, :] = LossFuns(predictions1_test_lobe/10,target_ims_lobe/10)  # .to('cpu')   # /10 because the normalisation was done by normalising everyting in [-13,16]..... still need to refine this
                test_MI_3[batch_idx, :] = mutual_info_regression((predictions1_test_lobe/10).to('cpu').numpy().reshape(-1,1),(target_ims_lobe/10).to('cpu').numpy().reshape(-1))
                test_DICE_3[batch_idx, :] = DiceFun(predictions1_test_lobe,target_ims_lobe)


                print('Done -- '+str(batch_idx))

                # TODO:save tuples
                tuple_1 = (test_losses_mse_1, test_losses_gcc_1, test_DICE_1, test_MI_1)
                tuple_2 = (test_losses_mse_2, test_losses_gcc_2, test_DICE_2, test_MI_2)
                tuple_3 = (test_losses_mse_3, test_losses_gcc_3, test_DICE_3, test_MI_3)

        return tuple_1,tuple_2,tuple_3




    '''testing -load best model'''
    if continue_run == True:
        frontal_scores, parietal_scores, temporal_scores = test_val_coarse(test_dataloader, edge_i, control_ico_coar,labels_ico_coar,continue_run=continue_run,continue_idx=continue_idx)
    else:
        frontal_scores, parietal_scores, temporal_scores = test_val_coarse(test_dataloader, edge_i, control_ico_coar,labels_ico_coar)




    '''calculate similarity'''
    # test_gcc = 0.5*main_losses_gcc +0.5*main_losses_mse

    # test_gcc = main_losses_gcc
    # test_mse = main_losses_mse
    # test_DICE = main_DICE
    # test_MI= main_MI
    # return test_gcc, test_mse, test_DICE, test_MI
    return frontal_scores, parietal_scores, temporal_scores


