from MDP import State, RandomState, RaiseHealth, LowerHealth, RaiseArmor, LowerArmor, RaiseSpeed, LowerSpeed, RaiseDamage, LowerDamage, RunGame, CalculateReward
import random,pickle

#Hyperparameters
totalEpisodes = 20 #total number of episodes to run for (likely way too few, just here as a starting point, try 100 or 1000 for more consistency)
maxRolloutLength = 100 #how many changes to try in a single episode (decrease for faster runtime, increase for better performance)
learningRate = 0.1 #how quickly to update the q-values (increase for faster convergence, decrease for more consistent learning/optimization)
discountFactor = 0.5 #how much to pay attention to future changes (increase for more longterm behaviour)
epsilon = 0.85 #how frequently to take the 'best' instead of random actions (increase for faster convergence, decrease for more exploration)
epsilonDecay = 0.001 #how quickly to decrease epsilon (increase for faster convergence, decrease for more exploration)
random.seed(1) #Ensures a consistent training result

#List of all actions in a string representation to make them easily hashable
actions = ["raiseHealth", "lowerHealth", "raiseArmor", "lowerArmor", "raiseSpeed", "lowerSpeed", "raiseDamage", "lowerDamage"]
qTable = {} #a dictionary of state->actions->values

#Iterate through each training episodes
for i in range(0, totalEpisodes):
	#Start with a totally random monster
	monsterInit = RandomState()
	#Track the state, action, and reward sequence
	SARs = []
	rolloutIndex = 0
	totalReward = 0 #track total reward

	currentState = monsterInit.clone() #Clone the state to make sure we can make changes to it and still track it
	while rolloutIndex < maxRolloutLength:
		rolloutIndex+=1
		state = currentState

		#Action Selection using decaying epsilon greedy
		action = random.choice(actions)
		if str(state) in qTable.keys():
			maxAction = action
			maxValue = -1000

			for a in actions:
				if a in qTable[str(state)].keys():
					if maxValue < qTable[str(state)][a]:
						maxValue = qTable[str(state)][a]
						maxAction = a
			action = maxAction
		else:
			action = random.choice(actions)

		if random.random()>epsilon:
			action = random.choice(actions)
		if epsilon<1:
			epsilon+=epsilonDecay

		#take an action to go to the next state s_(t+1) <- s_t
		nextState = state.clone()

		if action=="raiseHealth":
			nextState = RaiseHealth(nextState)
		elif action=="lowerHealth":
			nextState = LowerHealth(nextState)
		elif action=="raiseArmor":
			nextState = RaiseArmor(nextState)
		elif action=="lowerArmor":
			nextState = LowerArmor(nextState)
		elif action=="raiseSpeed":
			nextState = RaiseSpeed(nextState)
		elif action=="lowerSpeed":
			nextState = LowerSpeed(nextState)
		elif action=="raiseDamage":
			nextState = RaiseDamage(nextState)
		elif action=="lowerDamage":
			nextState = LowerDamage(nextState)
		
		reward = CalculateReward(nextState)
		totalReward+=reward

		SARs.append([str(state), action, reward])
		currentState = nextState

	print ("Episode: "+str(i)+" total reward: "+str(totalReward))

	# Q-update step
	for j in range(len(SARs)-1, 0, -1):
		oldQValue = 0#assume 0 initialization
		optimalFutureValue = -100

		if SARs[j][0] in qTable.keys():
			if SARs[j][1] in qTable[SARs[j][0]].keys():
				oldQValue = qTable[SARs[j][0]][SARs[j][1]]

			if j+1<len(SARs)-1:
				for a in actions:
					if a in qTable[SARs[j+1][0]].keys():
						if optimalFutureValue < qTable[SARs[j+1][0]][a]:
							optimalFutureValue = qTable[SARs[j+1][0]][a]
			else:
				optimalFutureValue = 0

		newQValue = oldQValue + learningRate*(SARs[j][2] + discountFactor*optimalFutureValue - oldQValue)

		if not SARs[j][0] in qTable.keys():
			qTable[SARs[j][0]] = {}

		qTable[SARs[j][0]][SARs[j][1]] = newQValue

#Dump the Q-table so we can load it later
pickle.dump(qTable,open("qTable"+str(totalEpisodes)+".pickle", "wb"))



