#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:36:56 2023

@author: santiago
"""

import pandas as pd
import os



def star(columns, N):
    
    network = pd.DataFrame(columns = columns, index=None)
    
    # Qonnector
    new_row = pd.DataFrame(['Qonnector', 'Qonnector', 'Qlient 1', 0, 3, 1]).transpose()
    new_row.columns = network.columns
    network = pd.concat([network, new_row], ignore_index=True)
    
    # Qlients
    for n in range(N):
        new_row = pd.DataFrame(['Qlient %d'%(n), 'Qlient', 'Qonnector', 1, 0, 0]).transpose()
        new_row.columns = network.columns
        network = pd.concat([network, new_row], ignore_index=True)

    return network


def joined_stars(columns, N_Qonnectors, N_Qlients):
    
    network = pd.DataFrame(columns = columns, index=None)
    
    # Qonnectors
    for n in range(N_Qonnectors):
        new_row = pd.DataFrame(['Qonnector %d'%(n), 'Qonnector', 'Qonnector %d'%((n+1)%N_Qonnectors), 1, 0, 0]).transpose()
        new_row.columns = network.columns
        network = pd.concat([network, new_row], ignore_index=True)
    
    # Qlients
    for N in range(N_Qonnectors):
        for n in range(N_Qlients):
            new_row = pd.DataFrame(['Qlient %d'%(N*N_Qlients + n), 'Qlient', 'Qonnector %d'%N, 1, 0, 0]).transpose()
            new_row.columns = network.columns
            network = pd.concat([network, new_row], ignore_index=True)

    return network

    
if __name__ == "__main__":
        
    flags = {'star': 0,
             'joined_stars': 1,
             }    
    
    path = 'networks' + os.sep    
    
    columns = ['Name', 'Type', 'Link', 'Distance to Qonnector (km)', 'Memory (size)', 'Processor']
    
    if flags['star']:
        N_max_star = 10
        for N in range(1, N_max_star+1):
            network = star(columns, N)
            network.to_csv(path + 'star_%02d.csv'%N, index=False)
    
    if flags['joined_stars']:
        N_Qonnectors = 2
        N_Qlients = 3
        network = joined_stars(columns, N_Qonnectors, N_Qlients)
        network.to_csv(path + 'joined_stars_%02dx%02d.csv'%(N_Qonnectors, N_Qlients), index=False)