import os
import subprocess
from setuptools import setup, find_packages

def install_submodule(path):
    """Install a submodule in editable mode."""
    conda_env_path = os.path.join(path, 'conda', 'meta.yaml')
    if os.path.exists(conda_env_path):
        subprocess.check_call(['conda', 'env', 'create', '-f', conda_env_path])
    subprocess.check_call(['pip', 'install', '-e', path])

# List of submodules to install
submodules = [
    'submodules/tomobase',
    'submodules/tomoacquire',
    'submodules/tdtomonapari'
]

# Install each submodule
for submodule in submodules:
    install_submodule(submodule)
setup(
    name='tdtomo',  # Replace with your package name
    version='0.0.1',  # Replace with your package version
    packages=find_packages(),
    install_requires=[
    ],
)