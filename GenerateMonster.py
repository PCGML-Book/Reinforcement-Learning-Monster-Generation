from MDP import *
import pickle,random

#Load agent
qTable = pickle.load(open("qTable1000.pickle", "rb"))

actions = ["raiseHealth", "lowerHealth", "raiseArmor", "lowerArmor", "raiseSpeed", "lowerSpeed", "raiseDamage", "lowerDamage"]
done = False
doneThreshold = 0.8

rolloutIndex = 0
maxRolloutLength = 500

maxAttempts = 100
bestMonster = None
bestReward = -1

for attempt in range(0, maxAttempts):
	monsterInit = RandomState()
	currState = monsterInit.clone()

	while not done and rolloutIndex<maxRolloutLength:
		rolloutIndex+=1

		#Action Selection
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

print ("Final Reward Value: "+str(bestReward))
print ("Final Monster: "+str(bestMonster))

