### [Regenerative Morphing](https://grail.cs.washington.edu/projects/regenmorph/)

  - A patch-based morphing method  
  - Create a morphed in-between image of two input images
  - Use [bidirectional similarity](https://breakdance.github.io/breakdance/) (BDS) to maximize objective function

### Directory Info
* `images/` : contain folders of input/output/reference images
* `regenerative_morph.py`: create a morphed image of two inputs, standard version
* `regenerative_morph_slow.py` : create a morphed image of two inputs, slow version

### How to Run
(Under activated `python_performance_env` environment) Go to the folder.
```sh
$ cd /your_computefest_folder/2020-ComputeFest/notebook_to_cloud/PythonPerformance/regenerative_morph
```

Run the script to generative a morphed image.
```sh
$ python regenerative_morph.py
```
The generated image will be saved at `../regenerative_morph/images/outputs`.

### Note
* To add new input images, simply add them into the `../regenerative_morph/images/inputs` folder.
* This implementation of regenerative morphing only outputs one morphed result.
* The input images need to have a significant overlapping, otherwise the morphed results will have white area.