import random

#Hyperparameters
numGamesPerMonster = 1000 #Using one thousand instead of one million discussed in Chapter 10

#Every state is a monster. Typically we would have a separate environment representation, but here the state encompasses all the info in the environment
class State: 
	def __init__(self, _health, _armor, _speed, _damage):
		self.health = _health
		self.armor = _armor
		self.speed = _speed
		self.damage = _damage

	def clone(self): #Create a shallow copy of this monster/state
		return State(self.health, self.armor, self.speed, self.damage)

	def __str__(self):
		return "(H: "+str(self.health)+", A: "+str(self.armor)+", S: "+str(self.speed)+", D: "+str(self.damage)+")"

def RandomState():
	return State(random.randint(1,101), random.randint(0,51), random.randint(0,51), random.randint(1,51))


#ACTIONS (pass in a state, return the new state if the action would take us to a new state)
def RaiseHealth(monster):
	monsterClone = monster.clone()
	if monsterClone.health<100:
		monsterClone.health+=1
	return monsterClone

def LowerHealth(monster):
	monsterClone = monster.clone()
	if monsterClone.health>1:
		monsterClone.health-=1
	return monsterClone

def RaiseArmor(monster):
	monsterClone = monster.clone()
	if monsterClone.armor<50:
		monsterClone.armor+=1
	return monsterClone

def LowerArmor(monster):
	monsterClone = monster.clone()
	if monsterClone.armor>0:
		monsterClone.armor-=1
	return monsterClone

def RaiseSpeed(monster):
	monsterClone = monster.clone()
	if monsterClone.speed<50:
		monsterClone.speed+=1
	return monsterClone

def LowerSpeed(monster):
	monsterClone = monster.clone()
	if monsterClone.speed>0:
		monsterClone.speed-=1
	return monsterClone

def RaiseDamage(monster):
	monsterClone = monster.clone()
	if monsterClone.damage<50:
		monsterClone.damage+=1
	return monsterClone

def LowerDamage(monster):
	monsterClone = monster.clone()
	if monsterClone.damage>1:
		monsterClone.damage-=1
	return monsterClone

#Run one game of this monster against the 'balanced' monster
def RunGame(monster):
	balancedMonster = State(50, 25, 25, 25)

	monster1 = monster
	monster2 = balancedMonster

	#Boolean for who goes first
	balancedFirst = balancedMonster.speed > monster.speed

	if balancedFirst:
		monster1 = balancedMonster
		monster2 = monster

	#Include since it's possible to have a monster that can't kill balanced but can't be killed by balanced
	attempts = 0

	#Have them fight until one of them dies
	while monster1.health>0 and monster2.health>0 and attempts<100:
		attempts+=1

		#Check if monster1 hits
		if (float(monster2.speed)/100.0)>random.uniform(0,1):
			monster2.health-= max(0, monster1.damage-monster2.armor)

		#Check if monster2 is alive and hits
		if monster2.health>0 and (float(monster1.speed)/100.0)>random.uniform(0,1):
			monster1.health-= max(0, monster2.damage-monster1.armor)

	#Return +1 for a win, -1 for a loss, and 0 for a tie
	result = 0
	if attempts<100:
		if monster1.health>0 and monster2.health<=0:
			if balancedFirst:
				result = -1
			else:
				result = 1
		elif monster1.health<=0 and monster2.health>0:
			if balancedFirst:
				result = 1
			else:
				result = -1

	return result

#Calculate reward for reaching this specific monster as winrate over 'numGamesPerMonster' games
def CalculateReward(monster):
	wins = 0
	losses = 0
	ties = 0
	for i in range(0, numGamesPerMonster):
		outcome = RunGame(monster.clone())
		if outcome==1:
			wins+=1.0
		elif outcome==-1:
			losses+=1.0
		else:
			ties+=1.0

	winRate = float(wins)/float(numGamesPerMonster)
	return (0.5-abs(winRate-0.5))/0.5
