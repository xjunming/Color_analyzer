# Color_analyzer
A simple color analysis tool for pitures.

When we do image processing, we often need to analyze the color distribution of the image. This is a statistic-based image color tool that lets you quickly understand the HSV distribution of your images.

## how to use
I wrote a demo here. see `demo.ipynb`

```
from Color_analyzer import Color_analyzer  #get the class
myanalyzer = Color_analyzer()   #Initialization data
```
```
feature_extractor(pic_dir, pic_format='tif', zoom_in_size=4 , save_npy=False)
# Arguments
    x: Numpy 3D array of probability scores, (N, AUGMENTATIONS_PER_IMAGE, NUM_CLASSES)
    mode: type of averaging, can be "arithmetic" or "geometric"
# Returns
    Mean probabilities 2D array (N, NUM_CLASSES)
```
