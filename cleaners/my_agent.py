__author__ = "Andrew Goh"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "andrewgoh2000@gmail.com"

import numpy as np
import random
import math

#Agent details
agentName = "biasedbutbad2"
trainingSchedule = [("random_agent.py", 500)]

#Store best population
best_population = None

#Store best fitness value
best_fitness = 0

#Store fitness scores for graph printing
training_scores = []
print_check = False #Print check, set to true to return textfile of average fitness scores

#Variables to keep track of training count to return the best_population
schedule_count = 1

def calculateScheduleCount(trainingSchedule):
    """
    Function to determine total schedule count

    :param trainingSchedule: list of trainingSchedule stating agent name and number of times to trai

    :return: integer of total number of times to train schedule
    """   
    if trainingSchedule == None or len(trainingSchedule) == 0:
        return 0
    if len(trainingSchedule) == 1:
        return trainingSchedule[0][1]
    if len(trainingSchedule) == 2:
        return trainingSchedule[0][1] + trainingSchedule[1][1]

#Total times agent is trained determined by schedule count
total_schedule_count = calculateScheduleCount(trainingSchedule)

class Cleaner:
    """
    A class for the cleaner agent that is used by cleaners.py
    ...
       
    Attributes
    ----------
    param nPercepts: total count of percepts
    param nActions: total count of actions
    param gridSize: size of grid given as a (Y, X) tuple
    param maxTurns: number of turns available

    Methods
    -------
    AgentFunction(percepts)
        Returns the next action list for the cleaner robot
    
    """
    def __init__(self, nPercepts, nActions, gridSize, maxTurns):
        """
        param nPercepts: total count of percepts
        param nActions: total count of actions
        param gridSize: size of grid given as a (Y, X) tuple
        param maxTurns: number of turns available
        """
        #Initialisation of Cleaner attributes
        self.nPercepts = nPercepts
        self.nActions = nActions
        self.gridSize = gridSize
        self.maxTurns = maxTurns

        #Chromosome numpy array (nActions x nPercepts + 1)
        self.chromosome = np.random.randint(low=-100, high=100, size=(nActions, nPercepts + 1))

    def AgentFunction(self, percepts):
        """
        Returns the next action list for the cleaner robot

        :param percepts: variable containing 4 variables (visual, energy, bin, fails) to be used as the weights for the action vector

        :return: action_vector (list of 4 integers)
        """
        #Extract variables
        visual, energy, bin, fails = percepts
        #Flatten visual with numpy method flatten() and append remaining percepts
        agent_percepts = np.append(visual.flatten(), np.array([energy, bin, fails]))
        
        #Dynamically appending values to action vector based on nActions
        action_vector = []
        for action in range(self.nActions):
            #Weight = first 63 values of chromosome layer
            weight = self.chromosome[action, :len(agent_percepts)]
            #Bias = last value of chromosome layer
            bias = self.chromosome[action, -1]
            #Dot product of weight and percepts + bias to produce single value, append to action_vector
            action_vector.append(np.dot(weight, agent_percepts) + bias)

        return action_vector


def evalFitness(population):
    """
    Fitness function used by the function newGeneration() for implementing a genetic algorithm

    :param population: list of cleaners to be evaluated

    :return: list of fitness values of the population
    """
    #Get length of population
    population_length = len(population)

    # Fitness initialiser for all agents
    fitness = np.zeros((population_length))

    #Get scores of each cleaner in the population
    for index, cleaner in enumerate(population):
        fitness[index] = cleaner.game_stats['cleaned']

    return fitness


