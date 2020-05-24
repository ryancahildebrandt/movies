#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 20:53:20 2020

@author: ryan
"""
# %% Doc setup
import pandas as pd
import numpy as np

# %% Read in movies data
global movies
movies = pd.read_csv("movies.csv")
movies["Vote"]=movies["Vote"].astype("float64")
movies["Runtime"]=movies["Runtime"].astype("float64")
movies[["Genre1","Genre2","Genre3"]]=movies.Genre.str.split(", ",expand=True)
movies["Revenue/Min"]=movies["Revenue"]/movies["Runtime"]
movies["Meta:Score"]=movies["Metascore"]/movies["Score"]*10
movies["Score Decile"]=movies["Score"].apply(np.floor)
movies["Metascore Decile"]=(movies["Metascore"]/10).apply(np.floor)
movies["Decade"]=((movies["Year"]/10).apply(np.floor))*10

#movies.to_csv("movies_out.csv", index=False)

# %% Useful lists
all_genres = movies["Genre1"].append(movies["Genre2"]).append(movies["Genre3"]).dropna().unique().tolist()
all_directors = movies["Director"].dropna().unique().tolist()

# %% Take a look
movies.info()
movies.head()
movies.describe()




