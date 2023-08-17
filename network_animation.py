#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:15:47 2023

@author: santiago
"""

import sys
import os
import glob
import imageio
import aux

# path = os.path.dirname(os.path.realpath('__file__'))
# sys.path.append(path)

#%%

def animation(network_name):
    # network_name = parameters['network']
    # file = 'Maze_5_many_solutions'
    FPS = 1    # frames per second
    animation_format = 'mp4' # 'mpeg', 'mp4', 'gif', ...
    
    AddFinalSecond = True   # to add a second at the end
    
    L = len(glob.glob('plots' + os.sep + network_name + os.sep + "*.png"))
    
    filenames = sorted(glob.glob('plots' + os.sep + network_name + os.sep + "*"))
    
    # for i in range(L):
    #     #print('Adding frame %d/%d\r'%(i,L), end='')
    #     filenames.append(file + '/' + network_name + '-' + str(i) + '.png')
    
    
    images = []
    
    for filename in filenames:
        images.append(imageio.imread(filename))
    
    if AddFinalSecond:
        for i in range(FPS):
            images.append(imageio.imread(filename))
    
    aux.check_dir('animations')
    imageio.mimsave('animations' + os.sep + network_name + '.' + animation_format, images, fps=FPS)
    
if __name__ == '__main__':
    animation('QEurope')