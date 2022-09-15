from MDP import State, RandomState, RaiseHealth, LowerHealth, RaiseArmor, LowerArmor, RaiseSpeed, LowerSpeed, RaiseDamage, LowerDamage, RunGame, CalculateReward
import pickle,random

#Hyperparameters
trainedQTableFile = open("qTable1000.pickle", "rb")
maxAttempts = 100 #max number of attempts allowed to find a balanced agent
maxRolloutLength = 500 #Make number of changes to attempt to make to find a balanced monster
doneThreshold = 0.8 #How good (according to the reward function) does a monster need to be

#Load the agent we're choosing to use
qTable = pickle.load(trainedQTableFile)

#Set of actions
actions = ["raiseHealth", "lowerHealth", "raiseArmor", "lowerArmor", "raiseSpeed", "lowerSpeed", "raiseDamage", "lowerDamage"]

#Whether or not we're done
done = False
rolloutIndex = 0

#Tracking the best monster we've found so far
bestMonster = None
bestReward = -1

for attempt in range(0, maxAttempts):
	monsterInit = RandomState()
	currState = monsterInit.clone()

	while not done and rolloutIndex<maxRolloutLength:
		rolloutIndex+=1

		#Action selection using pure exploitation
		action = random.choice(actions)
		maxValue = -1000
		maxAction = action
		if str(currState) in qTable.keys():
			for a in actions:
				if a in qTable[str(currState)].keys():
					if maxValue < qTable[str(currState)][a]:
						maxValue = qTable[str(currState)][a]
						maxAction = a
			action = maxAction
		else:
			action = random.choice(actions)

		if maxValue>doneThreshold:
			done = True

		#s_(t+1) <- s_t
		nextState = currState.clone()

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

		currState = nextState

	reward = CalculateReward(currState)
	
	if reward>bestReward:
		bestMonster = currState
		bestReward = reward

#Close the file
trainedQTableFile.close()

#Print the final monster and reward value
print ("Final Reward Value: "+str(bestReward))
print ("Final Monster: "+str(bestMonster))

