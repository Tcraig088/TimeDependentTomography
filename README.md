# Time-Dependent Tomography
![OS](https://img.shields.io/badge/os-Windows%20|%20Linux-lightgray)
![Code](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-yellow)
![License](https://img.shields.io/badge/license-GPL3.0-blue)
![Version](https://img.shields.io/badge/version-v0.0.1-blue)
![Testing](https://img.shields.io/badge/test-Experimental-orange)
![build](https://img.shields.io/badge/tested%20build-Windows%2011%20|%20Ubuntu%2024.04-orange)

## Table of Contents

 - **Overview**
   - [**Section 1. Description**](#1-description)
   - [**Section 2. Installation**](#2-installation)
   - [**Section 3. Usage**](#2-usage)
## 1. Description

The Time-Dependent Tomography (TD-Tomo) repository is a collection of multiple submodules used for addressing different tasks required for the acquisiton of tiltseries during scanning transmission electron tomography (STEM) that utilize novel acquisiton schemes such as golden ratio scanning or binomial decomposition. Each submodule is designed to work interoperable with each other or independently and can be run in a Juypter Notebook. Currently the package contains the following submodules:

1. [**TomoBase:**](https://google.co.nz) A base library for common tomography tasks such as alignment, reconstruction and post processing.
2. [**TomoAcquire:**](https://google.co.nz) A library for connecting to the microscope and acquiring tomography data.
3. [**TomoNDT:**](https://google.co.nz) A library for GPU accelerated processing of volume-time data with support for BLOSC compressed data storage.
4. [**TDTomoNapari**](https://google.co.nz) A napari plugin that register the installed submodules and allows their use in a Napari gui. 

## 2. Installation

All submodules can be installed independently and instructions to do so are available through there there individual github repositories. However, alternatively all repositories can be installed together in conda. 

There are some dependencies which impact only limited functions. The module can be run without them. However, they may be necessary for extended functionality. The install of these dependecies was made optional as to prevent bloat. 

1. [**PyQt5**](https://google.co.nz) **or** [**PySide2**](https://google.co.nz): Backend for  Graphical User Interface (GUI). Either should work. Testing was performed with PyQt5 (pyqt).
2. [**Qtpy:**](https://google.co.nz) Wrapper for GUI Backends. Without qtpy, GUI functions will be disabled.
3. [**Napari:**](https://google.co.nz) Visualization library for microscopy data. Without Napari, you are restricted to usage in a Juypter Notebook.
4. [**CuPY:**](https://google.co.nz) A library for GPU-accelerated computing with Python. Without CuPY GPU acceleration of some functions will be disabled.
5. [**Pytorch:**](https://google.co.nz) A GPU acceleration library for Machine-Learning. No function within TD-Tomo requires Pytorch where CuPy is installed. However, third-party libraries utilizing Pytorch and Machine Learning may benefit from Pytorch support. 
6. [**HyperSpy:**](https://google.co.nz) Used for read write operations for some data types.

```bash
#installs a minimal verison of the repository not including optional dependencies.
conda install tdtomo cudatoolkit=X.XX -c TCraig088 -c conda-forge

#installs the repository with all dependencies and a PyQt5 backend.
conda install tdtomo['all'] cudatoolkit=X.XX pyqt -c TCraig088 -c conda-forge
```

## 3. Usage
To use the library please read the usage guide for the various submodules. [**TDTomoNapari**](https://google.co.nz) has a good guide on how to run the GUI for a beginner.