def newGeneration(old_population):
    """
    Function for implementing Genetic Algorithm
    
    :param old_population: list of cleaner objects to be used to produce the next generation of cleaners

    :return: new_population: list of new cleaners made from the genetic algorithm
             avg_fitness: the average fitness score of the old_population
    """
    #Global variables
    global best_fitness, best_population, schedule_count, total_schedule_count, training_scores, print_check

    #Variable of population to not override old population to cause major bug
    population = old_population

    #Store length of population
    population_length = len(old_population)

    # Fetch the game parameters stored in each agent (we will need them to create a new child agent)
    gridSize = old_population[0].gridSize
    nPercepts = old_population[0].nPercepts
    nActions = old_population[0].nActions
    maxTurns = old_population[0].maxTurns
    
    #Get fitness of the population
    fitness = evalFitness(population)

    #list of parents and scores
    parent_and_scores = []
    #Set parent_and_scores to have elements to contain (parent cleaner, fitness)
    for number in range(population_length):
        parent_and_scores.append((population[number], fitness[number]))

    #Get top 10% of parents
    best_parents = selectParent(parent_and_scores, population_length)

    # Create new population list
    new_population = list()
    
    #Fill new_population list until it reaches correct population length
    while len(new_population) != population_length:
        # Create a new cleaner
        new_cleaner = Cleaner(nPercepts, nActions, gridSize, maxTurns)

        #Select 2 random parents from best_parents
        ind1, ind2 = np.random.choice(len(best_parents), replace=False, size = 2)

        #Get child chromosome
        child_chromosome = makeChild(best_parents[ind1].chromosome, best_parents[ind2].chromosome)
        
        #Set new cleaner chromosome to child chromosome
        new_cleaner.chromosome = child_chromosome
        # Add the new cleaner to the new population
        new_population.append(new_cleaner)

    #Compute the average fitness of old population and return it along with the new population
    avg_fitness = np.mean(fitness)

    #Update best population if score is better
    if avg_fitness > best_fitness:
        best_population = population
        best_fitness = avg_fitness

    #Give best population at end of schedule
    if schedule_count == total_schedule_count - 1:
        if print_check: #print textfile if true
            training_scores.append(best_fitness) #Append best fitness instead
            np.savetxt("biasedbutbad2.txt", training_scores)
        return (best_population, best_fitness)
    
    #Append to training_scores
    training_scores.append(avg_fitness)
    
    #Update schedule count
    schedule_count += 1
    
    #Return new population and old population fitness
    return (new_population, avg_fitness)


def selectParent(parentlist, population_size):
    """
    Function for Selecting list of parents, it takes the top 10% of the population to be the parents
    
    :param parentlist: list of cleaner objects to be used to produce the next generation of cleaners
    :param population_size: size of population to be used for calculating length of selected parents list

    :return: list of the top 10% of parents in the parentlist
    """
    #Sort parents in parentlist according to score
    parentlist = sorted(parentlist, key=lambda sublist: sublist[1], reverse=True)

    selected = [] #list to contain top 10% of parents
    for parent in parentlist: #Add top 10% parents to selected list without their scores
        if len(selected) < math.floor(population_size * 0.1): 
            selected.append(parent[0])
        else: break

    #Return selected parents list (top 10% of parents)
    return selected


def makeChild(parent1, parent2):
    """
    Function for creating children from the two provided parent chromosomes
    
    :param parent1: chromosome from cleaner parent 1
    :param parent2: chromosome from cleaner parent 2

    :return: chromosome that will be used to override a new cleaner object chromosome variable
    """
    #Child to be returned
    child = []

    #Counter for filling child actions integers (accessing rows of chromosome)
    count = 0
    while len(child) != len(parent1):
        #Double point crossover indexes
        point = random.randint(0, len(parent1[count]) // 2)
        point2 = random.randint(point, len(parent1[count]))

        #Child chromosome layer
        child_layer = []

        #Fill child layer
        count2 = 0 #iterator for accessing columns of chromosome
        while len(child_layer) != len(parent1[count]):
            value = None #Store value of parent
            if count2 <= point or count2 >= point2:
                value = parent1[count][count2]
            else:
                value = parent2[count][count2]
            #Add to child
            child_layer.append(value)
            count2 += 1

        #Mutation of one value of each child_layer
        index = random.randint(0, len(child_layer) - 1)
        value = random.randint(-100,100)
        child_layer[index] = value

        #Add child layer (64 list of values) to child list
        child.append(child_layer)
        count += 1

    #Return child chromosome (nActions by nPercepts + 1 array)
    return np.array(child)