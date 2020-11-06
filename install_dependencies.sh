#!/bin/bash 

if conda --version ; then
	echo Conda already installed. Skipping conda installation.
else
	echo Installing conda
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
	bash miniconda.sh -b -p $HOME/miniconda
	CONDA_SH=$HOME/miniconda/etc/profile.d/conda.sh
	source $CONDA_SH
fi

if ! conda env list | grep petalo
then
    conda env create -f environment.yml
fi

conda activate petalo
source setup.sh

