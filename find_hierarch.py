import numpy as np
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt
import matplotlib

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    '''make cluster label'''
    clusterlabel = np.asarray([])
    for i in model.labels_:
        if str(i) not in clusterlabel:
            clusterlabel = np.append(clusterlabel,str(i))
        else:
            clusterlabel = np.append(clusterlabel,'')


    '''Plot the '+simi_method+'_affine_maskesponding dendrogram'''
    # dendrogram(linkage_matrix, **kwargs,color_threshold=model.distances_[len(model.distances_)-model.n_clusters]+0.001,labels=clusterlabel,leaf_rotation=90) # if cluster is defined
    dendrogram(linkage_matrix, **kwargs,color_threshold=0.371)
    return linkage_matrix

def cluster_CC(similarity_score,simi_method = 'corrmse',level=None,lobe = None):
    '''
    cluster based on the similarity score matrix given
    :param similarity_score: e.g. 'similarity_score_1.npy'
    :return: children distance matrix in level 0
    '''
    '''load similarity matrix'''

    distance = 1- similarity_score # change similarity to distance used in clustering
    '''clustering'''
    n_clusters = similarity_score.shape[0]
    clustering = AgglomerativeClustering(distance_threshold=0.2575, n_clusters=None, affinity='precomputed',linkage='complete',compute_full_tree=True,compute_distances=True).fit(distance)
    # frontal 28 parietal 23 temporal
    '''plot the dendrogram'''
    # fig = plt.figure(figsize=(15,6))
    # matplotlib.rcParams['lines.linewidth'] = 0.7
    # fig.tight_layout()
    # plt.title("Hierarchical Clustering Dendrogram")


    # plot the top three levels of the dendrogram
    children_distance = plot_dendrogram(clustering)
    # plt.show()
    '''save children order'''
    # np.save('dendrogram_'+lobe+'/children_distance_cc_'+lobe+'_'+simi_method+'_affine_mask_complete_'+str(level)+'.npy',children_distance)


    # plt.savefig('dendrogram_'+lobe+'/complete_cc_'+lobe+'_'+simi_method+'_affine_mask.png', dpi=300)
    # np.save('dendrogram/label_'+lobe+'_'+simi_method+'_affine_mask_complete.npy',clustering.labels_)
    return children_distance