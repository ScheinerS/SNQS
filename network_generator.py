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
    
    new_row = pd.DataFrame(['Qonnector', 'Qonnector', 'Qlient 1', 0, 3, 1]).transpose()
    new_row.columns = network.columns
    network = pd.concat([network, new_row], ignore_index=True)
    
    # Qlients
    for n in range(N):
        new_row = pd.DataFrame(['Qlient %d'%(n+1), 'Qlient', 'Qonnector', 1, 0, 0]).transpose()
        new_row.columns = network.columns
        network = pd.concat([network, new_row], ignore_index=True)

    return network
    
if __name__ == "__main__":
    N_max = 10
    
    columns = ['Name', 'Type', 'Link', 'Distance to Qonnector (km)', 'Memory (size)', 'Processor']
    for N in range(1, N_max+1):
        network = star(columns, N)
        path = 'networks' + os.sep
        network.to_csv(path + 'star_%02d.csv'%N, index=False)
