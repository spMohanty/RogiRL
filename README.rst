=======
Rogi RL
=======


.. image:: https://img.shields.io/pypi/v/rogi_rl.svg
        :target: https://pypi.python.org/pypi/rogi_rl

.. image:: https://img.shields.io/travis/spMohanty/rogi_rl.svg
        :target: https://travis-ci.com/spMohanty/rogi_rl

.. image:: https://readthedocs.org/projects/rogi-rl/badge/?version=latest
        :target: https://rogi-rl.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

|

.. image:: https://i.imgur.com/tvuQdcz.png
        :target: https://i.imgur.com/tvuQdcz.png
        :alt: rogi-rl-logop

A simple Gym environment for RL experiments around disease transmission in a grid world environment.

***************
Installation
***************
.. highlight:: bash
.. code-block:: 
        pip install -U git+https://github.com/spMohanty/rogi_rl.git
        rogi-rl-demo


***************
Usage
***************
.. highlight:: python
.. code-block:: 
        #! /usr/bin/env python
        
        from rogi_rl import RogiSimEnv
        
        env = RogiSimEnv()

        observation = env.reset()
        done = False
        while not done:
            observation, reward, done, info = env.step(env.action_space.sample())



* Free software: GNU General Public License v3
* Documentation: https://rogi-rl.readthedocs.io.


Features
--------

* TODO

  
