__author__ = "Andrew Goh"
__email__ = "andrewgoh2000@gmail.com"

#Algorithm follows pseudocode from:
# https://stackoverflow.com/questions/62430071/donald-knuth-algorithm-mastermind

import random
import itertools as iter
from mastermind import evaluate_guess

class MastermindAgent():
    """
    A class that encapsulates the code dictating the
    behaviour of the agent playing the game of Mastermind.
    ...
       
    Attributes
    ----------
    code_length: int
        the length of the code to guess
    colours : list of char
        a list of colours represented as characters
    num_guesses : int
        the max. number of guesses per game

    Methods
    -------
    setFirstGuess()
        Returns the first guess to be used based on the code length and available colours

    setSecondGuess()
        Returns the second guess that has the second most variety of colours from the remaining solutions

    findNext()
        Returns the next guess using minimax concepts.

    AgentFunction(percepts)
        Returns the next guess of the colours on the board
    
    """
    def __init__(self, code_length,  colours, num_guesses):
      """
      :param code_length: the length of the code to guess
      :param colours: list of letter representing colours used to play
      :param num_guesses: the max. number of guesses per game
      """
      self.code_length = code_length
      self.colours = colours
      self.num_guesses = num_guesses
      #Store possible solutions
      self.solutions = []
    
    def setFirstGuess(self):
        """
        Returns the first guess to be used based on the code length and available colours
        """
        #Action to be returned
        action = []

        #Fill actions based on length of colours list.
        for i in range(self.code_length):
            #Alternates colours in self.colours and ensures that the index does not exceed the length of colours list
            index = (i // 2) % len(self.colours)

            #Append to action
            action.append(self.colours[index])

        return action
    
    def setSecondGuess(self):
        """
        Returns the second guess that has the second most variety of colours from the remaining solutions
        """
        #Exception if the code length or available colours is 2 or less. Returns random solution instead
        if self.code_length <= 2 or len(self.colours) <= 2: return random.choice(self.solutions)

        #Counter for the number of different elements in list
        variety_count = 0
        #Action to be returned
        action = None
        #Loop through all possible solutions
        for s in self.solutions:
            #Count variety in s
            count = 0
            colour = '' #Current colour
            colours = [] #List of colours to avoid checking the same colour again
            for c in s: #Count how many colours are in each guess
                if c != colour and c not in colours: 
                    colour = c
                    count += 1
                    colours.append(colour) #add to colour list
            if count >= variety_count and count < self.code_length: #Overrides variety count and append to possible actions
                variety_count = count
                action = s

        return action #Return a random action from the list that has guesses with the second most possible variety of colours
    
    def findNext(self):
        """
        Returns the next guess using minimax concepts
        """
        #List to keep track of Max scores of each solution in remaining solutions
        check = []
        #Check if theres only one solution left and return that solution if so
        if len(self.solutions) == 1: return self.solutions[0]
        #Loop through remaing guesses
        for s in self.solutions: #For each solution in remaining solution
            #Dictionary of scores, the score would be the count of remaining solutions from one solution in the remaining solution
            scores = {}
            for t in self.solutions:
                #if t and s are not the same
                if(t != s):
                    #Set current score of t and s
                    current_score = evaluate_guess(t, s)
                    #If scores are empty or current score not in scores, add count of 1
                    if scores == {} or current_score not in scores:
                        scores[current_score] = 1
                    #else update count of score in current scores
                    else:
                        scores[current_score] += 1
            #At end of loop, take score with highest amount and append it to check
            check.append(max(scores.values()))
        #Take index of remaining solutions list from the index that contains the min value of check
        lowest_of_worst = check.index(min(check))
        return self.solutions[lowest_of_worst]
    

    def AgentFunction(self, percepts):
        """Returns the next board guess given state of the game in percepts
        :param percepts: a tuple of four items: guess_counter, last_guess, in_place, in_colour
        , where
        guess_counter - is an integer indicating how many guesses have been made, starting with 0 for
        initial guess;
        last_guess - is a num_rows x num_cols structure with the copy of the previous guess
        in_place - is the number of character in the last guess of correct colour and position
        in_colour - is the number of characters in the last guess of correct colour but not in the
                    correct position
        :return: list of chars - a list of code_length chars constituting the next guess
        """
        # Extract different parts of percepts.
        guess_counter, last_guess, in_place, in_colour = percepts
        
        #Assign first guess
        if(guess_counter == 0):
            #Create list of possible solutions
            solutions = iter.product(self.colours, repeat=self.code_length)
            self.solutions = [list(e) for e in solutions]

            #Set first guess and return
            return self.setFirstGuess()
        else:#Not the first guess
            #Remove previous guess
            self.solutions.remove(last_guess)
            #Remove unrelated solutions, way taken from chatGPT to check if (1,2) and (1,2) are equal without loop
            self.solutions = [s for s in self.solutions if evaluate_guess(s, last_guess) == (in_place, in_colour)]
            #Assign second guess
            if (guess_counter == 1):
                #Returning second guess

                # return random.choice(self.solutions) #Return random guess from solutions list, used in testing
            
                return self.setSecondGuess() #Return second guess using second guess function
            
            else: #Use minimax function to assign guesses from third guess onwards
                return self.findNext()
            
