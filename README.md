# Rogi RL


[![](https://img.shields.io/pypi/v/rogi_rl.svg)](https://pypi.python.org/pypi/rogi_rl)
[![](https://img.shields.io/travis/spMohanty/rogi_rl.svg)](https://travis-ci.com/spMohanty/rogi_rl)
[![](https://readthedocs.org/projects/rogi-rl/badge/?version=latest)](https://rogi-rl.readthedocs.io/en/latest/?badge=latest)

   
![](https://i.imgur.com/tvuQdcz.png)


A simple Gym environment for RL experiments around disease transmission in a grid world environment.

## Installation


``` bash
pip install -U git+https://github.com/spMohanty/rogi_rl.git
rogi-rl-demo
```

and if everything went well, ideally you should see something along the lines of ![this](https://i.imgur.com/AKAi0yQ.png).

## Usage

``` python
#! /usr/bin/env python

from rogi_rl import RogiSimEnv

env = RogiSimEnv()

observation = env.reset()
done = False
while not done:
    observation, reward, done, info = env.step(env.action_space.sample())
```

### Usage with ASCII Renderer
``` python

from rogi_rl import RogiSimEnv

env_config = dict(
                width=10,
                height=10,
                population_density=0.80,
                vaccine_density=1.0,
                initial_infection_fraction=0.02,
                use_renderer="ascii")

env = RogiSimEnv(env_config)

observation = env.reset()
done = False
env.render(mode="ascii")
while not done:
    _action = input("Enter action - ex: [1, 4, 2] : ")
    if _action.strip() == "":
        _action = env.action_space.sample()
    else:
        _action = [int(x) for x in _action.split()]
        assert _action[0] in [0, 1]
        assert _action[1] in list(range(env._model.width))
        assert _action[2] in list(range(env._model.height))
    print("Action : ", _action)
    observation, reward, done, info = env.step(_action)
    env.render(mode="ascii")
```


## Available Configurations

You can instantiate a RogiSim enviornment with the following configuration options 

``` python


_config =  dict(
    width=50, # widht of the grid
    height=50, # height of the grid
    population_density=0.75, # %-age of the grid to be filled by agents
    vaccine_density=0.05, # no. of vaccines available as a fractions of the population
    initial_infection_fraction=0.1, # %-age of agents which are infected in the beginning 
    initial_vaccination_fraction=0.05,# %-age of agents which are vaccinated in the beginning 
    prob_infection=0.2, # probability of infection transmission on a single contact
    prob_agent_movement=0.0, # probability that an agent will attempt to move an empty cell around it
    disease_planner_config={
        "latent_period_mu" :  2 * 4,
        "latent_period_sigma" :  0,
        "incubation_period_mu" :  5 * 4,
        "incubation_period_sigma" :  0,
        "recovery_period_mu" :  14 * 4,
        "recovery_period_sigma" :  0,
    },
    max_timesteps=200, # maximum timesteps per episode 
    early_stopping_patience=14, # in-simulator steps to wait with the same susceptible population fraction before concluding that the simulation has ended
    use_renderer=False, # Takes : False, "human", "ascii"
    toric=True, # Make the grid world toric
    dummy_simulation=False, # Send dummy observations, rewards etc. Useful when doing integration testing with RL Experiments codebase
    debug=True)

env = RogiEnv(config=_config)


```






* Free software: GNU General Public License v3
* Documentation: https://rogi-rl.readthedocs.io.


## Author
* Sharada Mohanty  
