### [Regenerative Morphing](https://grail.cs.washington.edu/projects/regenmorph/)

  - A patch-based morphing method  
  - Create a morphed in-between image of two input images
  - Use [bidirectional similarity](https://breakdance.github.io/breakdance/) (BDS) to maximize objective function

### Directory Info
* `environment.yml` : set up environment of Python and packages
* `images/` : contain folders of input/output/reference images
* `regenerative_morph_slow.py` : create a morphed image of two inputs, slow version
* `regenerative_morph.py`: create a morphed image of two inputs, standard version

### How to Run
Go to the folder and activate the environment.
```sh
$ cd /your_computefest_folder/2020-ComputeFest/notebook_to_cloud/PythonPerformance/regenerative_morph
$ env create -f environment.yml
$ conda activate regenerative_morph_env
```

`conda activate` and `conda deactivate` only work on conda 4.6 and later versions. For conda versions prior to 4.6, run:
* Windows: `activate` or `deactivate`
* Linux and macOS: `source activate` or `source deactivate`

Run the script to generative a morphed image.
```sh
$ python regenerative_morph.py
```
The generated image will be saved at `../regenerative_morph/images/outputs`.

### Note
* To add new input images, simply add them into the `../regenerative_morph/images/inputs` folder.
* This implementation of regenerative morphing only outputs one morphed result.
* The input images need to have a significant overlapping, otherwise the morphed results will have white area.