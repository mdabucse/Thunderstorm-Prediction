import pandas as pd
import numpy as np
data  = pd.read_csv('final_data_set.csv')
n = input("Enter Date")
for i in range(int(n),int(n)-7,-1):
    print(i)