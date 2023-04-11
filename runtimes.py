#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 11:18:18 2023

@author: santiago
"""

import matplotlib.pyplot as plt
import aux

N = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
runtimes = [5, 8, 11, 15, 18, 26, 39, 92, 270, 917]
Qubits_received = [3413, 2807, 2179, 1693, 1181, 834, 507, 370, 219, 145]

aux.check_dir('plots')

plt.close('all')

plt.figure()
plt.scatter(N, runtimes)
plt.title(r'Runtimes')
plt.xlabel(r'N')
plt.ylabel(r'time [s]')
plt.grid()
plt.savefig('plots/runtimes.png')

plt.figure()
plt.scatter(N, Qubits_received)
plt.title(r'Qubits received by the N nodes')
plt.xlabel(r'N')
plt.ylabel(r'\# Qubits received')
plt.grid()
plt.savefig('plots/qubits_received.png')