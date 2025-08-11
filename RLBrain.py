#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:22:30 2020

@author: jingci
"""

import numpy as np
import pandas as pd


class RLBrain():
    '''
    Before running the code, please modify this file path as needed
    '''
    FILEPATH = '/Users/mirodilbekfazilov/developer/simu/Warehouse_Robot_Path_Planning/'
    def choose_action(self, observation, epsilon):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def learn(self, s, a, r, s_, alpha, gamma):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += alpha * (q_target - q_predict)  # update
        #print (self.q_table)

    """def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )"""

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table using concat
            new_row = pd.Series(
                [0] * len(self.actions),
                index=self.q_table.columns,
                name=state
            )
            self.q_table = pd.concat([self.q_table, new_row.to_frame().T])
