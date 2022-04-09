# from utils import *
import game
import argparse
from agents import bfs_agent
from agents import random_agent
from agents import dfs_agent
from agents import human_agent
from agents import minimax_agent
# import agents.random_agent


class Arena:
    def __init__(self, agent_1, agent_2, num_games) -> None:
        self.agent_1 = self._get_agent_from_string(agent_1, 1)
        self.agent_2 = self._get_agent_from_string(agent_2, 2)
        self.num_games = num_games
        self.victor = None

        #used for graphing
        self.agent_2_wins = 0
        self.agent_2_ties = 0
        self.agent_2_losses = 0

        print('arena initialised')

    def _get_agent_from_string(self, agent_string, agent_number):

        if agent_string == 'dfs':
            return dfs_agent.Dfs_agent(agent_number)
        if agent_string == 'bfs':
            return bfs_agent.Bfs_agent(agent_number)
        if agent_string == 'minimax':
            return minimax_agent.Minimax_agent(agent_number,4)
        if agent_string == 'random':
            return random_agent.Random_agent(agent_number)
        if agent_string == 'qlearn':
            pass
        if agent_string == 'nn':
            pass
        if agent_string == 'human':
            return human_agent.Human_agent(agent_number)
    
    def new_game(self):
        self.victor = None