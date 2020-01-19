### Directory Info
* `regenerative_morph/` : **Example 2** of the workshop, creates a morphed image based on two input images
* `environment.yml` : set up environment for **Example 1** and **Example 2**
* `plot_function.py` : **Example 1** of the workshop, plots the graph of a function

### Set up the Environment
Go to the folder and activate the environment.
```sh
$ cd /your_computefest_folder/2020-ComputeFest/notebook_to_cloud/PythonPerformance/
$ conda env create -f environment.yml
$ conda activate python_performance_env
```

`conda activate` and `conda deactivate` only work on conda 4.6 and later versions. For conda versions prior to 4.6, run:
* Windows: `activate` or `deactivate`
* Linux and macOS: `source activate` or `source deactivate`

### How to Run
(Under activated `python_performance_env` environment) Go to the folder.
```sh
$ cd /your_computefest_folder/2020-ComputeFest/notebook_to_cloud/PythonPerformance/
```
Run the script to generative a graph of a given function.
```sh
$ python plot_function.py
```