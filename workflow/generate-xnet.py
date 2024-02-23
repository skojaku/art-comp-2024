# %%
import numpy as np
import pandas as pd


data = np.load("umapping-scisci.npz")
xy = data["xy_paper"]
mass = data["mass"]
# %%

from pathlib import Path
import pickle as pkl

dataMAG2WOSPath = Path("/gpfs/slate-sciencegenome/WOS/MAG2WOS")
# paperTable = pd.read_csv(preprocessedPath / "paper_table.csv", dtype={"PaperID": str})
# PaperID,doi,title,year,date,journal_id,paper_id
with open(
    dataMAG2WOSPath / "paperID2TopCategories_no_multidisciplinary_withNSFFields.pkl",
    "rb",
) as file:
    category = pkl.load(file)
# %%
import polars as pl

df = pl.from_pandas(category)
# %%
paper_table = pl.read_csv("../../data/derived/preprocessed/scisci/paper_table.csv")
# %%
dg = (
    paper_table.with_columns(pl.Series("x", xy[:, 0]))
    .with_columns(pl.Series("y", xy[:, 1]))
    .with_columns(pl.Series("mass", mass))
    .rename({"PaperID": "PaperId"})
)
# %%
xdf = df.join(dg, on="PaperId", how="inner")
data_table = xdf.to_pandas()
# %%
import numpy as np
from xnet import xnetwork
import igraph

g = igraph.Graph()
sampled_data_table = data_table.sample(2000000).copy()
# data_table = plot_data.dropna().sample(1000000).copy()

g.add_vertices(sampled_data_table.shape[0])

g.vs["name"] = (
    sampled_data_table["title"]
    .fillna("")
    .str.encode("ascii", "ignore")
    .str.decode("ascii")
    .values
)
g.vs["weight"] = np.ones(sampled_data_table.shape[0])
g.vs["Mass"] = sampled_data_table["mass"].values

g.vs["Year"] = sampled_data_table["year"].values
g.vs["NSF Field"] = sampled_data_table["NSF Field"].fillna("Other").values
g.vs["subjectCategory"] = sampled_data_table["subjectCategory"].fillna("Other").values
g.vs["simpleSubjectCategory"] = (
    sampled_data_table["simpleSubjectCategory"].fillna("Other").values
)
g.vs["researchArea"] = sampled_data_table["researchArea"].fillna("Other").values
g.vs["Position"] = (sampled_data_table[["x", "y"]].values * 50).tolist()
# g.add_edges(edges)

xnetwork.igraph2xnet(g, "../../data/tmp/all-science.xnet", [], [])

# %%
