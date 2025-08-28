# GRS RECAST3D Prpoject

This project contains two folders: recastgui (python) and BeamSimulator (Matlab). The recastgui folder contains a gui for running RECAST3D and measuring the reconstruction quality. The BeamSimulator folder contains code for generating images and volumes with simulated beam damage. 


# 1.  RECAST3D Gui
# Installation
This code works with Linux Ubuntu or Fedora with Nvidia and CudaToolKit >12.4. To check your environment is correctly setup run the command. The output should show the nvidia driver and CUDA versions.

```bash
nvidia-smi
```

To install the code first install RECAST3D as instructed in the [documentation](https://cicwi.github.io/RECAST3D/installation_instructions/). The most convenient method is to conda install into your environment. 

```bash
conda install -c cicwi -c astra-toolbox/label/dev recast3d tomopackets slicerecon
```

From there download the source code and in the recastgui folder run the following
```bash
pip install .
```

# Usage
Github pages for usage instructions is currently under maintenance. 
The base instructions is to run the following command, which will open a tkinter gui. From there set the available setting to use center of mass alignment (COM), GRS scanning regime and select the folder your images are being saved into before starting the program. Please note, current supported file types are emi/ser and tiff.

```bash
recastgui
```

# 2.  Beam Simulator

## Setup
 
Add the folders in the BeamSimulator path into your working Matlab working directory. Install a forward and back projection operator into your path along side it. The toolset for forward and backprojections is the [ASTRA Toolbox](https://astra-toolbox.com/downloads/index.html) for MATLAB.

## Usage 

A tutorial can be found in BeamSimulator/tutorial.m

# License

This code is licensed under GNU general public license version 3.0.

# Reference
Reference the following article when using this repository

```bibtex
@article{Craig2023,
author = {Craig, Timothy M and Kadu, Ajinkya A and Batenburg, Kees Joost and Bals, Sara},
doi = {10.1039/D2NR07198C},
journal = {Nanoscale},
number = {11},
pages = {5391--5402},
publisher = {The Royal Society of Chemistry},
title = {{Real-time tilt undersampling optimization during electron tomography of beam sensitive samples using golden ratio scanning and RECAST3D}},
url = {http://dx.doi.org/10.1039/D2NR07198C},
volume = {15},
year = {2023}
}
```