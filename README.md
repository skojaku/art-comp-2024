# BU Art Competition

## Outcome

![figs/geo-science.png](figs/all-sciences-v2.png)

**Charting Scientific Foraging**: Just as slime mold explores and exploits foods, so too do scientists forage for scientific discoveries. The colors represent research topics. The elevation represents the number of scientists publishing in that area. Scientists are mapped by a language model, BERT, trained on 134M scientific papers and visualized with HeliosWeb.

## About the competition

- [Web page](https://www.binghamton.edu/research/division-offices/research-advancement/art-of-science/index.html)
- Deadline Feb 23
- Two categories, **The world around us** and **Visualizing the Unseen**.

## Shared folder
- Raw data: `/data/art`
- Shared folder: https://drive.google.com/drive/folders/1XytENk21iqdhgbwtBCZTm3OPsdRuQn9f?usp=sharing

# How to make the terrain plot

1. Create .xnet file using xnet library (see example in [workflow/example-generate-xnet.py](workflow/example-generate-xnet.py))
2. Open [HeliosWeb](http://heliosweb.io/docs/example/?advanced&dark&density&size=0.0&layout=0&use2d&densityProperty=Mass) and drag & drop the .xnet file.
3. Set the "Greys" as the colormap. And zoom in as much as possible while displaying the whole object
4. Right click & save the figure
5. Select the node label to the class type you want to color by. You will see a legend on the left.
6. Set the colormap to tab18.
7. Click one class in the legend. Modify the intensity or kernel width appropriately. Then, save the figure. Repeat for all classes except "Others".
8. Put all figures into one folder. Open `plot.py` and edit the path to a folder to the folder with the images.
9. Run `plot.py`.

# Data
[Lin, Z., Yin, Y., Liu, L. et al. SciSciNet: A large-scale open data lake for the science of science research. Sci Data 10, 315 (2023). https://doi.org/10.1038/s41597-023-02198-9](https://www.nature.com/articles/s41597-023-02198-9)
 

