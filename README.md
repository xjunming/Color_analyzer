# Color_analyzer
A simple color analysis tool for pitures.

When we do image processing, we often need to analyze the color distribution of the image. This is a statistic-based image color tool that lets you quickly understand the HSV distribution of your images.

## how to use
I wrote a demo here. see `demo.ipynb`

import Color_analyzer and Initialize it
```
from Color_analyzer import Color_analyzer  #get the class
myanalyzer = Color_analyzer()   #Initialization
```

To extract features
```
feature_extractor(pic_dir, pic_format='tif', zoom_in_size=4 , save_npy=False)
'''
:param pic_dir: Folder location where images are stored
:param pic_format: jpg, png, tif, etc.
:param zoom_in_size:  In order to reduce the running time, you need to compress the picture.
:param save_npy: if True, save the feature array as ./output/main_color_array.npy
:return: a array of feature
'''
```

Draw a three-dimensional map
```
myanalyzer.plot_3d(feature)
'''
:param feature: the feature array
:param elev: the angle of the picture
:param azim: the angle of the picture
:return: None
'''
```

plot histogram to description the means and variance of the h,s,v
```
plot_hist(feature, savefig)
'''
:param feature: the feature array
:param savefig: if True, save the histogram pictures.
:return: None
'''
```
