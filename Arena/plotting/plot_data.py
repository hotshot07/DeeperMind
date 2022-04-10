import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

W = 0.2

AGENT='bfs'


df = pd.read_csv("../plot_data/bfsall4.csv")

agent_names = list(df['name'])

wins = list(df['wins'])
ties = df['ties'].to_list()
losses = df['losses'].to_list()


bar1 = np.arange(len(agent_names))
bar2 = [i+W for i in bar1]
bar3 = [i+W for i in bar2]


plt.bar(bar1,wins,W,label = f'Wins against {AGENT}')
plt.bar(bar2,losses,W,label = f'Losses against {AGENT}')
plt.bar(bar3,ties,W,label = 'Ties')
plt.ylim(top=100)

plt.legend()

plt.xticks(bar1+W,agent_names)

plt.xlabel('Agents', fontsize = 16)
plt.ylabel('Games', fontsize=16)

plt.title(f"{AGENT} vs ..")
plt.show()



