import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


url = "http://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')

title = soup.title
#print(title)

rows = soup.find_all('tr')
for row in rows:
    row_td = row.find_all('td')
#print(row_td)

str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
#print(cleantext)

list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
#print(clean2)

df = pd.DataFrame(list_rows)

df1 = df[0].str.split(',', expand=True)

df1[0] = df1[0].str.strip('[')

col_labels = soup.find_all('th')

all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
#print(all_header)

df2 = pd.DataFrame(all_header)

df3 = df2[0].str.split(',', expand=True)

frames = [df3, df1]

df4 = pd.concat(frames)

df5 = df4.rename(columns=df4.iloc[0])

df6 = df5.dropna(axis=0, how='any')
df6.info()
df6.shape

df7 = df6.drop(df6.index[0])
df7.head()

df7.rename(columns={'[Place': 'Place'},inplace=True)
df7.rename(columns={' Team]': 'Team'},inplace=True)

df7['Team'] = df7['Team'].str.strip(']')

df8 = df7.replace('\n','', regex=True)
df8 = df8.replace('\r','', regex=True)

time_list = df8[' Chip Time'].tolist()

time_mins = []
for i in time_list:
    try:
        h, m, s = i.split(':')
    except:
        h = 0
        m, s = i.split(':')
    math = (int(h) * 3600 + int(m) * 60 + int(s))/60
    time_mins.append(math)
#print(time_mins)

df8['Runner_mins'] = time_mins
df8.head()

df8.describe(include=[np.number])


from pylab import rcParams
rcParams['figure.figsize'] = 15, 5
 
df8.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
plt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])

x = df8['Runner_mins']
ax = sns.displot(x, kind='hist', kde=True, rug=False, color='m', bins=25, edgecolor='black')
plt.show()

#f_fuko = df8.loc[df8[' Gender']==' F']['Runner_mins']
#m_fuko = df8.loc[df8[' Gender']==' M']['Runner_mins']
#sns.displot(f_fuko, kind='hist', kde=True, rug=False, edgecolor='black', label='Female')
#sns.displot(m_fuko, kde=True, rug=False, edgecolor='black', label='Male')
#plt.legend()


f_fuko = df8.loc[df8[' Gender']==' F']['Runner_mins']
m_fuko = df8.loc[df8[' Gender']==' M']['Runner_mins']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Female')
sns.distplot(m_fuko, hist=False, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Male')
plt.legend()
plt.show()

g_stats = df8.groupby(" Gender", as_index=True).describe()
print(g_stats)

df8.boxplot(column='Runner_mins', by=' Gender')
plt.ylabel('Chip Time')
plt.suptitle("")