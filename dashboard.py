#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 21:12:23 2020

@author: ryan
"""
# %% Doc Setup
import altair as alt
import altair_viewer
import datapane as dp

from eda import *
from viz import *
alt.data_transformers.disable_max_rows()

# %% Legends
selection = alt.selection_multi(fields=["Genre1"])
color = alt.condition(selection,
                    alt.Color("Genre1:N", legend=None),
                    alt.value('lightgray'))
legend_genre = alt.Chart(movies).mark_rect().encode(
    y=alt.Y("Genre1:N",
            axis=alt.Axis(orient='right')),
    color=color
).add_selection(
    selection
    )
    
# %% Charts
sctr = alt.Chart(movies).mark_point(filled=True).encode(
    alt.X("Score:Q"),
    alt.Y("Metascore:Q"),
    alt.Size("Revenue:Q"),
    alt.OpacityValue(0.5),
    alt.Order("Rank:O", sort="ascending"),
    tooltip = [alt.Tooltip("Title:N"),
               alt.Tooltip("Year:O"),
               alt.Tooltip("Runtime:Q")
              ],
    color=color).add_selection(
    selection
).interactive()

#(sctr | legend_genre).show()

# %% Report
rprt = dp.Report(dp.Markdown("# 10,000 Movies Dataset Explorer"),
                 dp.Markdown("## Dataset"),
                 dp.Table(movies),
                 dp.Markdown("## Score vs Metascore"),
                 dp.Markdown("### **Explore by Genre**"),
                 dp.Plot(sctr | legend_genre),
                 dp.Markdown("## Genre 1 -> Genre 2 & Genre 3"),
                 dp.Plot(hv.render(chrd,backend="bokeh")))
rprt.save(path='movies_dashboard.html', open=True)
#rprt.publish(name='10000_Movies_Dataset_Explorer', open=True, visibility='PUBLIC')
#https://datapane.com/ryancahildebrandt/reports/10000_Movies_Dataset_Explorer