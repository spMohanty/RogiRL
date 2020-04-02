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



* Free software: GNU General Public License v3
* Documentation: https://rogi-rl.readthedocs.io.


## Author
* Sharada Mohanty  
