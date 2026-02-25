# Time-Dependent Tomography
![OS](https://img.shields.io/badge/os-Windows%20|%20Linux-lightgray)
![Code](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-yellow)
![License](https://img.shields.io/badge/license-GPL3.0-blue)
![Version](https://img.shields.io/badge/version-v0.0.1-blue)
![Testing](https://img.shields.io/badge/test-Experimental-orange)
![build](https://img.shields.io/badge/tested%20build-Windows%2011%20|%20Ubuntu%2024.04-orange)

# Description

The Time-Dependent Tomography (TD-Tomo) repository is a collection of multiple submodules used for addressing different tasks required for the acquisiton of tiltseries during scanning transmission electron tomography (STEM) that utilize novel acquisiton schemes such as golden ratio scanning or binary decomposition. Each submodule is designed to work interoperable with each other or independently and can be run in a Juypter Notebook. Currently the package contains the following submodules:

1. **TomoBase:** A base library for common tomography tasks such as alignment, reconstruction and post processing which has a registration system for GPU acceleration and library interoperability
2. **TomoAcquire:** A library for connecting to the microscope and acquiring tomography data.
3. **TomoNDT:** A library for GPU accelerated processing of volume-time data with support for BLOSC compressed data storage.
4. **TDTomoNapari** A napari plugin that register the installed submodules and allows their use in a Napari gui. 
5. **TomoLive** A tkinter project for real-time analysis of electron tomography data 

## Installation/Usage

All submodules can be installed independently and instructions to do so are available through each of the submodule. Instructions for a full install of all libraries and a full read the docs will be provided here at a later date.

