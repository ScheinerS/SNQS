#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:52:16 2023

@author: santiago
"""

'''
Verification. Shettell & Markham.
'''

import itertools
import netsquid as ns

# l = len(Q)

l = 3
operators = []

for i in range(l):
    operators = [ns.X]*l
    operators[l-1] = ns.Y # replace the (l-1)th
    print(operators)
