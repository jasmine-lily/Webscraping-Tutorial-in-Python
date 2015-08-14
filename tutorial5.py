import csv
import re
from matplotlib import pyplot as plt
import operator
from pandas import DataFrame

#===============================================================================
#read in an existing list of skill sets
#===============================================================================
with open('tools.txt') as f1, open('analysismethod.txt') as f2:
    tools = f1.read().lower().split('\n')
    analysis = f2.read().lower().split('\n')
f1.close(); f2.close()

skills = tools + analysis

#===============================================================================
#count the number of skills mentioned in the job descriptions
#===============================================================================

slib = {}
with open('data_scientist_jobs.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c = row['desc'].lower()
        for i in skills:
            items = i.split(',')
            if len(items) == 1:
                reg = r'\b{}s?\b'.format(re.escape(i))
            else:
                reg = []            
                for i in range(len(items)):
                    reg.append(r'\b{}s?\b'.format(re.escape(items[i])))
                reg = '|'.join(reg)
            if len(re.findall(reg, c))!=0:
                if items[0] not in slib:
                    slib[items[0]] = 1
                else:
                    slib[items[0]] += 1
 
from operator import itemgetter
sorted_lib = sorted(slib.items(), key=itemgetter(1),reverse=True)

top20 = [] 
for i in sorted_lib[:20]:   
    top20.append(i)
  
 #===============================================================================
 #Plot bar chart of the numbers
 #=============================================================================== 
  
from pylab import *
val = [w[1] for w in reversed(sorted_lib[:20])]
pos = arange(20)+.5    

figure(1)
barh(pos,val, align='center')
yticks(pos, [w[0].upper() for w in reversed(sorted_lib[:20])],fontsize=11)
xlabel('Frequency'.upper(),fontsize=14)
title('What Skills are Most Wanted?\n',fontsize=20)
grid(True) 
 
show()
 
#===============================================================================
# Does location matters?
#===============================================================================
 
#===============================================================================
# Compute the skill frequencies for the West and other locations
#===============================================================================

import pandas as pd
import numpy as np

jobs = DataFrame.from_csv('data_scientist_jobs.csv',index_col=None)

#-------------------------------------------------------------------------------
# Extract state from address
#-------------------------------------------------------------------------------

location = []
for i in jobs.address:
    try:
        location.append(i.split(',')[1].strip())
    except:
        location.append('Error')

#-------------------------------------------------------------------------------
# Divide the data into two groups 
# 1. West(CA and WA)
# 2. Other locations
#-------------------------------------------------------------------------------
            
location = pd.Series(location)
illegal = location == 'Error'
west = (location == 'CA') | (location == 'WA')
west, other = jobs.desc[west], jobs.desc[np.invert(illegal|west)]


#-------------------------------------------------------------------------------
# Define the count function
#-------------------------------------------------------------------------------

def count(doc, skills):
    slib = {}
    for i in doc.index:
        c = doc[i].lower()
        for i in skills:
            items = i.split(',')
            if len(items) == 1:
                reg = r'\b{}s?\b'.format(re.escape(i))
            else:
                reg = []            
                for i in range(len(items)):
                    reg.append(r'\b{}s?\b'.format(re.escape(items[i])))
                reg = '|'.join(reg)
            if len(re.findall(reg, c))!=0:
                if items[0] not in slib:
                    slib[items[0]] = 1
                else:
                    slib[items[0]] += 1
    return slib

#-------------------------------------------------------------------------------
# Compute the skill frequencies for the two data sets
#-------------------------------------------------------------------------------

westlib = count(west,skills)
otherlib = count(other,skills)


#===============================================================================
# Plot the frequencies of skills for the West and other locations
#===============================================================================

import numpy as np
import matplotlib.pyplot as plt

topskills = [w[0] for w in top20]

westlib_query = [(w,westlib[w]) for w in westlib if w in topskills]
otherlib_query = [(w,otherlib[w]) for w in otherlib if w in topskills]
   
skills = reversed([w.upper() for w in topskills])
west = np.array([w[1] 
                 for i in reversed(topskills) 
                 for w in westlib_query
                 if w[0] == i])
other = np.array([w[1] 
                 for i in reversed(topskills) 
                 for w in otherlib_query
                 if w[0] == i])


import csv
with open('output.csv', 'wb') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(zip(west,other))
f.close()

y = pos = arange(20)+.5   
    
fig, axes = plt.subplots(ncols=2, sharey=True)
axes[0].barh(y,west, align='center', zorder=10)
axes[0].set(title='West')
axes[1].barh(y,other, align='center', zorder=10)
axes[1].set(title='Other')
    
axes[0].invert_xaxis()
axes[0].set(yticks=y, yticklabels=[])
for yloc, skill in zip(y, skills):
    axes[0].annotate(skill, (0.5, yloc), xycoords=('figure fraction', 'data'),
                     ha='center', va='center')
axes[0].yaxis.tick_right()
    
for ax in axes.flat:
    ax.margins(0.03)
    ax.grid(True)
    
fig.tight_layout()
fig.subplots_adjust(wspace=0.25)
plt.show()










       
