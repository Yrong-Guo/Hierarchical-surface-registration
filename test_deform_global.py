#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chang
"""
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




def pairwise_reg_similarity(level=None, move_root=None, move_root_rev=None, target_root=None, target_root_rev=None,test_mode = False):
    """ hyper-parameters """
    ver_dic = {0: 12, 1: 42, 2: 162, 3: 642, 4: 2562, 5: 10242, 6: 40962}

    batch_size = 1
    in_channels = 2
    out_channels = 0

    num_feat = [32, 64, 128, 256, 512]

    data_ico = 6  # input data ico

    labels_ico_coar = 6  # 5  # labels ico

    control_ico_coar = 2  # ico 2

    num_neigh_coar = 80  # 600 #int(ver_dic[labels_ico_coar]/2)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 'cpu'#

    ################################################################

    model_coarse = DDR_Coarse(in_ch=in_channels, out_ch=out_channels, num_features=num_feat,
                              device=device, num_neigh=num_neigh_coar, data_ico=data_ico,
                              labels_ico=labels_ico_coar, control_ico=control_ico_coar)
    model_coarse.to(device)


    test_dataset = MRIImages(move_root, target_root)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size,
                                 shuffle=False, pin_memory=True)

    edge_i = torch.LongTensor(np.load('../DDR_files/edge_index_6.npy')).to(device)

    def test_val_coarse(dataloader, edge_i, control_ico, data_ico):

        test_losses_mse_1 = torch.zeros((len(dataloader), 1))
        test_losses_gcc_1 = torch.zeros((len(dataloader), 1))
        test_DICE_1 = torch.zeros((len(dataloader), 1))


        for batch_idx, (moving_ims, target_ims, moving_id, target_id) in enumerate(dataloader):
            moving_ims, target_ims = (moving_ims.squeeze(0)).to(device), (target_ims.squeeze(0)).to(device)
            with torch.no_grad():
                moving_id = moving_id[0]
                target_id = target_id[0]

                '''average folds prediction'''
                # load model for fold1
                model_coarse.load_state_dict(torch.load(
                    '/home/yg21/YourongGuo/normativemodel/hierarc_hcp/copy/fold1_1/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                # make prediction - warp the feature and mask
                def_control_ico_test_1 = model_coarse(moving_ims, target_ims, edge_i)

                # load model for fold2
                model_coarse.load_state_dict(torch.load(
                    '/home/yg21/YourongGuo/normativemodel/code2_fold/DDR_Coarse/trained_models/new/fold2/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                def_control_ico_test_2 = model_coarse(moving_ims, target_ims, edge_i)

                # load model for fold3
                model_coarse.load_state_dict(torch.load(
                    '/home/yg21/YourongGuo/normativemodel/code2_fold/DDR_Coarse/trained_models/new/fold3/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                def_control_ico_test_3 = model_coarse(moving_ims, target_ims, edge_i)

                # load model for fold4
                model_coarse.load_state_dict(torch.load(
                    '/home/yg21/YourongGuo/normativemodel/code2_fold/DDR_Coarse/trained_models/new/fold4/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                def_control_ico_test_4 = model_coarse(moving_ims, target_ims, edge_i)

                # load model for fold5
                model_coarse.load_state_dict(torch.load(
                    '/home/yg21/YourongGuo/normativemodel/code2_fold/DDR_Coarse/trained_models/new/fold5/best_models_coarse/best_val_model_coarse.pkl'))
                model_coarse.eval()
                def_control_ico_test_5 = model_coarse(moving_ims, target_ims, edge_i)

                # average the control grid and upsample
                def_control_ico_test = (def_control_ico_test_1 + def_control_ico_test_2 + def_control_ico_test_3 + def_control_ico_test_4 + def_control_ico_test_5) / 5

                # upsampling
                lobe_mask_moving = None
                predictions1_test, def_control_ico_test, warped_mask = upsample_control(moving_ims, lobe_mask_moving,
                                                                                        control_ico, data_ico,
                                                                                        def_control_ico_test, device)


                if test_mode:
                    img_header = nib.load('/home/yg21/YourongGuo/normativemodel/code3_tohcptemp/DDR_Coarse_tohcptemp/DDR_Coarse/Deformation_results/100206.DDR.L.sulc.affine.ico6.shape.gii')
                    img_header.darrays[0].data = predictions1_test.squeeze().to('cpu').numpy()
                    nib.save(img_header, '/home/yg21/YourongGuo/normativemodel/medialwall/'+moving_id+'.DDR.'+target_id+'.L.ico-6.shape.gii')


                '''-----------------------------------------------------------------similarity scores for global hemisphere-----------------------------------------------------------------'''

                '''frontal'''
                test_losses_gcc_1[batch_idx, :], test_losses_mse_1[batch_idx, :] = LossFuns(predictions1_test / 10, target_ims / 10)  # .to('cpu')   # /10 because the normalisation was done by normalising everyting in [-13,16]..... still need to refine this
                test_DICE_1[batch_idx, :] = DiceFun(predictions1_test, target_ims)

                print('Done -- '+str(batch_idx))

        # return registered_feats, test_losses_mse, test_losses_gcc, deff_field_test
        # return test_losses_mse, test_losses_gcc, deff_field_test

        # return test_losses_mse, test_losses_gcc, test_DICE, test_MI
        return test_losses_mse_1, test_losses_gcc_1, test_DICE_1




    '''testing -load best model'''
    test_losses_mse, test_losses_gcc, test_DICE = test_val_coarse(test_dataloader, edge_i, control_ico_coar,labels_ico_coar)


    '''calculate similarity'''
    # test_gcc = 0.5*main_losses_gcc +0.5*main_losses_mse

    # test_gcc = main_losses_gcc
    # test_mse = main_losses_mse
    # test_DICE = main_DICE
    # test_MI= main_MI
    # return test_gcc, test_mse, test_DICE, test_MI
    return test_losses_mse, test_losses_gcc, test_DICE


