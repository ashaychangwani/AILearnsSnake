# AILearnsSnake

This app was an experimental game used to create a game in Python using PyGame and then teaching an AI to play the game using an **Artificial Neural Network** and optimizing the gameplay using **Genetic Algorithm (GA)**.

There are 3 required to execute the program.
    *main_game.py
    *nn.py
    *ga.py

1. *main_game.py*
    
    This file is what the entire snake game in Python is based out on. It writes the rules for the game, the score calculation for any given game, and displays the same to the user. 

    It can be played in two ways: by a user or by an AI. The two methods that facilitate it are playGame and playGameAI respectively.

    If a user is playing the game, it works based on the inputs from the user using the direction keys on the keyboard. The internal pygame clock is significantly slowed down to allow the user to process and decide the input. If no input is provided, it continues on the same path. If multiple inputs are provided, only the first input in the time frame is considered. 

    The scoring of the game is as follows:
        +500 for eating an apple
        -1 for moving in a direction towards the apple
        -2 for moving in a direction away from the apple
        -2000 for colliding with the boundaries
        -1500 for colliding with itself

    The final score is displayed at the end of each game. This also serves as the fitness function for our AI which quantifies the fitness of a particular chromosome in a generation of the GA.

        *calcParams
        This function is responsible for calculating the binary parameters that will be used as inputs by the neural network in order to determine what the ideal output is. The parameters are as follows: 
            1. FrontBlocked: Is the cell in front of the snake blocked? Blockage can be due to the snakes own body or the boundary.
            2. LeftBlocked: Is there a blockage to the immediate left of the snake head?
            3. RightBlocked: Is there a blockage to the immediate left of the snake head?
            4. GoalLeft: Is the goal towards the left of the snake head? 
            5. GoalRight: Is the goal towards the right of the snake head?
            6. GoalFront: Is the goal in front of the snake head?
            7. GoalBack: Is the goal behind the snake head? 
        These parameters change depending on the direction of movement of the snake.

        *move
        This function takes inputs from the user to facilitate the playGame function, and updates the game depending on the users input and checks for the multiple condititions at every iteration.

        *move2
        This function is what allows the AI to play the game. It gives the parameters as inputs to the neural network and gets the output in the range [0-2], where 0 means moving left, 1 means continuining straight, 2 means moving right.

    The other functions simply check the rules of the game to ensure it is being played correctly. 


2. *nn.py*
    This file contains the code that implements the artificial neural network for our game. The architecure of the ANN is as follows: 
        *Input layer: 7 neurons for 7 parameters
        *Hidden layer: 5 neurons, activation function=Sigmoid
        *Output layer: 3 neurons, activation function=Softmax

3. *ga.py*
    Finally, this file is what needs to be run in order to visualize the AI training itself on the snake game. It contains the implementation of the Genetic Algorithm that is being used for this game. 
    The specification for the GA are as follows:
    Initial Population = initPop 
    Generate Initial Population = createInitPop()
    Fitness Function = fitnessFn()  #It runs the game with the chromosome as weights to the neural network and the fitness of that gene is the final score.
    Selection = Takes place using the cumulative distributive function (cdf()) and choice() functions that essentially pick one gene from the pool with probabilitities proportional to their fitness value
    Crossover = crossOver() 
    Mutation = mutation() 
