# Hierarchical-surface-registration

This repository contains Python scripts and SLURM bash code to perform hierarchical surface registration and template concatenation for brain imaging analysis. The downstream analysis codes are also provided.

![‎Figure_method_overview_increaselobecombine ‎001](https://github.com/user-attachments/assets/79727233-467d-43a3-a897-62d68fc70801)
*Figure 1: Overview of MSM-HT. A, After mirror-flipping all right hemispheres (into rigid alignment with left hemispheres) using Workbench Command, all pairs of sulcal depth maps were co-registered using DDR. B, once sulcal depth maps are coarsely aligned, the overlap of cortical folding patterns, for each pair of hemispheres, are separately assessed for each of the frontal, parieto-occipital, and temporal lobes - using a combination of dice overlap and cross-correlation. C, Hierarchical alignment in steps. (1) Agglomerative hierarchical clustering is applied to each of the resulting similarity matrices, (2) the hierarchy is thresholded at the similarity score that returns thirty clusters for each lobe, (3) MSM is then used to co-register curvature maps of individuals within each cluster to generate a template for each cluster - that summarises the shape of folds within that cluster, (4) Intermediate templates were generated at each node of the dendrogram, by aligning pairs of templates until all images were merged into HT-PA at the top. (5) Finally, all templates are further registered through the hierarchical path to a common space. D, Combining the registration across three lobes. Mappings are combined across lobes by iterating alignment: first to frontal lobe templates, then parietal and finally temporal. This process repeated through 3 resolution levels of the MSM registration.*

## Requirements

### Python libraries
 - `numpy`
 - `nibabel`
 - `scikit-learn` (for clustering and other ML tools)
 - `scipy` (for statistical test, e.g. wilcoxon, ttest_rel)
 - `pandas`
 - `seaborn`
 - `matplotlib`
 - For libraries regarding DDR training, please see requirements of [DDR](https://github.com/mohamedasuliman/DDR)

### External tools
- **Workbench (wb_command)**: [Connectome Workbench](https://www.humanconnectome.org/software/connectome-workbench).
- **[newMSM](https://github.com/rbesenczi/newMSM)**: Software for surface registration - Multimodel Surface Mapping.
- **[SLURM](https://slurm.schedmd.com/overview.html)**: A job scheduler for High-Performance Computing (HPC).

## Workflow

### Step 1: calculating the pairwise similarities

