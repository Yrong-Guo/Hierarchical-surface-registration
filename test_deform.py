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
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import numpy as np
from DDR_Dataloader_2 import MRIImages
import torch
from torch.utils.data import DataLoader
import nibabel as nib
from DDR_Coarse_Models import DDR_Coarse
from sklearn.feature_selection import mutual_info_regression
from DDR_Funs import LossFuns, loss_smooth,DiceFun
from utils.get_lobe_2 import get_lobe
from DDR_upsample import upsample_control
import pickle
from itertools import islice


def pairwise_reg_similarity( move_root=None, target_root=None, continue_run=False,continue_idx=None):
    """ hyper-parameters """
    ver_dic = {0: 12, 1: 42, 2: 162, 3: 642, 4: 2562, 5: 10242, 6: 40962}

    batch_size = 1
    in_channels = 2
    out_channels = 0

    num_feat = [32, 64, 128, 256, 512]

    data_ico = 6  # input data ico

    labels_ico_coar = 6 # labels ico

    control_ico_coar = 2  # ico 2

    num_neigh_coar = 80  # 600 #int(ver_dic[labels_ico_coar]/2)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 'cpu'#
    # print("The device is '{}' ".format(device))
    ################################################################

    model_coarse = DDR_Coarse(in_ch=in_channels, out_ch=out_channels, num_features=num_feat,
                              device=device, num_neigh=num_neigh_coar, data_ico=data_ico,
                              labels_ico=labels_ico_coar, control_ico=control_ico_coar)
    model_coarse.to(device)


    test_dataset = MRIImages(move_root, target_root)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size,
                                 shuffle=False, pin_memory=True)

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


        for batch_idx, (moving_ims, target_ims, moving_id, target_id) in enumerate(islice(dataloader, continue_idx, None), start=continue_idx):
            moving_ims, target_ims = (moving_ims.squeeze(0)).to(device), (target_ims.squeeze(0)).to(device)
            with torch.no_grad():
                moving_id = moving_id[0]
                target_id = target_id[0]

                # change aparc - if trying to fit in the templates established, will need only the moving image lobar mask
                lobe_roi_moving, lobe_mask_moving = get_lobe(id = moving_id,aparc_dir='/affined_aparc',aparc_suffix='.aparc.affine.ico6.label.gii')
                lobe_roi_target, _ = get_lobe(id = target_id,aparc_dir='/affined_aparc',aparc_suffix='.aparc.affine.ico6.label.gii')



                # need to move moving mask to GPU device
                for key, value in lobe_mask_moving.items():
                    lobe_mask_moving[key] = torch.from_numpy(lobe_mask_moving[key]).to(device)
                # lobe_mask_moving = torch.from_numpy(lobe_mask_moving).to(device)

                '''average folds prediction'''
                # load model for fold1
                model_coarse.load_state_dict(torch.load(
                    '/fold1/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                # make prediction - warp the feature and mask
                def_control_ico_test_1 = model_coarse(moving_ims, target_ims, edge_i)

                # load model for fold2
                model_coarse.load_state_dict(torch.load(
                    '/fold2/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                def_control_ico_test_2 = model_coarse(moving_ims, target_ims, edge_i)

                # load model for fold3
                model_coarse.load_state_dict(torch.load(
                    '/fold3/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                def_control_ico_test_3 = model_coarse(moving_ims, target_ims, edge_i)

                # load model for fold4
                model_coarse.load_state_dict(torch.load(
                    '/fold4/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                def_control_ico_test_4 = model_coarse(moving_ims, target_ims, edge_i)

                # load model for fold5
                model_coarse.load_state_dict(torch.load(
                    '/fold5/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                def_control_ico_test_5 = model_coarse(moving_ims, target_ims, edge_i)

                # average the control grid and upsample
                def_control_ico_test = (def_control_ico_test_1 + def_control_ico_test_2 + def_control_ico_test_3 + def_control_ico_test_4 + def_control_ico_test_5) / 5

                # upsampling
                predictions1_test, def_control_ico_test, warped_mask = upsample_control(moving_ims, lobe_mask_moving,
                                                                                        control_ico, data_ico,
                                                                                        def_control_ico_test, device)


                # predictions1_test, def_control_ico_test, _, warped_mask = model_coarse(moving_ims, target_ims, edge_i,lobe_mask_moving)  # first model



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

                if batch_idx % 10 == 0:
                    tuple_1 = (test_losses_mse_1, test_losses_gcc_1, test_DICE_1, test_MI_1)
                    tuple_2 = (test_losses_mse_2, test_losses_gcc_2, test_DICE_2, test_MI_2)
                    tuple_3 = (test_losses_mse_3, test_losses_gcc_3, test_DICE_3, test_MI_3)

                    # Saving the tuples to a file using pickle
                    with open('main9_process/simi_score_process_1.pkl', 'wb') as file:
                        pickle.dump((tuple_1, tuple_2, tuple_3), file)

        return tuple_1,tuple_2,tuple_3




    '''testing -load best model'''
    if continue_run == True:
        frontal_scores, parietal_scores, temporal_scores = test_val_coarse(test_dataloader, edge_i, control_ico_coar,labels_ico_coar,continue_run=continue_run,continue_idx=continue_idx)
    else:
        frontal_scores, parietal_scores, temporal_scores = test_val_coarse(test_dataloader, edge_i, control_ico_coar,labels_ico_coar)


    # SAVE AGAIN

    # Saving the tuples to a file using pickle
    with open('main9_process/simi_score_final.pkl', 'wb') as file:
        pickle.dump((frontal_scores, parietal_scores, temporal_scores), file)


    return frontal_scores, parietal_scores, temporal_scores


