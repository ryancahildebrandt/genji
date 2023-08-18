#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 07:12:07 PM EDT 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import itertools
import fugashi
import numpy as np
import matplotlib.colors
import random

from readin import *

def scrape_text(in_text: str, in_tagger):
    texts = []
    names = []
    positions = []
    for token_index, token in enumerate(in_tagger(in_text)):
        if token.surface in names_map.keys():
            texts.append(token.surface)
            names.append(names_map[token.surface])
            positions.append(token_index)
    out = [texts, names, positions]
    return out

def collect_relationships(in_text: str, in_chapter_index: int, in_positions: list, in_names: list, window_size: int):
    relationship_dists = np.subtract.outer(in_positions, in_positions).flatten()
    relationship_names = [sorted(list(i)) for i in itertools.product(in_names, in_names)]
    relationships = pd.DataFrame({
        "chapter" : in_chapter_index,
        "name1" : [i[0] for i in relationship_names],
        "name2" : [i[1] for i in relationship_names],
        "distance" : relationship_dists,
    }).query('name1 != name2 and 0 < distance <= @window_size')
    out = relationships
    return out

# text tagging
tagger = fugashi.Tagger('-Owakati')
tagging_results = {}
color_dict = {}
window_size = 25 

for chapter_index, chapter in enumerate(chapter_texts):
    texts, names, positions = scrape_text(chapter, tagger)
    relationships = collect_relationships(chapter, chapter_index, positions, names, window_size)
    edgelist = relationships.value_counts(["name1", "name2", "chapter"]).to_frame().reset_index().rename(columns = {0 : "weight"})
    tagging_results[chapter_index] = { 
        "text" : texts, 
        "name" : names,
        "chapter" : chapter_index,
        "position" : positions, 
        "relationships" : relationships,
        "edgelist" : edgelist
    }
    color_dict[chapter_index] = random.choice(list(matplotlib.colors.CSS4_COLORS.keys()))

full_edgelist = pd.concat([tagging_results[i]["relationships"] for i in tagging_results]).value_counts(["name1", "name2"]).to_frame().reset_index().rename(columns = {0 : "n_edges"})
full_edgelist["log1p_weight"] = full_edgelist["n_edges"].map(np.log1p)

chapter_edgelist = pd.concat([tagging_results[i]["relationships"] for i in tagging_results]).value_counts(["name1", "name2", "chapter"]).to_frame().reset_index().rename(columns = {0 : "n_edges"})
chapter_edgelist["name1"] = "Chapter " + chapter_edgelist["chapter"].astype(str) + ": " + chapter_edgelist["name1"].astype(str)
chapter_edgelist["name2"] = "Chapter " + chapter_edgelist["chapter"].astype(str) + ": " + chapter_edgelist["name2"].astype(str)
chapter_edgelist["log1p_weight"] = chapter_edgelist["n_edges"].map(np.log1p)

full_edgelist.to_csv("./outputs/full_edgelist.csv")
chapter_edgelist.to_csv("./outputs/chapter_edgelist.csv")