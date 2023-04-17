import os
# import sys
import shutil
from datetime import datetime
import pandas as pd

def check_dir(path):
    is_dir = os.path.isdir(path)
    if(not is_dir):
        os.mkdir(path)
        print('Created:', path)

def save_parameters(directory):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    shutil.copy2('parameters.csv', directory + os.sep + 'parameters_' + timestamp + '.csv')

def read_parameters(filename):
    P = pd.read_csv('parameters.csv', header=0)
    P['value'] = pd.to_numeric(P['value'], downcast='integer', errors='ignore')
    parameters = dict(zip(P['parameter'], P['value']))
    return parameters