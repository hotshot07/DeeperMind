import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams["figure.figsize"] = (16,9)

W = 0.2

AGENT='Q-learning'
CONNECT=4
FILE_NAME="qlearn3_p1all3"


df = pd.read_csv(f"../plot_data/{FILE_NAME}.csv")

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
plt.ylabel('Number of games', fontsize=16)

plt.title(f"Outcomes of Connect {CONNECT} games: {AGENT} vs different algorithms", fontsize=20)
plt.savefig(f'figures/{FILE_NAME}.png', dpi=300, bbox_inches='tight')
# plt.show()


# qlearn4_p2,29,27,44
#qlearn3_p2,27,3,70


