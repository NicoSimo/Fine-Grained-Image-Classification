import scipy.io
import pandas as pd
import os
import json

def convert(input_path, output_path):
    '''
    Function that takes in input the path to a .mat file and the path to the output csv file.
    input_path: str, path to the input .mat file
    output_path: str, path to the output csv file
    '''

    mat_file = scipy.io.loadmat(input_path)
    mat_file = {k:v for k, v in mat_file.items() if k[0] != '_'}

    output_data = pd.DataFrame({k: pd.Series(v[0]) for k, v in mat_file.items()}) 

    output_data.to_csv(output_path)