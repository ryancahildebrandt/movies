#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 15:42:46 2020

@author: ryan
"""
# %% Script setup
from eda import *
import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
import seaborn as sns
import squarify

global jnt 
global prll 
global chrd

sns.set(style="dark",
        palette="PuBuGn_d",
        font="DejaVu Sans")

import holoviews as hv
from holoviews import opts, dim
from bokeh.sampledata.les_mis import data
from IPython.display import display_html

hv.extension("bokeh")

#%%
prplt=sns.pairplot(movies)
prplt.savefig("prplt.png")

# %% score vs metascore
jnt = sns.jointplot(x="Score",
              y="Metascore",
              data=movies,
              kind="reg",
              dropna=True)# "scatter" | "reg" | "resid" | "kde" | "hex"

jnt.savefig("jointplot.png")


# %% chord- genres
movies_genres12 = pd.crosstab(movies.Genre1, movies.Genre2)
movies_genres13 = pd.crosstab(movies.Genre1, movies.Genre3)

movies_chord12 = hv.Dataset((list(movies_genres12.columns),
                           list(movies_genres12.index),
                           movies_genres12),
                          ['source', 'target'], 'value_12').dframe()

movies_chord13 = hv.Dataset((list(movies_genres13.columns),
                           list(movies_genres13.index),
                           movies_genres13),
                          ['source', 'target'], 'value_13').dframe()

movies_chord = pd.DataFrame.merge(movies_chord12,movies_chord13, how="outer")
movies_chord["value"]=movies_chord.value_12+movies_chord.value_13.fillna(0).astype(int)
movies_chord.drop(["value_12","value_13"], 1, inplace=True)

chrd = hv.Chord(movies_chord).opts(
    node_color='index',
    edge_color='source',
    label_index='index', 
    cmap='Category20b',
    edge_cmap='Category20b',
    width=750,
    height=750)
hv.render(chrd,backend="bokeh")
hv.save(chrd,"chord.html", backend="bokeh")

# %% score decile vs other quant vars
movies_parallel=movies[["Metascore Decile","Score","Metascore","Vote","Runtime","Revenue","Revenue/Min","Meta:Score"]]
movies_parallel_norm=(movies_parallel.drop("Metascore Decile", axis=1)-movies_parallel.drop("Metascore Decile", axis=1).mean())/movies_parallel.drop("Metascore Decile", axis=1).std()
movies_parallel_norm["Metascore Decile"]=movies["Metascore Decile"]
#parallel_coordinates(movies_parallel_norm, "Metascore Decile")
#plt.show()

movies_parallel_desc = movies_parallel.groupby("Metascore Decile").describe()[zip(movies_parallel.columns[1:],np.repeat("mean",8))]
movies_parallel_desc["Metascore Decile"]=movies_parallel_desc.index
movies_parallel_desc_norm=(movies_parallel_desc.drop("Metascore Decile", axis=1)-movies_parallel_desc.drop("Metascore Decile", axis=1).mean())/movies_parallel_desc.drop("Metascore Decile", axis=1).std()
movies_parallel_desc_norm["Metascore Decile"]=movies_parallel_desc_norm.index

prll = parallel_coordinates(movies_parallel_desc_norm, "Metascore Decile")
prll.set_xticklabels(prll.get_xticklabels(),rotation=45)


#prll.figure.savefig("prll.png")

# %%


