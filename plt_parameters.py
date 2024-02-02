#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:08:59 2023

@author: santiago
"""
import matplotlib.pyplot as plt

plt.close('all')
plt.rcParams['text.usetex'] = True

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}

plt.rc('font', **font)