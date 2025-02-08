import numpy as np
import pandas as pd
import nibabel as nib
from get_clusters_with_thre import get_clusters_with_thre

def get_lobe(lobe = None,id = None, data_path='/home/yg21/YourongGuo/normativemodel/HCP_labels', data_suffix = '.L.aparc.native.label.gii',outputmask = False, save_path = None,save_suffix = None):
    'lobe from parcellation'
    frontal_lobe = [27,26,2,3,24,17,18,19,20,23,12,32,14,28]
    parietal_lobe = [22,31,29,25,10,8]
    temporal_lobe = [34,30,1,15,7,33,16,6]+[11,5,21,13,9] # temporal + occipital + (8__inferiorparietal)

    regions = nib.load(data_path+'/'+id + data_suffix)

    regions_mask = regions.darrays[0].data

    ROI_id = np.asarray([])

    if lobe == 'frontal':
        lobeid = frontal_lobe
    elif lobe =='parietal':
        lobeid = parietal_lobe
    elif lobe =='temporal':
        lobeid = temporal_lobe

    for item in lobeid:
        ROI_id = np.append(ROI_id, np.where(regions_mask == item))

    ROI_id = ROI_id.astype('int32')
    regions_mask = np.zeros((regions_mask.shape))
    regions_mask[ROI_id.astype('int32')] = 1

    if outputmask == True:
        regions.darrays[0].data = regions_mask
        nib.save(regions, save_path+'/'+id+save_suffix)

    return




def leaf_in_cluster(merge_path = None):
    """
    :param node: string id e.g. 'NODE001' '110234'
    :param merge_path: path of the merge file
    :return: leaf_id the string np array of leaves of give node
    """

    # get the merging pass of the
    merge = pd.read_pickle(merge_path)
    leaf_id = {}
    for i in range(len(merge)):
        nodeid = merge.loc[[i]]
        if 'NODE' in nodeid['subID1'].values[0]: # if branch 1 is a node
            leaf_id[nodeid['mergeID'].values[0]] = leaf_id[nodeid['subID1'].values[0]] # add previous saved branch dict to it
        else:
            leaf_id[nodeid['mergeID'].values[0]] = np.asarray(nodeid['subID1']) # add it self to it
        if 'NODE' in nodeid['subID2'].values[0]:
            leaf_id[nodeid['mergeID'].values[0]] = np.append(leaf_id[nodeid['mergeID'].values[0]],leaf_id[nodeid['subID2'].values[0]])
        else:
            leaf_id[nodeid['mergeID'].values[0]] = np.append(leaf_id[nodeid['mergeID'].values[0]], np.asarray(nodeid['subID2']))
    return leaf_id


def hierarch_path_dict(inter_templates,merge_hierarchy_path):
    """
    give the initial_templates, give merging path (.pkl)
    :param inter_templates:
    :return: cluster_hie_dict, output initial_template: hierarchical path dictionary
    """
    # load in merge_path
    merge_hierarchy = pd.read_pickle(merge_hierarchy_path)

    # define a cluster -hierarchy path dict
    cluster_hie_dict = {}

    # create a key for each template
    for templates in inter_templates:
        cluster_hie_dict[templates]=np.asarray([])

    for j in range(0, len(merge_hierarchy)):

        # get merge process
        i = merge_hierarchy.iloc[[j]].index[0]
        # print('merge ID ' + str(i))

        to_merge = merge_hierarchy.loc[[i]]

        A = str(to_merge['subID1'][i])
        B = str(to_merge['subID2'][i])
        combined = str(to_merge['mergeID'][i])

        if A in cluster_hie_dict:
            cluster_hie_dict[A] = np.append(cluster_hie_dict[A], combined)
        if B in cluster_hie_dict:
            cluster_hie_dict[B] = np.append(cluster_hie_dict[B], combined)

    for j in range(0, len(merge_hierarchy)):
        # get merge process
        i = merge_hierarchy.iloc[[j]].index[0]
        # print('merge ID ' + str(i))

        to_merge = merge_hierarchy.loc[[i]]

        A = str(to_merge['subID1'][i])
        B = str(to_merge['subID2'][i])
        combined = str(to_merge['mergeID'][i])

        for templates in inter_templates:

            if A in cluster_hie_dict[templates]:
                cluster_hie_dict[templates] = np.append(cluster_hie_dict[templates], combined)

            if B in cluster_hie_dict[templates]:
                cluster_hie_dict[templates] = np.append(cluster_hie_dict[templates], combined)

    return cluster_hie_dict


def get_lobe_clusters(lobe, exclude=True):
    '''

    :param lobe: lobe
    :param exclude: if true, then exclude the clusters sizes < 5
    :return: list of clusters in this lobe
    '''
    # lobe='frontal'  # this analysis is only done on the temporal lobe, with temporal lobe without the insula mask
    simi_method = 'corrdice'
    subject_list = '../Data_files/Subjects_IDs_HCP_all_LR'

    # subjects = open(subject_list).read().splitlines()


    # check 30 template threshold
    # exclude very small clusters
    if lobe == 'temporal':
        exclude_cluster = np.asarray(['NODE2066', 'NODE2107', 'NODE2119', 'NODE2137', 'NODE2144'])
        cluster_thre = 0.365
    elif lobe == 'parietal':
        exclude_cluster = np.asarray(['NODE1856'])
        cluster_thre = 0.477
    elif lobe == 'frontal':
        exclude_cluster = np.asarray(['NODE1910', 'NODE2115','NODE2147'])
        cluster_thre = 0.38


    '''
    get cluster frequency
    '''
    merge_path = '../main5_levelstep/dendrogram_'+lobe+'/mergeprocess_'+lobe+'_'+simi_method+'_affine_mask_complete_0.pkl'
    ### TODO:frontal corrmse 0.28 corrdice 0.38  ### parietal corrdice 0.477 corrmse 0.371 ### temporal corrdice 0.365 corrmse 0.247
    temps_30 = get_clusters_with_thre(merge_path,subject_list =subject_list,cluster_thre=cluster_thre,size=True,rt_temp=True )

    if exclude:
        temps_30 = np.setdiff1d(temps_30, exclude_cluster)

    return temps_30



def repeatable_command_generate(command_name,command_flags,subjects,subject_suffix,output):

    command='wb_command '+command_name

    output = output

    rep_flag = ''

    for lf in subjects:
            rep_flag = rep_flag +' '+ command_flags +' '+lf+subject_suffix

    command_text = command+' '+output+rep_flag+'\n'
    return command_text