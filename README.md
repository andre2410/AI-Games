# AI-Games
Using AI to play games. Made during University assignments.

## Mastermind game

Mastermind is a game where you have to guess the secret code of colours. Each turn, you would know which colours are correct in the correct position and which colours are correct but in the wrong position. You win when all colours are in the correct position.

To make an agent that solves the game for you, I used an adjusted version of [Donald Knuth's algorithm](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm) and minimax to solve the game quickly. It can solve 100 games with an average of 4.83 guesses.

Pseudocode:
1. Start by creating a list of all possible combinations called C based on the length of the code and how many possible colours are available.

2. Give the first guess. The combination of the first guess would depend on the code length and colours. The first guess would have alternating colours which alternates between 2 counts of each colour. 
For example, the order for the first guess for a code length of 5 and 6 possible colours would consist of the first colour, 2 of the second colour and 1 of the third colour. 

3. If the game is won, end the algorithm. 

4. If the game continues, remove the previous guess and any unrelated possible combinations in C that does not give the same score as the first guess. The score is given from an evaluation method which was provided.
If the score of the first guess is (2,0) and another guess in C has a score of (1,0), it is	not the same and therefore is removed from C. 

5. For the second guess, consider the code length and the number of possible colours. If the code length is smaller, take the guess from C that has the second most possible variety of colours. If two guesses have the same colour variety, keep the more recent guess. The only exception would be if the code length or available colours are equal or less than 2 where a random guess from C will be selected.
	
6. If a guess is RBBGG and another guess is RGBBR, the RGBBR guess is selected. If the RGBBR guess is compared to a guess with the same number of colours, keep
the more recent guess. From the third guess onwards, a minimax technique is applied to find the next guess. 
For the remaining guesses in C, every guess could result in a set number of futher attempts achieve the correct combination. By using the same evaluation method that determines if two guesses are related, we can evaluate each guess in C and determine how many guesses are related to it by score. 

For example, guess B has 20 counts of score (1,4). That means there are 20 guesses related to it by the score (1,4). If the correct combination is related to that guess, it would take at most 20 more attempts of guessing to reach the correct combination. 
By applying the concepts of a minimax algorithm, we would take the worst count of each guess based on that comparison and choose the guess that has the lowest count among all the other guesses.

If there is only one guess remaining in C, use that guess and do not perform the minimax technique.

7. Repeat from step 3.

### Instructions to run game:
To run agent.py, please place it in the same folder with the following files:
mastermind.py: the main game file used to run the game.
settings.py: the file that contains the game settings such as code length.

To run the code using the IDE PyCharm, these steps can be followed:
1. Open PyCharm and create new project
2. For the project location, select the folder that contains the required files above
3. For the interpreter, use a Python environment that has the numpy library installed.
4. When asked whether to create the project from existing source, select Yes
6. Open settings.py and ensure that it is using agent.py in the "agentFile" setting. You can change the other settings to your desired game environment.
7. In the project pane, right click mastermind.py and select Run

You can run the game in any IDE as long as the Python interpreter can use the library numpy.

agent.py uses the inbuilt Python libraries itertools and random in addition to the provided libraries.


## Cleaners
This is more of a task than a game. I needed to optimise the performance of a vacuuming agent population called cleaners, tasked with cleaning an area. I was given an environment where the cleaner can move forwards or backwards in discrete steps and it can rotate in either direction by 90 degrees. When the cleaner drives over a dirty area, it automatically picks up the dirt unless its bin is full. The cleaners run on a battery that needs to be recharged periodically at a charging station (green square), where also the bin is emptied.
The objective is for the cleaners to clean the largest area they can. There is another population of cleaners with random actions on the environment, competing for cleaning credits. A cleaning tournament game would start and both populations of cleaners will compete to clean more squares to win. The game will be run on a 41x41 grid area, 40 cleaners per population and 100 turns(moves) per game. My task was to beat the random cleaners consistently after my agent is trained using a genetic algorithm, otherwise my agents should lose without any training. We can only have a maximum number of 500 training games for our training schedule. 

### Genetic algorithm implementation
The fitness function used for my implementation was the default fitness function provided by my lecturer. It calculates the fitness of each agent by counting the total number of dirt loads picked up and returns a list where each element is the score of each corresponding cleaner in the population. There were other parameters that can be used to evaluate the cleaner’s performance but due to the diversity of ways to adjust the fitness function, the default fitness function provided a sufficient scoring method to evaluate the population's behaviour. Moreover, more effort was catered towards improving the parent selection and child production of the algorithm whereby having cleaners that have a higher count of dirt loads picked up gives a reasonable scoring for the cleaner’s performance.

The genetic algorithm uses a training schedule of 500 games against the random agent. For the parent selection, I went with a biased selection of taking only the top 10% of the population in terms of their fitness scores. I made a list containing the previous population and the list respective scores acquired from the fitness function. I parsed it into the function selectParent() which takes the list mentioned and the population size as parameters. The function sorts the population list in descending order of scores and returns the top 10% of parents in terms of the scores which is then stored in a best_parents list.
For creating the next population of cleaners, I took two random parents (does not need to be unique) from the best_parents list and parsed their chromosomes as parameters into the makeChild() function. The makeChild() function creates an empty child list and enters the child chromosome creating process where it first does two-point crossover. It selects 2 random indexes (first index is less than half of 64 to ensure that values from both parents can be included in the child), it fills a child_layer list with values from the first parent chromosome layer up to the first index and then values from the second parent chromosome layer up to the second index and finally values from the first parent until the length of 64 is reached. A guaranteed mutation will happen by changing a single value in the chromosome layer to a random value between -100 and 100 and the chromosome layer would be added to the child list. The process repeats until the child list reaches the length of 4 (length of actions list of agent) and it returns the child chromosome (4 by 64 list of values).
A new cleaner agent would be created and the child chromosome would override the new cleaner chromosome. The process of creating children would be repeated until the number of children produced meets the population size. The new generation that consists of only children would be returned along with the old population’s fitness score determined by the fitness function. By following the training schedule specified in my_agent.py, the number of specified generations would be trained and the population that achieved the highest average fitness score would be returned when the training schedule finishes.


### Reasoning behind implementation:
The current solution uses similar concepts that could solve the eight queens problem within 4 generations. The problem was solved by using a genetic algorithm to find an ideal board state where all eight queen pieces on a 8 x 8 chessboard are in positions where no one can attack the other. By only having 64 possible values for the board positions and a list of 8 values for the chromosome (for each queen piece position), the variation of chromosomes was very little and the ideal fitness score could not be achieved within a low number of generations. However, having a high population count with a very biased parent selection that picks the best parents determined by the fitness score and guaranteed mutation, the variation issue was solved since a wider diversity of combinations can be covered within one generation.
The biased parent selection only produces a few parents per time (4 parents for a population of 40 cleaners). This ensures that the next generation would have chromosome values from the fittest parents in the population. Due to the limited number of parents, having a guaranteed mutation rate and asexual reproduction prevents the problem of having low variation across generations.
Although a high mutation rate sacrifices consistency where new generations could have much worse fitness scores, being able to choose which population to return at the end of the training schedule negates this problem. Similar to how the eightqueens problem just needs one correct combination out of the population, the generations of cleaners just needs to produce the best population it can to be used for the tournament game.
By changing only one index out of the 64 values in the chromosome layer, the mutation does not change the chromosome values drastically thus preventing the next generation from being completely different to the previous generation.

### Instructions to run code:
To run my_agent.py, please place it in the same folder with the following files:
cleaners.py: the main game file used to run the game.
settings.py: the file that contains the game settings.

To run the code using the IDE PyCharm, these steps can be followed:
1. Open PyCharm and create new project
2. For the project location, select the folder that contains the required files above
3. For the interpreter, use a Python environment that has the numpy library installed.
4. When asked whether to create the project from existing source, select Yes
6. Open settings.py and ensure that it is using agent.py in the "agentFile" setting. You can change the other settings to your desired game environment.
7. In the project pane, right click cleaners.py and select Run

To test without training:
Change the trainingSchedule variable in my_agent.py to None. After this, check if the player settings in settings.py has player1 as agent.py and player2 to random_agent.py. Run cleaners.py and "biasedbutbad2" should lose to random almost everytime due to no training.

You can run the game in any IDE as long as the Python interpreter can use the library numpy.

my_agent.py uses the inbuilt Python libraries itertools and random in addition to the provided libraries:
numpy
random
math


