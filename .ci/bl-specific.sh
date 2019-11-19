#!/bin/bash

cp -Rv data_files ~/.ipython/profile_${TEST_PROFILE}/

conda install -y -c ${CONDA_CHANNEL_NAME} 11-id-chx-collection
