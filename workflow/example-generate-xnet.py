import numpy as np
import pandas as pd
from xnet import xnetwork
import igraph

g = igraph.Graph()
sampled_data_table = data_table.sample(2000000).copy()

g.add_vertices(sampled_data_table.shape[0])

g.vs["name"] = (
    sampled_data_table["title"]
    .fillna("")
    .str.encode("ascii", "ignore")
    .str.decode("ascii")
    .values
) # Name for search
g.vs["weight"] = ... # can be numeric  
g.vs["category"] = # can be any categoric
g.vs["foxjumpsover"] = ... # you can use any name for the key  
g.vs["Position"] = (sampled_data_table[["x", "y"]].values * 50).tolist() # this determines the location of points

# g.add_edges(edges) # you can connects lines. 

xnetwork.igraph2xnet(g, "all-science.xnet", [], [])

# %%
