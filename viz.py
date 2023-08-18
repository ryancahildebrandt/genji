#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 07:12:33 PM EDT 2023 
author: Ryan Hildebrandt, github.com/ryancahildebrandt
"""
# imports
import matplotlib.pyplot as plt
import pyvis.network as pv

from tagging import *

# by chapter
chapter_net = pv.Network()
for row in chapter_edgelist.itertuples():
    source = row[1]
    target = row[2]
    color = color_dict[row[3]]
    size = row[4]
    weight = row[5]

    chapter_net.add_node(source, source, title = source, color = color, value = size)
    chapter_net.add_node(target, target, title = target, color = color, value = size)
    chapter_net.add_edge(source, target, value = weight, color = color)

chapter_net.save_graph("outputs/chapter_graph.html")

# full text
full_net = pv.Network()
for row in full_edgelist.itertuples():
    source = row[1]
    target = row[2]
    size = row[3]
    weight = row[4]

    full_net.add_node(source, source, title = source, value = size)
    full_net.add_node(target, target, title = target, value = size)
    full_net.add_edge(source, target, value = weight)

full_net.save_graph("outputs/full_graph.html")
