# Hierarchical-surface-registration

This repository contains Python scripts and SLURM bash code to perform hierarchical surface registration and template concatenation for brain imaging analysis. The downstream analysis codes are also provided.

![‎Figure_method_overview_increaselobecombine ‎001](https://github.com/user-attachments/assets/79727233-467d-43a3-a897-62d68fc70801)


## Requirements

### Python libraries
 - numpy
 - nibabel
 - pandas
 - matplotlib
 - see requirements of [DDR](https://github.com/mohamedasuliman/DDR)

### External tools
- **Workbench (wb_command)**: [Connectome Workbench](https://www.humanconnectome.org/software/connectome-workbench).
- **[newMSM](https://github.com/rbesenczi/newMSM)**: Software for surface registration - Multimodel Surface Mapping.
- **[SLURM](https://slurm.schedmd.com/overview.html)**: A job scheduler for High-Performance Computing (HPC).


