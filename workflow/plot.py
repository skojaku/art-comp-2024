# %%
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import glob
import scipy

# Load and display the image
Alist = []
for i in np.sort(glob.glob("../data/science-geo/*.png")):
    print(i)
    img = mpimg.imread(i)
    A = img[:, :, 2]
    A = A.max() - A
    # A = A[::20, ::20]  # Reduce the size by a factor of 4
    A = np.power(A, 1.5)
    Alist.append(A)
# %%
import earthpy.spatial as es
import seaborn as sns
from PIL import ImageColor
from scipy.ndimage import zoom

Abase = Alist[0].copy()

from scipy.ndimage import gaussian_filter

# Smooth Abase using a Gaussian filter


# Upsampling Abase
Abase = zoom(
    Abase[::10, ::10], 10, order=1
)  # Upsample by a factor of 10 using cubic interpolation

Abase = zoom(
    Abase[::2, ::2], 2, order=1
)  # Upsample by a factor of 10 using cubic interpolation
Abase = gaussian_filter(Abase, sigma=3)
Asupp = Alist[1:]
min_threshold = 1e-6

hillshade = es.hillshade(Abase * 3000, azimuth=100, altitude=1)
hillshade_masked = np.ma.masked_where(Abase < min_threshold, hillshade)


fig, ax = plt.subplots()
fig.set_size_inches(7, 7)
# fig.patch.set_facecolor(sns.dark_palette(plt.cm.Blues(1 - 0.03))[0])
fig.patch.set_facecolor("#061323")

from matplotlib.colors import LinearSegmentedColormap

color_X = plt.cm.cividis(0.05)
color_Y = plt.cm.cividis(0.5)
cmap = LinearSegmentedColormap.from_list("custom_cmap", [color_X, color_Y])
# c = plt.imshow(
#    np.ma.masked_where(Abase < min_threshold, Abase),
#    cmap=cmap,
#    alpha=1.0,
# )
ax.imshow(hillshade_masked, cmap=cmap, alpha=0.4)
cmap = [
    "#e6194B",
    # "#3cb44b",
    "#ffe119",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#42d4f4",
    "#f032e6",
    "#bfef45",
    "#fabed4",
    "#469990",
    "#dcbeff",
    "#9A6324",
    "#fffac8",
    "#800000",
    "#aaffc3",
    "#808000",
    "#ffd8b1",
    "#f11f76",
    "#a9a9a9",
    "#ffffff",
    "#000000",
]

import colorsys


def make_color_brighter(hex_color):
    # Convert hex to RGB
    rgb = tuple(int(hex_color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    # Convert RGB to HSL
    hsl = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    # Increase the lightness
    brighter = hsl[1] * 1.2
    if brighter > 0.9:
        brighter = hsl[1]
    brighter_hsl = (hsl[0], brighter, hsl[2])
    # Convert back to RGB
    brighter_rgb = colorsys.hls_to_rgb(
        brighter_hsl[0], brighter_hsl[1], brighter_hsl[2]
    )
    # Convert RGB back to hex
    brighter_hex = "#%02x%02x%02x" % (
        int(brighter_rgb[0] * 255),
        int(brighter_rgb[1] * 255),
        int(brighter_rgb[2] * 255),
    )
    return brighter_hex


# Apply the function to make each color in cmap brighter
original_colors = []
cmap = [make_color_brighter(color) for i, color in enumerate(cmap)]

alpha_max = 0.5
for i in range(len(Asupp)):
    As = Asupp[i].copy()
    As = np.ma.masked_where(Abase < min_threshold, As)
    n = As.shape[0]
    rgb_color = ImageColor.getcolor(cmap[i], "RGB")
    rgb_color = np.array(rgb_color) / 255.0
    A = np.zeros((As.shape[0], As.shape[1], 4))
    A[:, :, :3] = rgb_color
    A[:, :, 3] = As * alpha_max
    c = plt.imshow(
        A,
    )

plt.axis("off")  # Do not show axes to keep it clean
plt.savefig("geo-science.png", bbox_inches="tight", dpi=500)
## %%
# plt.imshow(
#    A,
#    alpha=1.0,
#    vmin=0,
# )
# A
## %%
# Abase.shape
#
## %%
# hillshade = es.hillshade(Abase * 3000, azimuth=100, altitude=1)
#
# hillshade_masked = np.ma.masked_where(Abase < 0.01, hillshade)
#
# fig, ax = plt.subplots()
# fig.set_size_inches(7, 10)
# c = plt.imshow(Abase, cmap="cividis", interpolation="spline36", alpha=1.0)
# ax.imshow(hillshade_masked, cmap="Greys", alpha=0.3)
# plt.axis("off")  # Do not show axes to keep it clean
# plt.savefig("terrain.png", bbox_inches="tight", pad_inches=0, dpi=500)
#
## %%
#

# %%

# %%
