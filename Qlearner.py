from MDP import *
import random,pickle

#Hyperparameters
totalEpisodes = 1000
maxRolloutLength = 100
learningRate = 0.1
discountFactor = 0.5
epsilon = 0.85
epsilonDecay = 0.001
random.seed(1) #Ensures a consistent training result

actions = ["raiseHealth", "lowerHealth", "raiseArmor", "lowerArmor", "raiseSpeed", "lowerSpeed", "raiseDamage", "lowerDamage"]
qTable = {}#state->actions->values

for i in range(0, totalEpisodes):
	monsterInit = RandomState()
	SARs = []
	rolloutIndex = 0
	totalReward = 0

	currentState = monsterInit.clone()
	while rolloutIndex < maxRolloutLength:
		rolloutIndex+=1

		state = currentState

		#Action Selection
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

		#s_(t+1) <- s_t
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

pickle.dump(qTable,open("qTable"+str(totalEpisodes)+".pickle", "wb"))



