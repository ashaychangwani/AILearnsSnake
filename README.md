# AILearnsSnake

This app was an experimental game used to create a game in Python using PyGame and then teaching an AI to play the game using an **Artificial Neural Network** and optimizing the gameplay using **Genetic Algorithm (GA)**.

# Demo
![Demo](images/demo.gif)
___
The snakes look in 8 intercardinal directions, and in each direction, check for 3 things:
    1. Whether the apple exists in the chosen direction
    2. Whether a part of the snake's body lies in the chosen    direction (and if yes, how far is it)
    3. How far the closest boundary is, along the chosen direction.

These 3 inputs multiplied by the 8 directions give us the 24 inputs that will be fed to the neural network. 

The neural network returns 3 kinds of output: 
    * 1: Move forward in the previous direction
    * 2: Turn left
    * 3: Turn right
Please note that these directions are relative to the current direction of the snake.

There is fairly detailed documentation for each function in each of the classes. Please feel free to go through them and raise a new pull request to add features or edits that you want to edit.

There will also be Medium posts regarding the project, the process followed to build it and the intuition behind it will be explained in depth in the blogs. I'll make sure to update the links into the README.md file as soon as the blogs are published. 

There are 4 files required to train the network.
* snake.py
* params.py
* nn.py
* ga.py

1. *snake.py*

    This file contains two classes: snake and environment. 

    The snake class is responsible for storage of all data relevant to the particular snake like the coordinates of it's head, the rest of it's body as well as results like score, time since it last ate an apple, etc.

    The Environment class contains information regarding the pygame frame, and is responsible for drawing the apple, snake and boundary onto the pygame frame. It also contains the game specific variables like the position of the apple at that instant, as well as generating a new apple position if the snake eats the previous apple. 

2. *nn.py*

    The nn.py file contains the NeuralNet class and contains the code for the neural network. The architecure of the neural network is as follows: 

    24 neurons in the input layer
        ReLU activation
    16 neurons in the hidden layer
        Softmax activation
    3 neurons in the output layer

    The 24 input and 3 outputs are explained above. The class is also responsible for generating the 24 inputs by taking information about the snake and it's surroundings and converting it into inputs that will be accepted by the neural network.

3. *params.py*

    This file simply initializes some variables that are shared between different classes. 

4. *ga.py*

    This is the class that needs to be run in order to train the neural network and run the Genetic Algo. The GeneticAlgo class is initialized by passing all the parameters about the display, the snake, the neural network and hyperparameters for the genetic algorithm (like percentage for elitism, mutation, crossover, etc). 

    The class starts with executing the "runner" function. It iterates through the number of generations to train for, and logs infromation about each generation-- like the average score, the 90th percentile score, etc.

    Once it has executed for all generations, it takes the top n snakes of each generation and saves them in a file so that they can be visualized later. 

    The rest of the GA functions have been documented in depth within the ga.py file, feel free to go through them for any other clarification. 