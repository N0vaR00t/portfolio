"""
Diana Nykonenko
DQN algorithm 
"""

import gymnasium as gym                                                          # importing space
import gym_anytrading
from stable_baselines3.common.vec_env import DummyVecEnv                        
from stable_baselines3 import DQN                                                # importing algorithm 
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import yfinance as yf                                                            # importing database
import csv


# Read CSV file into a DataFrame 
data = pd.read_csv('test_data.csv') 

data.shape

env = gym.make('stocks-v0',                                                      # creating environment
                df=data,
                frame_bound=(3, 100),
                window_size=3)

state = env.reset()

while True:
  
  obs, reward, done, trunc, info = env.step(env.action_space.sample())

  if done or trunc:

    print('info: ', info)
    break

plt.figure(figsize=(15,6), facecolor='w')
plt.cla()
env.render_all()
plt.show()

env_maker = lambda: gym.make('stocks-v0',                                         # space for training
                            df=data, 
                            frame_bound=(10,1000), 
                            window_size=5)

env = DummyVecEnv([env_maker])                                                    # environment

model = DQN('MlpPolicy', env, verbose=1,                                          # defining model 
            learning_rate=0.00025, 
            gamma=0.99,
            buffer_size=10000, 
            batch_size=512)

model.learn(total_timesteps=100000)                                               # setting time staps

env = gym.make('stocks-v0',                                                       # creating the space
                df=data, 
                frame_bound=(1000, 2200), 
                window_size=5)

obs, info = env.reset()

while True:                                                                       # testing the model 
 
  action, _states = model.predict(obs)
  obs, rewards, done, trunc, info = env.step(action)

  if done or trunc:

    print('info: ', info)
    break
  
plt.figure(figsize=(15,6), facecolor='w')                                         # plotting the graph
plt.cla()
env.render_all()
plt.show()