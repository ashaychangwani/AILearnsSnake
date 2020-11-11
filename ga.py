import random
import pickle
import time
from snake import Environment, snake
import numpy as np
import matplotlib.pyplot as plt
from params import *

class GeneticAlgo:

    def __init__(self, display_width, display_height, unit, NN_shape, init_NN, population_size, no_of_generations,
                 percentage_best_performers, percentage_worst_performers, mutation_percent, mutation_intensity):
        """
        Initializes an object of class GeneticAlgo with the parameters of the game. 

        Args:
            display_width (int): The width of the frame in pixels
            display_height (int): The height of the frame in pixels
            unit (int): The size of each block of the frame in pixels
            NN_shape (list): The shape of the NeuralNetwork responsible for converting the input to outputs
            init_NN (bool): Boolean decribing whether the neural network should be initialized with random wieghts
            population_size (int): Number of objects in each generation
            no_of_generations (int): Number of generations to run the neural net
            percentage_best_performers (int): Percentage of top performers of the previous generation to be used for elitism
            percentage_worst_performers (int): Percentage of worst performers of the previous generation to be used for elitism
            mutation_percent (int): Percentage chance of mutation of each member in weight matrix
            mutation_intensity (int): Intensity of mutation (magnitude of change in the weights)
        """

        self.display_width = display_width
        self.display_height = display_height
        self.unit = unit
        self.NN_shape = NN_shape
        self.init_NN = init_NN
        self.population_size = population_size
        self.no_of_generations = no_of_generations
        self.percentage_best_performers = percentage_best_performers
        self.percentage_worst_performers = percentage_worst_performers
        self.mutation_percent = mutation_percent
        self.mutation_intensity = mutation_intensity

    def run(self, snakes, environment):
        """Runs the snake for a single generation.

        Args:
            snakes (list of type snake): List of all the snakes of the current generation to be run.
            environment (object): Object of type environment

        Returns:
            average of all scores
            90th percentile scores
        """

        i = 1
        scores = []

        generation_seed = random.random()
        for snake in snakes:
            start_time = time.time()
            checkloop = False
            self.progress(i/self.population_size, 30)
            random.seed(generation_seed)
            apple_position = environment.create_new_apple(snake.snake_position)
            snake.neuralnet.setNextFood(apple_position)

            while(snake.isAlive()):
                if (snake.head_x, snake.head_y) == environment.apple_position:
                    snake.time_since_apple = 0
                    result = snake.neuralnet.decision(
                        snake.head_x, snake.head_y, snake.snake_position, snake.direction)
                    snake.eatApple(result)
                    start_time = time.time()
                    snake.neuralnet.setNextFood(
                        environment.create_new_apple(snake.snake_position))
                    checkloop = False

                if snake.time_since_apple > 250:  # could be tuned
                    if not checkloop:
                        checkloop = True
                        any_point = (snake.head_x, snake.head_y)
                        times = 0
                    elif (snake.head_x, snake.head_y) == any_point:
                        times += 1
                        if times > 2:
                            snake.collision_with_boundary = True
                            snake.collision_with_self = True

                if time.time() - start_time > 0.5:
                    snake.collision_with_boundary = True
                    snake.collision_with_self = True

                result = snake.neuralnet.decision(
                    snake.head_x, snake.head_y, snake.snake_position, snake.direction)

                if snake.move(result) == False:
                    break
            random.seed()
            scores.append(len(snake.snake_position) - 1)
            i += 1
        print("\nAverage: %.2f \n90th percentile: %.2f" %
              (np.average(scores), np.percentile(scores, 90)))
        return np.average(scores), np.percentile(scores, 90)

    def print_top(self, snakes):
        """Prints information (number, score, and reason for death) about the top snakes in each generation

        Args:
            snakes (list): List of objects (of type snake) of the top for current generation
        """
        i = 0
        for snake in snakes:
            i += 1
            print('snake ', i, ', score : ', len(snake.snake_position)
                  - 1, end='\t')
            if snake.collision_with_self and snake.collision_with_boundary:
                print('stuck in loop')
            elif snake.collision_with_boundary and not snake.collision_with_self:
                print('crashed wall')
            else:
                print('crashed body')

    def save(self, snakes, filename):
        """Saves the top snakes from every generation into a pickle file to be loaded in the gui.py file

        Args:
            snakes (list): List of top snakes of every generation
            filename (str): String representing filename of the output file
        """
        f = open(filename, "wb")
        pickle.dump(snakes, f)
        f.close()

    def cloneOfParents(self, parents):
        """Creates clones of parents selected for elitism to be added to the next generation

        Args:
            parents (list): List of parents selected for elitism

        Returns:
            [list]: List of the clones of the input snakes
        """
        snakes = []
        for parent in parents:
            babySnake = snake(self.display_width, self.display_height,
                                    self.NN_shape, self.unit,
                                    False)
            babySnake.neuralnet.theta = parent.neuralnet.theta
            babySnake.neuralnet.bias = parent.neuralnet.bias
            snakes.append(babySnake)
        return snakes

    def elitism(self, snakes):
        """Selects top performing parents for elitism (along with a few bottom performers for variance)

        Args:
            snakes (list): List of all snakes in the generation sorted by their scores

        Returns:
            [list]: List of parents that have been selected for elitism and cloned for future generation
        """
        parents = []
        num_top = int(self.population_size *
                              self.percentage_best_performers / 100)
        num_bottom = int(self.population_size *
                                 self.percentage_worst_performers / 100)

        parents.extend(self.cloneOfParents(snakes[:num_top]))
        parents.extend(self.cloneOfParents(snakes[-num_bottom:]))
        return parents, num_top, num_bottom
    
    def create_new_pop(self, snakes):
        """Function to create the new generation using the parents from the previous generation

        Args:
            snakes (list): List of all snakes from the previous generation

        Returns:
            [list]: List of snakes that represent the next generation
        """
        parents, num_top, num_bottom = self.elitism(snakes)
        children = self.offspringGeneration(
            parents, self.population_size - num_top - num_bottom)

        children = self.mutate(children)
        parents.extend(children)
        return parents

    def crossOver(self, parent1, parent2):
        """Performs crossover function of genetic algos

        Args:
            parent1 (snake): Input parent 1
            parent2 (snake): Input parent 2

        Returns:
            [snake]: Returns the child born from crossover of the two input parents
        """
        child = snake(self.display_width, self.display_height,
                            self.NN_shape, self.unit)
        for i in range(len(parent1.neuralnet.theta)):
            for j in range(parent1.neuralnet.theta[i].shape[0]):
                for k in range(parent1.neuralnet.theta[i].shape[1]):
                    child.neuralnet.theta[i][j, k] = random.choice([
                        parent1.neuralnet.theta[i][j, k],
                        parent2.neuralnet.theta[i][j, k]])

            for j in range(parent1.neuralnet.bias[i].shape[1]):
                child.neuralnet.bias[i][0, j] = random.choice(
                    [parent1.neuralnet.bias[i][0, j],
                        parent2.neuralnet.bias[i][0, j]
                     ]
                )
        return child

    def offspringGeneration(self, parents, no_of_children):
        """Generates the rest of the population after elitism is done by perfoming crossover
           on the parents until the members of the next generation is equal to the specified 
           population

        Args:
            parents (list): List of snakes that have been selected via elitism
            no_of_children (int): Number of snakes that are to be generated via crossover

        Returns:
            [list]: List of all the snakes of the next generation produced via crossover
        """
        all_children = []
        for _ in range(no_of_children):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)

            all_children.append(self.crossOver(parent1, parent2))

        return all_children

    def mutate(self, children):
        """Performs mutation task of Genetic Algos on the snakes in order to increase variety

        Args:
            children (list): List of all snakes in current generation (produced via elitism + crossover)

        Returns:
            [list]: List of all snakes in current generation after mutation is complete
        """
        for child in children:
            for W in child.neuralnet.theta:
                for _ in range(int(W.shape[0] * W.shape[1] * self.mutation_percent/100)):
                    row = random.randint(0, W.shape[0]-1)
                    col = random.randint(0, W.shape[1]-1)
                    W[row][col] += random.uniform(-self.mutation_intensity,
                                                  self.mutation_intensity)
        return children

    def runner(self):
        """
        Main function of the GeneticAlgo Class that evaluates the result for each generation of
        and populates the next generation along.
        Prints the graph of the average and 90th percentile score for each generation to identify
        ideal early stopping point
        """
        snakes = [snake(self.display_width, self.display_height, self.NN_shape,
                              self.unit) for _ in range(self.population_size)]
        environment = Environment(self.display_height, self.display_width, self.unit)
        top_snakes = []
        averages = []
        percentile = []
        for i in range(self.no_of_generations):
            print('GENERATION: ', i+1, end='\n')
            avg, ptile = self.run(snakes, environment)
            averages.append(avg)
            percentile.append(ptile)

            snakes.sort(key=lambda x:
                len(x.snake_position), reverse=True)

            self.print_top(snakes[0:5])

            top_snakes.append(snakes[:3])

            snakes = self.create_new_pop(snakes)
        self.save(top_snakes, "saved/test.pickle")
        plt.plot(averages)
        plt.plot(percentile)
        plt.show()

    def progress(self, percent, length):
        """Creates a progress bar to check progress of current generation

        Args:
            percent (int): Percentage that is complete
            length (int): Length of the progress bar
        """
        hashes = round(percent*length)
        print('\r', '*'*hashes + '_'*(length - hashes),
              '[{:.2%}]'.format(percent), end='')


if __name__ == '__main__':
    ga = GeneticAlgo(display_width, display_height, unit, NN_shape, init_NN, population_size, no_of_generations,
                     percentage_best_performers, percentage_worst_performers, mutation_percent, mutation_intensity)

    ga.runner()