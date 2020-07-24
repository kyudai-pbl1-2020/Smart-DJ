#Create sample of 10 lines of input data

import numpy as np
import pandas as pd
import random

sample = pd.DataFrame(columns=['month','hour','temperature','pressure','humidity'])
for i in range(10):
    month = random.randrange(1,13)
    hour = random.randrange(0,24)
    temperature = round(random.uniform(-20, 40),2)
    pressure = round(random.uniform(900, 1100),2)
    humidity = round(random.uniform(0, 100),2)
    sample = sample.append({'month':month,'hour':hour,'temperature':temperature,'pressure':pressure,'humidity':humidity},ignore_index=True)
#print(sample)
sample.to_csv('sample-sensor-data.csv',index=False)
#a = pd.read_csv('sample-sensor-data.csv')
#print(a)

