# Reinforcement-Learning-Monster-Generation
Example of how to use reinforcement learning to generate "balanced" monsters.

Scripts: 
- MDP.py defines the Markov Decision Process based on the one from Chapter 10
- Qlearner.py defines the Q-learning training environment 
- GenerateMonster.py queries the trained Q-learning agent to generate a 'balanced' monster

Instructions: 
1. Install Python 3.9 (but tweaking it for other versions should be simple) and the 'pickle' library
2. Run GenerateMonster.py to generate a 'balanced' monster according to the reward function defined in MDP.py and based on a pretrained Q-learner
3. Alter the hyperparameters at the top of Qlearner.py to train a new Q-learner agent
4. Swap the input file at the top of GenerateMonster.py to use your new Q-learner agent and get output from it
5. Make further changes to GenerateMonster.py to alter how to generate/sample from trained agents, Qlearner.py to alter the training process and get new agents, and MDP.py to alter the Markov Decision Process. 
6. Rerun Qlearner.py then GenerateMonster.py to see the impact of your changes.  
