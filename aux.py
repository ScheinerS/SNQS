import os
import pandas as pd

def check_dir(path):
    is_dir = os.path.isdir(path)
    if(not is_dir):
        os.mkdir(path)
        print('Created:', path)

def save_parameters(directory):
    from datetime import datetime
    import shutil
    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    shutil.copy2('parameters.csv', directory + os.sep + 'parameters_' + timestamp + '.csv')

def read_parameters(filename):
    # filename = 'parameters'
    
    P = pd.read_csv(filename + '.csv', skiprows=0)
    P['value_num'] = pd.to_numeric(P['value'], downcast='integer', errors='ignore')
    P['value'] = P['value_num'][P['value_num'].notna()]
    
    # Q = pd.DataFrame()
    # Q['value'] = pd.to_numeric(P['value'], errors='ignore')
    
    
    parameters = dict(zip(P['parameter'], P['value']))
    return parameters

def read_network(network_name):
    path = 'networks' + os.sep 
    try:
        network = pd.read_csv(path + network_name + '.csv', header=0)
        return network
    except:
        import glob
        import sys
        print('Network "%s" not found in directory "%s". Available networks:\n'%(network_name, path))
        for file in sorted(glob.glob(path + '*.csv')):
            print(file.split('/')[-1].split('.')[0])
        sys.exit()