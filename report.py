#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 08:42:55 PM EDT 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import datapane as dp

from viz import *

# read graphs
with open("./outputs/full_graph.html", "rt") as f:
    full_html = f.read()

with open("./outputs/chapter_graph.html", "rt") as f:
    chapter_html = f.read()

# report
rprt = dp.View(
	dp.Text("""
# Genji & Friends
#### *Extracting character relationships Murasaki Shikibu's **The Tale of Genji** (源氏物語)*

---

## Dataset

The datasets used for the current project were pulled from the following: 
- [Aozora Bunko Corpus](https://www.kaggle.com/datasets/ryancahildebrandt/azbcorpus) for Japanese full text of The Tale of Genji
- [源氏物語の登場人物](https://ja.wikipedia.org/wiki/%E6%BA%90%E6%B0%8F%E7%89%A9%E8%AA%9E%E3%81%AE%E7%99%BB%E5%A0%B4%E4%BA%BA%E7%89%A9), for a list of named characters in the text

---

## Approach

This project uses an approach similar to [A Network of Thrones](https://networkofthrones.wordpress.com/) and other character network projects. The general process for this kind of project is very straightforward, and generally consists of:
- Identifying and extracting mentions of named characters in a text
- Counting interactions or relationships between characters, where an interaction is defined as two character mentions happening within a certain number of words/tokens of one another in the text
- Creating a graph network from this list of interactions, using the number of interactions between two given characters to dictate the edge weights

---

## Results

The following are the main outputs of the text analysis, split into networks for the full text and interactions by chapter. Here, I used an interaction distance of 25 tokens, which is a little longer than other projects due to Japanese's tendency to not explicitly mention names in every sentence relating to an individual. A larger window helps to capture interactions which may stretch over longer portions of the text before naming the characters involved.
    """),
    dp.HTML(full_html, label = "Full Text Graph"),
    dp.Text("""
    *This is the network for all 56 chapters included in this project.*
    *Unsurprisingly, Genji (光源氏) finds himself at the center of the graph as he has by far the most frequent and wide reaching interactions with other characters.*
    """),
    dp.HTML(chapter_html, label = "Chapter Graph"),
    dp.Text("""
    *Here, each subgraph corresponds to one chapter and the chapter numbers are noted before the name of the character node.*
    *Interestingly, there are a fair number of chapters which don't explicitly name Genji, or at least Genji doesn't "interact" with another character.*
    """),
	dp.Text("""# 完了""")
	)

dp.save_report(rprt, path = './outputs/genji_rprt.html', open = True)
