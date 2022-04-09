import matplotlib.pyplot as plt
import numpy as np

W = 0.2

agent_names = ["apple", "banana", "custard"]

wins = [5,6,7]
ties = [2,6,1]
losses = [8,1,2]


bar1 = np.arange(len(agent_names))
bar2 = [i+W for i in bar1]
bar3 = [i+W for i in bar2]


plt.bar(bar1,wins,W,label = 'wins')
plt.bar(bar2,ties,W,label = 'ties')
plt.bar(bar3,losses,W,label = 'losses')

plt.legend()

plt.xticks(bar1+W,agent_names)

plt.xlabel('Agents')
plt.ylabel('Games')

plt.title("cool bar plots of my favourite pies")
plt.show()



