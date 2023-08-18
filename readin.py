#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 04:45:30 PM EDT 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import pandas as pd
import duckdb

# texts readin
con = duckdb.connect("data/aozora_corpus.db")
genji_query = """
SELECT work_id, work_name, subtitle, main_text, n_char  
FROM texts 
JOIN 
    (
        SELECT DISTINCT work_id, work_name, subtitle 
        FROM works 
        WHERE work_name = '源氏物語'
        ) 
USING (work_id)
"""

texts_df = con.sql(genji_query).df()
chapter_texts = texts_df["main_text"].tolist()
full_text = "".join(chapter_texts)
texts_df["main_text"] = texts_df["main_text"].map(lambda text: text.split("。"))
texts_df = texts_df.explode("main_text")
sentence_texts = texts_df["main_text"].tolist()
texts_df["sentence_position"] = range(len(texts_df))

# names readin
#https://ja.wikipedia.org/wiki/%E6%BA%90%E6%B0%8F%E7%89%A9%E8%AA%9E%E3%81%AE%E7%99%BB%E5%A0%B4%E4%BA%BA%E7%89%A9
names_df = pd.read_csv("data/characters.csv").fillna("")
names_dict = {i.name : list(filter(None, [i.name, i.alt1, i.alt2])) for i in names_df.itertuples()}

additional_aliases = {
    "大輔の命婦" : "大輔",
    "小野の妹尼" : "小野",
    "朧月夜" : "月夜",
    "紀伊守" : "紀伊",
    "光源氏" : "源氏",
    }
additional_names = {
    "玄宗" : "玄宗",
    "関白" : "関白",
    "楊貴" : "楊貴",
    "大蔵" : "大蔵"
    }
ambiguous_names = {
    "姫" : "姫",
    "妹" : "妹",
    "婿" : "婿",
    "帝" : "帝",
    "妃" : "妃",
    "后" : "后",
}

for i in additional_aliases:
    names_dict[i] = names_dict[i] + [additional_aliases[i]]

names_dict.update(additional_names)

names_map = {}
for person in names_dict:
    for alias in names_dict[person]:
        names_map[alias] = person