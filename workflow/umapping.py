# %%
from cuml.manifold.umap import UMAP as cuUMAP
import cupy
import pandas as pd
import numpy as np
from scipy import sparse
import sys
from laborflow2vec import vector_cover, gravity_potential


# import igraph
from tqdm.auto import tqdm

# %% Load
if "snakemake" in sys.modules:
    emb_file = snakemake.input["paper_emb_file"]
    author_emb_file = snakemake.input["author_emb_file"]
    author2paper_net_file = snakemake.input["author2paper_net_file"]
    year_author_table_file = snakemake.input["year_author_table_file"]
    author_table_file = snakemake.input["author_table_file"]
    paper_table_file = snakemake.input["paper_table_file"]
    output_file = snakemake.output["output_file"]
else:
    emb_file = "../../data/scisci/embeddings/paper_embedding~60c7926b7a265d89dbd48ef738984888_model~laborflow2vec.npz"
    author2paper_net_file = (
        "../../data/derived/preprocessed/scisci/author_paper_net.npz"
    )
    year_author_table_file = (
        "../../data/derived/preprocessed/scisci/year_author_table.csv"
    )
    paper_table_file = "../../data/derived/preprocessed/scisci/paper_table.csv"
    output_file = "umapping-scisci.npz"

# Load
emb_paper = np.load(emb_file)["emb"]
year_author_table = pd.read_csv(year_author_table_file)
yearauthor2paper = sparse.load_npz(author2paper_net_file)

# %% Projection
import os

os.environ["CUDA_VISIBLE_DEVICES"] = str(1)

X_train = cupy.array(
    emb_paper[np.random.choice(emb_paper.shape[0], size=100000)]
    .copy(order="C")
    .astype("float32")
)


trained_UMAP = cuUMAP(
    metric="cosine",
    n_neighbors=100,
    min_dist=0.1,
    n_components=2,
    # min_dist=0.2,
    n_epochs=10000,
).fit(X_train)


# %% Iterative Mapping
def iterative_mapping(X, model, batch_size=10000):
    n_batch = (X.shape[0] + batch_size - 1) // batch_size
    xylist = []
    for batch_id in range(n_batch):
        start_id = batch_id * batch_size
        end_id = (batch_id + 1) * batch_size
        end_id = np.minimum(end_id, X.shape[0])
        xy = model.transform(
            cupy.array(X[start_id:end_id].copy(order="C").astype("float32"))
        ).get()
        xylist.append(xy)
    return np.vstack(xylist)


xy_paper = iterative_mapping(emb_paper, trained_UMAP)

# %% Computing the mass
import polars as pl

mass = gravity_potential.calc_author_mass(
    pl.from_pandas(year_author_table), yearauthor2paper
)

# %% Centering & Rescaling
center = np.mean(xy_paper, axis=0)
xy_paper -= center

# %% Save
np.savez(output_file, xy_paper=xy_paper, mass=mass)
