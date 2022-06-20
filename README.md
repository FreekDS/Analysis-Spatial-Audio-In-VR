# Analysis-Spatial-Audio-In-VR

> Analysis of data gathered with an experiment in VR related to ambisonic and normal sounds.

This repository contains all files that were used to analyze the data gathered from the spatial audio experiment. A
Python Notebook is used to extract various metrics from the data which helps us to analyze the results obtained from the
experiment.

### Repository contents

- `data/`: this directory contains all data gathered by the spatial audio experiment.
    - `rotation-location/`: contains the data files created by the experiment that contain the positional and rotational
      information of the participants
    - `sfx-info/`: contains the data files created by the experiment that logged when sounds started and stopped playing
      and at which accuracy the players looked at the sound sources at which times.
    - `participants.csv`: contains the participant information gathered from the survey performed after the experiment.
- `files_checker.py`: a simple Python script that verifies whether only one sound at a time was playing. This script is
  used to manually remove mistakes from the log files.
- ``README.md``: this file.
- ```spatial-audio-analysis.ipynb```: the most important file of this repository. The Notebook that is used to analyze
  the data gathered from the experiments. Each analysis step is explained in the notebook using Markdown blocks and the
  code can be executed using the code blocks.
