import neighbors
import matplotlib.pyplot as plt

'''
This script plots data from the eurostat panel.
'''

panel = neighbors.main()

borders = [list(panel[el][panel['neighbor_joined']==True][panel[el].notnull()])
           for el in panel.columns.tolist()[8:-4]]

interior = [list(panel[el][panel['neighbor_joined']==False][panel[el].notnull()])
            for el in panel.columns.tolist()[8:-4]]

# getting averages, years for every 2 years

y1 = [sum(el)/len(el) for el in borders]
y1 = [y1[i] for i in range(0,len(y1),2)]

y2 = [sum(el)/len(el) for el in interior]
y2 = [y2[i] for i in range(0,len(y2),2)]

years = panel.columns.tolist()[8:-4]
years1 = [i for i in range(1993,2014,2)]

# plot
plt.plot(years1,y1, label = 'Border Regions')
plt.plot(years1,y2, label = 'Interior Regions')
plt.xticks(years1)
plt.plot((2004, 2004), (0,500), 'k-', label = '2004')
plt.legend()
plt.ylabel('Per Capita R&D Expenditure')
plt.xlabel('Year')
