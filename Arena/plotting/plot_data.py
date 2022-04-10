import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

W = 0.2



df = pd.read_csv("/Users/hotshot07/Desktop/DeeperMind/Arena/data/random.csv")

agent_names = list(df['name'])

wins = list(df['wins'])
ties = df['ties'].to_list()
losses = df['losses'].to_list()


bar1 = np.arange(len(agent_names))
bar2 = [i+W for i in bar1]
bar3 = [i+W for i in bar2]


plt.bar(bar1,wins,W,label = 'wins')
plt.bar(bar2,losses,W,label = 'losses')
plt.bar(bar3,ties,W,label = 'ties')
plt.ylim(top=100)

plt.legend()

plt.xticks(bar1+W,agent_names)

plt.xlabel('Agents')
plt.ylabel('Games')

plt.title("Neural network hybrid shit")
plt.show()



