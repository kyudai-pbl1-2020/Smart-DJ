import pandas as pd

a = pd.read_csv('youtube-list.csv', index_col=0)
#print(a)
print(a.loc['sad','rainy'])