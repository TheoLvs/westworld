# Westworld
![](./img/cover_hq_westworld1.jpg)
> *Photo by Alexander London on Unsplash*

## Description
**Westworld** is a multi-agent simulation library, its goal to simulate and optimize systems and environments with multiple agents interacting. Its inspiration is drawn from Unity software and [Unity ML Agents](https://github.com/Unity-Technologies/ml-agents), adapted in Python. 

The goal is to be able to simulate environments in logistics, retails, epidemiology, providing pre-coded spatial environments and communication between agents. Optimization can be included using heuristics as well as Reinforcement Learning.

!!! warning "Experimental"
    This library is extremely experimental, under active development and alpha-release
    Don't expect the documentation to be up-to-date or all features to be tested
    Please contact [us](mailto:theo.alves.da.costa@gmail.com) if you have any question

*The name is of course inspired by the TV series Westworld, which is actually a gigantic multi-agent simulation system.*


## Features
### Current features
- Easy creation of Grid and non-grid environments
- Objects (Agents, Obstacles, Collectibles, Triggers)
- Subclassing of different objects to create custom objects
- Spawner to generate objects randomly in the environment
- Basic rigid body system for all objects
- Simple agent behaviors (pathfinding, wandering, random walk, fleeing, vision range)
- Automatic maze generation
- Layer integration to convert image to obstacle and snap it to a grid
- Sample simulations and sample agents for classic simulations
- Simulation visualization, replay and export (gif or video)

### Roadmap features
- More classic simulations and tutorials (boids, sugarscape)
- Better pathfinding
- Easy Reinforcement Learning integration with Stable Baselines
- Other visualization functions than PyGame for web integration 


## Installation
### Install from PyPi
The library is available on [PyPi](https://pypi.org/project/westworld/) via 
```
pip install westworld
```

### For developers
- You can clone the github repo / fork and develop locally
- Poetry is used for environment management, dependencies and publishing, after clone you can run 

```
# To setup the environment
poetry install

# To run Jupyter notebook or a python console
poetry run jupyter notebook
poetry run python
```

## Contributors
- [Théo Alves Da Costa](mailto:theo.alves.da.costa@gmail.com)





